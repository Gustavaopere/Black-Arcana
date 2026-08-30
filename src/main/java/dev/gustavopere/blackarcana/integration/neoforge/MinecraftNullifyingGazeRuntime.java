package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Server-authoritative dispel runtime for Nullifying Gaze.
 *
 * <p>Effects are fail-closed: only explicitly tagged/adapted effects may be removed,
 * protected effects always win, and public LivingEntity removal APIs are used so
 * NeoForge/provider cancellation hooks remain authoritative.</p>
 */
public final class MinecraftNullifyingGazeRuntime {
    public static final double MAX_RANGE_BLOCKS = 128.0D;

    public static final TagKey<MobEffect> NULLIFIABLE_EFFECTS = TagKey.create(
        Registries.MOB_EFFECT,
        ResourceLocation.fromNamespaceAndPath("black_arcana", "nullifiable"));
    public static final TagKey<MobEffect> PROTECTED_EFFECTS = TagKey.create(
        Registries.MOB_EFFECT,
        ResourceLocation.fromNamespaceAndPath("black_arcana", "nullification_protected"));

    private static final Map<MinecraftServer, EffectPolicyState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftNullifyingGazeRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftNullifyingGazeRuntime::onServerStopped);
    }

    /** Adapter hook. Registration is monotonic for the lifetime of one server instance. */
    public static void registerNullifiableEffect(MinecraftServer server, ResourceLocation effectId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(effectId, "effectId");
        stateFor(server).nullifiableEffects.add(effectId);
    }

    /** Adapter hook. Protected registration always overrides nullifiable registration. */
    public static void registerProtectedEffect(MinecraftServer server, ResourceLocation effectId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(effectId, "effectId");
        stateFor(server).protectedEffects.add(effectId);
    }

    public static NullifyResult nullify(
        MinecraftServer server,
        UUID casterId,
        UUID targetId,
        double maxRange
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");

        if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > MAX_RANGE_BLOCKS) {
            return NullifyResult.denied(
                "nullifying_gaze_range_config",
                "Nullifying Gaze range is outside the generic same-dimension remote safety ceiling");
        }
        if (casterId.equals(targetId)) {
            return NullifyResult.denied(
                "nullifying_gaze_self",
                "Nullifying Gaze requires a distinct target");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return NullifyResult.denied(
                "nullifying_gaze_caster_unavailable",
                "Caster must be loaded and alive");
        }
        if (target == null || !target.isAlive() || target.level() != level) {
            return NullifyResult.denied(
                "nullifying_gaze_target_unavailable",
                "Target must be loaded, alive and in the caster dimension");
        }
        if (!withinRange(caster, target, maxRange)) {
            return NullifyResult.denied(
                "nullifying_gaze_range",
                "Target is outside configured Nullifying Gaze range");
        }
        if (!caster.hasLineOfSight(target)) {
            return NullifyResult.denied(
                "nullifying_gaze_los",
                "Nullifying Gaze requires direct line of sight");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return NullifyResult.denied(
                "nullifying_gaze_runtime_unavailable",
                "Black Arcana server runtime is unavailable");
        }

        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, facts);
        if (!authorization.decision().allowed()) {
            return new NullifyResult(authorization.decision(), Optional.empty());
        }
        if (facts.boss()) {
            return NullifyResult.denied(
                "nullifying_gaze_boss_resistant",
                "Boss targets require an explicit provider-specific nullification contract");
        }

        EffectPolicyState state = stateFor(server);
        ArrayList<EffectCandidate> eligible = new ArrayList<>();
        for (Holder<MobEffect> effect : new ArrayList<>(target.getActiveEffectsMap().keySet())) {
            Optional<ResourceLocation> effectId = effect.unwrapKey().map(key -> key.location());
            if (effectId.isEmpty()) continue;
            ResourceLocation id = effectId.get();
            boolean nullifiable = effect.is(NULLIFIABLE_EFFECTS) || state.nullifiableEffects.contains(id);
            boolean protectedEffect = effect.is(PROTECTED_EFFECTS) || state.protectedEffects.contains(id);
            if (nullifiable && !protectedEffect) {
                eligible.add(new EffectCandidate(effect, id));
            }
        }
        eligible.sort(Comparator.comparing(candidate -> candidate.effectId().toString()));
        if (eligible.isEmpty()) {
            return NullifyResult.denied(
                "nullifying_gaze_no_eligible_effect",
                "Target has no explicitly nullifiable, unprotected active effect");
        }

        // Revalidate immediately before mutation; a rejected/cancelled removal remains fail-closed.
        if (!target.isAlive() || target.level() != level || !withinRange(caster, target, maxRange)) {
            return NullifyResult.denied(
                "nullifying_gaze_target_changed",
                "Target state changed before Nullifying Gaze settlement");
        }
        if (!caster.hasLineOfSight(target)) {
            return NullifyResult.denied(
                "nullifying_gaze_los",
                "Line of sight was lost before Nullifying Gaze settlement");
        }

        EffectCandidate chosen = eligible.getFirst();
        if (!target.removeEffect(chosen.effect())) {
            return NullifyResult.denied(
                "nullifying_gaze_removal_rejected",
                "The selected effect rejected or no longer accepted removal");
        }
        return new NullifyResult(ArcanaDecision.allow(), Optional.of(chosen.effectId()));
    }

    private static EntityInteractionAuthorization authorize(
        ArcanaServerRuntime runtime,
        ServerLevel level,
        LivingEntity caster,
        LivingEntity target,
        EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.CONTROL,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.CONTROL));
    }

    private static boolean withinRange(LivingEntity caster, LivingEntity target, double maxRange) {
        double distanceSquared = caster.distanceToSqr(target);
        return Double.isFinite(distanceSquared) && distanceSquared <= maxRange * maxRange;
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static EffectPolicyState stateFor(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new EffectPolicyState());
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static final class EffectPolicyState {
        private final Set<ResourceLocation> nullifiableEffects = ConcurrentHashMap.newKeySet();
        private final Set<ResourceLocation> protectedEffects = ConcurrentHashMap.newKeySet();
    }

    private record EffectCandidate(Holder<MobEffect> effect, ResourceLocation effectId) {
        private EffectCandidate {
            Objects.requireNonNull(effect, "effect");
            Objects.requireNonNull(effectId, "effectId");
        }
    }

    public record NullifyResult(ArcanaDecision decision, Optional<ResourceLocation> removedEffectId) {
        public NullifyResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(removedEffectId, "removedEffectId");
            if (!decision.allowed() && removedEffectId.isPresent()) {
                throw new IllegalArgumentException("Denied Nullifying Gaze result cannot report a removed effect");
            }
        }

        private static NullifyResult denied(String code, String detail) {
            return new NullifyResult(ArcanaDecision.deny(code, detail), Optional.empty());
        }
    }
}
