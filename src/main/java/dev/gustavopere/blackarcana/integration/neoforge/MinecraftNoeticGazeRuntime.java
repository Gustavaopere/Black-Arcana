package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.NoeticGazePolicy;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.NullificationRegistry;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Loaded-only, server-authoritative runtime for Gaze of Stillness and Nullifying Gaze.
 *
 * <p>The runtime never acquires chunks, never reflects provider state and never applies permanent
 * faction/team/AI mutations. Stillness is maintained only while reciprocal sight/facing and the
 * canonical CONTROL authorization remain valid. Nullification removes only explicitly registered
 * effect ids and revalidates authorization immediately before settlement.</p>
 */
public final class MinecraftNoeticGazeRuntime {
    private final NullificationRegistry nullificationRegistry;
    private final Map<MinecraftServer, ServerState> states = new IdentityHashMap<>();

    public MinecraftNoeticGazeRuntime(NullificationRegistry nullificationRegistry) {
        this.nullificationRegistry = Objects.requireNonNull(nullificationRegistry, "nullificationRegistry");
    }

    public synchronized ArcanaDecision startStillness(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            int requestedDurationTicks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");
        if (casterId.equals(targetId)) {
            return deny("gaze_self_target", "Gaze of Stillness requires a distinct target");
        }
        if (requestedDurationTicks <= 0 || requestedDurationTicks > NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS) {
            return deny("gaze_duration", "Requested gaze duration exceeds the hard Noetic ceiling");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || !caster.isAlive()) {
            return deny("gaze_caster_unavailable", "Caster must be a loaded living entity");
        }
        if (target == null || !target.isAlive()) {
            return deny("gaze_target_unloaded", "Gaze target must be a loaded living entity");
        }
        if (!(caster.level() instanceof ServerLevel level) || target.level() != level) {
            return deny("gaze_dimension", "Caster and gaze target must share one loaded server dimension");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return deny("gaze_runtime_unavailable", "Canonical server interaction authority is unavailable");
        }

        EntityProtectionFacts protectionFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, protectionFacts);
        ArcanaDecision gazeAdmission = NoeticGazePolicy.authorizeStillness(gazeFacts(caster, target, authorization));
        if (!gazeAdmission.allowed()) return gazeAdmission;

        long nowTick = server.overworld().getGameTime();
        ServerState state = states.computeIfAbsent(server, ignored -> new ServerState());
        pruneDiminishingReturns(state, nowTick);

        Long playerImmunityUntil = state.playerImmunityUntil.get(targetId);
        if (target instanceof ServerPlayer
                && playerImmunityUntil != null
                && nowTick < playerImmunityUntil) {
            return deny(
                    "gaze_player_reapplication_immunity",
                    "Player target remains inside the canonical Stillness reapplication-immunity window");
        }
        if (state.byCaster.containsKey(casterId)) {
            return deny("gaze_caster_busy", "Caster already owns an active Gaze of Stillness session");
        }
        if (state.casterByTarget.containsKey(targetId)) {
            return deny("gaze_target_busy", "Target is already controlled by an active Gaze of Stillness session");
        }
        if (state.byCaster.size() >= NoeticSafetyCeilings.MAX_ACTIVE_GAZES) {
            return deny("gaze_capacity", "Active gaze registry reached its hard server ceiling");
        }

        DrState existingDr = state.drByTarget.get(targetId);
        int priorApplications = existingDr == null ? 0 : existingDr.stacks();
        if (existingDr == null && state.drByTarget.size() >= NoeticSafetyCeilings.MAX_GAZE_DR_TRACKED_TARGETS) {
            return deny("gaze_dr_capacity", "Diminishing-return registry reached its hard bounded capacity");
        }

        int playerControlCapTicks = target instanceof ServerPlayer
                ? Math.min(
                        authorization.limits().maxControlTicks(),
                        NoeticSafetyCeilings.MAX_PLAYER_GAZE_DURATION_TICKS)
                : authorization.limits().maxControlTicks();
        int effectiveTicks = NoeticGazePolicy.effectiveControlTicks(
                requestedDurationTicks,
                playerControlCapTicks,
                priorApplications);
        if (effectiveTicks <= 0) {
            return deny("gaze_dr_immunity", "Target is temporarily immune after repeated gaze control");
        }

        StillnessSession session = new StillnessSession(
                casterId,
                targetId,
                nowTick + effectiveTicks,
                target.getX(),
                target.getZ());
        state.byCaster.put(casterId, session);
        state.casterByTarget.put(targetId, casterId);
        state.drByTarget.put(
                targetId,
                new DrState(
                        Math.min(NoeticSafetyCeilings.MAX_GAZE_DR_STACKS, priorApplications + 1),
                        nowTick + NoeticSafetyCeilings.GAZE_DR_RESET_TICKS));
        if (target instanceof ServerPlayer) {
            state.playerImmunityUntil.put(
                    targetId,
                    nowTick + NoeticSafetyCeilings.GAZE_PLAYER_REAPPLICATION_IMMUNITY_TICKS);
        }
        restoreStillnessAnchor(target, session);
        return ArcanaDecision.allow();
    }

    /**
     * Applies the horizontal Stillness lock before the entity performs tick work. This corrects any
     * packet/previous-tick X/Z drift without cancelling the entity tick, so gravity and unrelated
     * entity logic continue to run normally.
     */
    public synchronized void enforceStillnessBeforeEntityTick(MinecraftServer server, LivingEntity target) {
        enforceStillnessMovement(server, target);
    }

    /** Applies the same lock after entity work so AI/travel during the tick cannot accumulate X/Z drift. */
    public synchronized void enforceStillnessAfterEntityTick(MinecraftServer server, LivingEntity target) {
        enforceStillnessMovement(server, target);
    }

    public synchronized NullificationResult nullify(MinecraftServer server, UUID casterId, UUID targetId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");
        if (casterId.equals(targetId)) {
            return NullificationResult.denied("nullifying_gaze_self_target", "Nullifying Gaze requires a distinct target");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || !caster.isAlive()) {
            return NullificationResult.denied("nullifying_gaze_caster_unavailable", "Caster must be a loaded living entity");
        }
        if (target == null || !target.isAlive()) {
            return NullificationResult.denied("nullifying_gaze_target_unavailable", "Target must be a loaded living entity");
        }
        if (!(caster.level() instanceof ServerLevel level) || target.level() != level) {
            return NullificationResult.denied("nullifying_gaze_dimension", "Caster and target must share one loaded server dimension");
        }
        if (caster.distanceToSqr(target) > gazeRangeSquared()) {
            return NullificationResult.denied("nullifying_gaze_range", "Target exceeds the hard Noetic gaze range");
        }
        if (!caster.hasLineOfSight(target)) {
            return NullificationResult.denied("nullifying_gaze_los", "Caster must maintain line of sight for nullification");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return NullificationResult.denied("nullifying_gaze_runtime_unavailable", "Canonical server interaction authority is unavailable");
        }

        EntityProtectionFacts protectionFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, protectionFacts);
        ArcanaDecision policy = NoeticGazePolicy.authorizeNullification(
                protectionFacts.boss(), authorization.decision().allowed());
        if (!policy.allowed()) return new NullificationResult(policy, 0);

        List<ResourceLocation> activeIds = activeEffectIds(target);
        List<ResourceLocation> selected = nullificationRegistry.selectNullifiable(activeIds);
        if (selected.isEmpty()) {
            return NullificationResult.denied(
                    "nullifying_gaze_no_eligible_effects",
                    "Target has no explicitly allowlisted nullifiable effects");
        }

        LivingEntity settlementTarget = findLoadedLivingEntity(server, targetId);
        LivingEntity settlementCaster = findLoadedLivingEntity(server, casterId);
        if (settlementTarget != target || settlementCaster != caster || !target.isAlive() || target.level() != level) {
            return NullificationResult.denied(
                    "nullifying_gaze_settlement_target_changed",
                    "Target or caster changed before nullification settlement");
        }
        if (caster.distanceToSqr(target) > gazeRangeSquared() || !caster.hasLineOfSight(target)) {
            return NullificationResult.denied(
                    "nullifying_gaze_settlement_sight",
                    "Range or line of sight changed before nullification settlement");
        }

        EntityProtectionFacts settlementFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization settlementAuthorization = authorize(
                runtime, level, caster, target, settlementFacts);
        ArcanaDecision settlementPolicy = NoeticGazePolicy.authorizeNullification(
                settlementFacts.boss(), settlementAuthorization.decision().allowed());
        if (!settlementPolicy.allowed()) return new NullificationResult(settlementPolicy, 0);

        Set<ResourceLocation> selectedSet = new LinkedHashSet<>(selected);
        int removed = 0;
        int scanned = 0;
        for (MobEffectInstance effect : new ArrayList<>(target.getActiveEffects())) {
            if (scanned++ >= NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES) break;
            ResourceLocation effectId = BuiltInRegistries.MOB_EFFECT.getKey(effect.getEffect().value());
            if (effectId == null || !selectedSet.contains(effectId)) continue;
            if (target.removeEffect(effect.getEffect())) {
                removed++;
                if (removed >= NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION) break;
            }
        }

        if (removed == 0) {
            return NullificationResult.denied(
                    "nullifying_gaze_settlement_empty",
                    "No allowlisted effect remained removable at settlement");
        }
        return new NullificationResult(ArcanaDecision.allow(), removed);
    }

    public synchronized void tick(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.get(server);
        if (state == null) return;

        long nowTick = server.overworld().getGameTime();
        pruneDiminishingReturns(state, nowTick);
        if (state.byCaster.isEmpty()) {
            if (state.drByTarget.isEmpty() && state.playerImmunityUntil.isEmpty()) states.remove(server);
            return;
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        List<UUID> closeCasters = new ArrayList<>();
        for (StillnessSession session : state.byCaster.values()) {
            if (nowTick >= session.expiresAtTick() || runtime == null) {
                closeCasters.add(session.casterId());
                continue;
            }

            LivingEntity caster = findLoadedLivingEntity(server, session.casterId());
            LivingEntity target = findLoadedLivingEntity(server, session.targetId());
            if (caster == null || target == null || !caster.isAlive() || !target.isAlive()
                    || !(caster.level() instanceof ServerLevel level) || target.level() != level) {
                closeCasters.add(session.casterId());
                continue;
            }

            EntityProtectionFacts protectionFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, protectionFacts);
            ArcanaDecision admission = NoeticGazePolicy.authorizeStillness(gazeFacts(caster, target, authorization));
            if (!admission.allowed()) {
                closeCasters.add(session.casterId());
                continue;
            }
            restoreStillnessAnchor(target, session);
        }
        for (UUID casterId : closeCasters) closeSession(state, casterId);
        if (state.byCaster.isEmpty()
                && state.drByTarget.isEmpty()
                && state.playerImmunityUntil.isEmpty()) {
            states.remove(server);
        }
    }

    public synchronized int activeGazes(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.get(server);
        return state == null ? 0 : state.byCaster.size();
    }

    public synchronized int clearEntity(MinecraftServer server, UUID entityId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(entityId, "entityId");
        ServerState state = states.get(server);
        if (state == null) return 0;

        List<UUID> closeCasters = new ArrayList<>();
        for (StillnessSession session : state.byCaster.values()) {
            if (session.casterId().equals(entityId) || session.targetId().equals(entityId)) {
                closeCasters.add(session.casterId());
            }
        }
        closeCasters.forEach(casterId -> closeSession(state, casterId));
        state.drByTarget.remove(entityId);
        state.playerImmunityUntil.remove(entityId);
        if (state.byCaster.isEmpty()
                && state.drByTarget.isEmpty()
                && state.playerImmunityUntil.isEmpty()) {
            states.remove(server);
        }
        return closeCasters.size();
    }

    public synchronized int clearForServerStop(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.remove(server);
        return state == null ? 0 : state.byCaster.size();
    }

    private void enforceStillnessMovement(MinecraftServer server, LivingEntity target) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(target, "target");
        ServerState state = states.get(server);
        if (state == null) return;

        UUID casterId = state.casterByTarget.get(target.getUUID());
        if (casterId == null) return;
        StillnessSession session = state.byCaster.get(casterId);
        if (session == null || !session.targetId().equals(target.getUUID())) return;

        long nowTick = server.overworld().getGameTime();
        if (nowTick >= session.expiresAtTick()) {
            closeSession(state, casterId);
            return;
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !target.isAlive()
                || !(caster.level() instanceof ServerLevel level) || target.level() != level) {
            closeSession(state, casterId);
            return;
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            closeSession(state, casterId);
            return;
        }
        EntityProtectionFacts protectionFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, protectionFacts);
        if (!NoeticGazePolicy.authorizeStillness(gazeFacts(caster, target, authorization)).allowed()) {
            closeSession(state, casterId);
            return;
        }

        restoreStillnessAnchor(target, session);
    }

    private static NoeticGazePolicy.Facts gazeFacts(
            LivingEntity caster,
            LivingEntity target,
            EntityInteractionAuthorization authorization
    ) {
        boolean sameDimension = caster.level() == target.level();
        boolean withinRange = sameDimension && caster.distanceToSqr(target) <= gazeRangeSquared();
        return new NoeticGazePolicy.Facts(
                true,
                sameDimension,
                withinRange,
                caster.hasLineOfSight(target),
                target.hasLineOfSight(caster),
                facing(caster, target),
                facing(target, caster),
                target.isAlive(),
                authorization.decision().allowed());
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

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static boolean facing(LivingEntity observer, LivingEntity target) {
        Vec3 toTarget = target.getEyePosition().subtract(observer.getEyePosition());
        if (toTarget.lengthSqr() <= 1.0E-12D) return true;
        Vec3 look = observer.getLookAngle();
        if (look.lengthSqr() <= 1.0E-12D) return false;
        return look.normalize().dot(toTarget.normalize()) > 0.0D;
    }

    private static void restoreStillnessAnchor(LivingEntity target, StillnessSession session) {
        if (target.getX() != session.anchorX() || target.getZ() != session.anchorZ()) {
            target.teleportTo(session.anchorX(), target.getY(), session.anchorZ());
        }
        suppressHorizontalMovement(target);
    }

    private static void suppressHorizontalMovement(LivingEntity target) {
        Vec3 motion = target.getDeltaMovement();
        if (motion.x != 0.0D || motion.z != 0.0D) {
            target.setDeltaMovement(0.0D, motion.y, 0.0D);
        }
    }

    private static List<ResourceLocation> activeEffectIds(LivingEntity target) {
        List<ResourceLocation> effectIds = new ArrayList<>();
        int scanned = 0;
        for (MobEffectInstance effect : target.getActiveEffects()) {
            if (scanned++ >= NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES) break;
            ResourceLocation id = BuiltInRegistries.MOB_EFFECT.getKey(effect.getEffect().value());
            if (id != null) effectIds.add(id);
        }
        return effectIds;
    }

    private static void pruneDiminishingReturns(ServerState state, long nowTick) {
        state.drByTarget.entrySet().removeIf(entry -> entry.getValue().resetAtTick() <= nowTick);
        state.playerImmunityUntil.entrySet().removeIf(entry -> entry.getValue() <= nowTick);
    }

    private static void closeSession(ServerState state, UUID casterId) {
        StillnessSession removed = state.byCaster.remove(casterId);
        if (removed != null) state.casterByTarget.remove(removed.targetId(), casterId);
    }

    private static double gazeRangeSquared() {
        return NoeticSafetyCeilings.MAX_GAZE_RANGE_BLOCKS * NoeticSafetyCeilings.MAX_GAZE_RANGE_BLOCKS;
    }

    private static ArcanaDecision deny(String code, String detail) {
        return ArcanaDecision.deny(code, detail);
    }

    private static final class ServerState {
        private final Map<UUID, StillnessSession> byCaster = new LinkedHashMap<>();
        private final Map<UUID, UUID> casterByTarget = new HashMap<>();
        private final Map<UUID, DrState> drByTarget = new LinkedHashMap<>();
        private final Map<UUID, Long> playerImmunityUntil = new LinkedHashMap<>();
    }

    private record StillnessSession(
            UUID casterId,
            UUID targetId,
            long expiresAtTick,
            double anchorX,
            double anchorZ
    ) {
        private StillnessSession {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(targetId, "targetId");
            if (!Double.isFinite(anchorX) || !Double.isFinite(anchorZ)) {
                throw new IllegalArgumentException("Stillness anchor must be finite");
            }
        }
    }

    private record DrState(int stacks, long resetAtTick) {
        private DrState {
            if (stacks <= 0 || stacks > NoeticSafetyCeilings.MAX_GAZE_DR_STACKS) {
                throw new IllegalArgumentException("DR stacks outside the hard Noetic ceiling");
            }
        }
    }

    public record NullificationResult(ArcanaDecision decision, int removedEffects) {
        public NullificationResult {
            Objects.requireNonNull(decision, "decision");
            if (removedEffects < 0 || removedEffects > NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION) {
                throw new IllegalArgumentException("Nullification result count exceeds the hard Noetic action ceiling");
            }
        }

        public static NullificationResult denied(String code, String detail) {
            return new NullificationResult(ArcanaDecision.deny(code, detail), 0);
        }
    }
}
