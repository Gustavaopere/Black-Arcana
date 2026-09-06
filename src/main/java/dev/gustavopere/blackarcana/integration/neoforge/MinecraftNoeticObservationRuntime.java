package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationFacts;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationPolicy;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationSession;
import dev.gustavopere.blackarcana.content.noetic.NoeticPerceptionSnapshot;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Minecraft-facing Stage 07.07 observation boundary.
 *
 * <p>Targets are resolved only from the server's already-loaded entity indexes. This adapter never owns
 * chunk acquisition, arbitrary entity serialization, inventories, capabilities, or client camera authority.</p>
 */
public final class MinecraftNoeticObservationRuntime {
    private final NoeticObservationRuntime observations;
    private final FamiliarOwnershipRegistry familiarOwnership;
    private final Map<UUID, AuthorizationContext> authorizationByViewer = new LinkedHashMap<>();

    public MinecraftNoeticObservationRuntime(
            NoeticObservationRuntime observations,
            FamiliarOwnershipRegistry familiarOwnership
    ) {
        this.observations = Objects.requireNonNull(observations, "observations");
        this.familiarOwnership = Objects.requireNonNull(familiarOwnership, "familiarOwnership");
    }

    public synchronized ArcanaDecision start(
            MinecraftServer server,
            UUID viewerId,
            UUID targetId,
            NoeticObservationKind kind,
            int durationTicks,
            boolean explicitConsent
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(targetId, "targetId");
        Objects.requireNonNull(kind, "kind");

        tick(server);
        ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
        if (viewer == null) {
            return ArcanaDecision.deny("noetic_viewer_unloaded", "Noetic observation requires a loaded server player viewer");
        }
        if (!viewer.isAlive()) {
            return ArcanaDecision.deny("noetic_viewer_dead", "Noetic observation requires a living viewer");
        }

        LoadedLivingTarget target = findLoadedLivingTarget(server, targetId);
        NoeticObservationFacts facts = facts(viewer, target, explicitConsent);
        ArcanaDecision admission = NoeticObservationPolicy.authorize(kind, facts);
        if (!admission.allowed()) return admission;

        NoeticObservationRuntime.StartResult result = observations.start(
                viewerId,
                targetId,
                kind,
                server.getTickCount(),
                durationTicks);
        return switch (result) {
            case STARTED -> {
                authorizationByViewer.put(viewerId, new AuthorizationContext(targetId, explicitConsent));
                yield ArcanaDecision.allow();
            }
            case VIEWER_ALREADY_ACTIVE -> ArcanaDecision.deny(
                    "noetic_viewer_active", "Viewer already owns an active Noetic observation session");
            case GLOBAL_LIMIT -> ArcanaDecision.deny(
                    "noetic_global_limit", "Noetic observation global active-session ceiling is exhausted");
            case INVALID_DURATION -> ArcanaDecision.deny(
                    "noetic_duration", "Noetic observation duration is outside the hard safety ceiling");
        };
    }

    public synchronized Optional<NoeticPerceptionSnapshot> snapshot(MinecraftServer server, UUID viewerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        tick(server);

        NoeticObservationSession session = observations.session(viewerId).orElse(null);
        AuthorizationContext context = authorizationByViewer.get(viewerId);
        if (session == null || context == null || !session.targetId().equals(context.targetId())) {
            authorizationByViewer.remove(viewerId);
            if (session != null) observations.close(viewerId, NoeticObservationSession.CloseReason.TARGET_UNAVAILABLE);
            return Optional.empty();
        }

        ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
        if (viewer == null) {
            clearViewer(viewerId, NoeticObservationSession.CloseReason.VIEWER_LOGOUT);
            return Optional.empty();
        }
        if (!viewer.isAlive()) {
            clearViewer(viewerId, NoeticObservationSession.CloseReason.VIEWER_DEATH);
            return Optional.empty();
        }

        LoadedLivingTarget target = findLoadedLivingTarget(server, session.targetId());
        NoeticObservationFacts facts = facts(viewer, target, context.explicitConsent());
        ArcanaDecision revalidation = NoeticObservationPolicy.authorize(session.kind(), facts);
        if (!revalidation.allowed() || target == null) {
            clearViewer(viewerId, NoeticObservationSession.CloseReason.TARGET_UNAVAILABLE);
            return Optional.empty();
        }
        return Optional.of(snapshotOf(target.entity()));
    }

    public synchronized void tick(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        observations.expire(server.getTickCount());
        authorizationByViewer.entrySet().removeIf(entry -> observations.session(entry.getKey()).isEmpty());

        Iterator<Map.Entry<UUID, AuthorizationContext>> iterator = authorizationByViewer.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<UUID, AuthorizationContext> entry = iterator.next();
            UUID viewerId = entry.getKey();
            ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
            if (viewer == null) {
                observations.clearViewer(viewerId, NoeticObservationSession.CloseReason.VIEWER_LOGOUT);
                iterator.remove();
                continue;
            }
            if (!viewer.isAlive()) {
                observations.clearViewer(viewerId, NoeticObservationSession.CloseReason.VIEWER_DEATH);
                iterator.remove();
                continue;
            }
            if (findLoadedLivingTarget(server, entry.getValue().targetId()) == null) {
                observations.clearViewer(viewerId, NoeticObservationSession.CloseReason.TARGET_UNAVAILABLE);
                iterator.remove();
            }
        }
    }

    public synchronized boolean clearViewer(UUID viewerId, NoeticObservationSession.CloseReason reason) {
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(reason, "reason");
        authorizationByViewer.remove(viewerId);
        return observations.clearViewer(viewerId, reason);
    }

    public synchronized int clearTarget(UUID targetId) {
        Objects.requireNonNull(targetId, "targetId");
        int closed = observations.clearTarget(targetId);
        authorizationByViewer.entrySet().removeIf(entry -> entry.getValue().targetId().equals(targetId));
        return closed;
    }

    public synchronized int clearForServerStop() {
        authorizationByViewer.clear();
        return observations.clearForServerStop();
    }

    NoeticObservationRuntime observations() {
        return observations;
    }

    FamiliarOwnershipRegistry familiarOwnership() {
        return familiarOwnership;
    }

    private NoeticObservationFacts facts(
            ServerPlayer viewer,
            LoadedLivingTarget target,
            boolean explicitConsent
    ) {
        if (target == null) {
            return new NoeticObservationFacts(false, false, false, false, false, false, explicitConsent, false);
        }
        LivingEntity entity = target.entity();
        boolean sameDimension = viewer.serverLevel() == target.level();
        boolean withinRange = sameDimension
                && viewer.distanceToSqr(entity) <= NoeticSafetyCeilings.MAX_RANGE_BLOCKS * NoeticSafetyCeilings.MAX_RANGE_BLOCKS;
        boolean ownedFamiliar = familiarOwnership.ownership(viewer.getUUID(), entity)
                == FamiliarOwnershipProvider.Result.OWNED;
        return new NoeticObservationFacts(
                true,
                sameDimension,
                withinRange,
                viewer.hasLineOfSight(entity),
                entity.isAlive(),
                entity instanceof ServerPlayer,
                explicitConsent,
                ownedFamiliar);
    }

    private static LoadedLivingTarget findLoadedLivingTarget(MinecraftServer server, UUID targetId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity candidate = level.getEntity(targetId);
            if (candidate instanceof LivingEntity living) {
                return new LoadedLivingTarget(level, living);
            }
        }
        return null;
    }

    private static NoeticPerceptionSnapshot snapshotOf(LivingEntity target) {
        String entityTypeId = String.valueOf(BuiltInRegistries.ENTITY_TYPE.getKey(target.getType()));
        String displayName = target.getDisplayName().getString();
        double maxHealth = target.getMaxHealth();
        double healthFraction = maxHealth > 0.0D && Double.isFinite(maxHealth)
                ? target.getHealth() / maxHealth
                : 0.0D;

        List<String> effects = new ArrayList<>();
        for (MobEffectInstance effect : target.getActiveEffects()) {
            if (effects.size() >= NoeticSafetyCeilings.MAX_EFFECT_IDS) break;
            effects.add(String.valueOf(BuiltInRegistries.MOB_EFFECT.getKey(effect.getEffect().value())));
        }
        String mainHandItemId = String.valueOf(BuiltInRegistries.ITEM.getKey(target.getMainHandItem().getItem()));
        return NoeticPerceptionSnapshot.sanitized(
                target.getUUID(),
                entityTypeId,
                displayName,
                healthFraction,
                effects,
                mainHandItemId);
    }

    private record LoadedLivingTarget(ServerLevel level, LivingEntity entity) {
        private LoadedLivingTarget {
            Objects.requireNonNull(level, "level");
            Objects.requireNonNull(entity, "entity");
        }
    }

    private record AuthorizationContext(UUID targetId, boolean explicitConsent) {
        private AuthorizationContext {
            Objects.requireNonNull(targetId, "targetId");
        }
    }
}
