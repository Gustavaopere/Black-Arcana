package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.AstralProjectionEntity;
import dev.gustavopere.blackarcana.content.noetic.AstralProjectionMovementIntent;
import dev.gustavopere.blackarcana.content.noetic.AstralProjectionPose;
import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.content.noetic.BlackArcanaNoeticEntities;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationSession;
import dev.gustavopere.blackarcana.content.noetic.NoeticPerceptionSnapshot;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.NullificationRegistry;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;
import dev.gustavopere.blackarcana.network.neoforge.NoeticViewNetworkBridge;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingChangeTargetEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalInt;
import java.util.Set;
import java.util.UUID;

/**
 * Stage 07.07 composition root for all Noetic/Familiar server lifecycle state.
 *
 * <p>This class owns only bounded ephemeral registries. Entity resolution remains loaded-only in the
 * concrete adapters; no method here acquires chunks, serializes arbitrary target state or creates a
 * second familiar system. Optional provider adapters may register only explicit ownership evidence.</p>
 */
public final class MinecraftNoeticRuntime {
    private static final Map<MinecraftServer, ServerState> STATES =
            Collections.synchronizedMap(new IdentityHashMap<>());
    private static boolean registered;

    private MinecraftNoeticRuntime() { }

    public static synchronized void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        if (registered) return;
        registered = true;
        gameBus.addListener(MinecraftNoeticRuntime::onServerStarted);
        gameBus.addListener(MinecraftNoeticRuntime::onEntityTickPre);
        gameBus.addListener(MinecraftNoeticRuntime::onEntityTickPost);
        gameBus.addListener(MinecraftNoeticRuntime::onLivingChangeTarget);
        gameBus.addListener(MinecraftNoeticRuntime::onLivingDamagePost);
        gameBus.addListener(MinecraftNoeticRuntime::onServerTick);
        gameBus.addListener(MinecraftNoeticRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftNoeticRuntime::onPlayerChangedDimension);
        gameBus.addListener(MinecraftNoeticRuntime::onLivingDeath);
        gameBus.addListener(MinecraftNoeticRuntime::onServerStopped);
    }

    /**
     * Registers one explicit provider. Optional mod bootstraps call this only after NeoForge confirms
     * the provider mod is present and its public API probe succeeds.
     */
    public static boolean registerFamiliarOwnershipProvider(
            MinecraftServer server,
            FamiliarOwnershipProvider provider
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(provider, "provider");
        return stateFor(server).familiarOwnership.register(provider);
    }

    public static int familiarProviderCount(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.familiarOwnership.providerCount();
    }

    public static ArcanaDecision startObservation(
            MinecraftServer server,
            UUID viewerId,
            UUID targetId,
            NoeticObservationKind kind,
            int durationTicks,
            boolean explicitConsent
    ) {
        return stateFor(server).observation.start(
                server, viewerId, targetId, kind, durationTicks, explicitConsent);
    }

    public static Optional<NoeticPerceptionSnapshot> observationSnapshot(
            MinecraftServer server,
            UUID viewerId
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        ServerState state = STATES.get(server);
        return state == null ? Optional.empty() : state.observation.snapshot(server, viewerId);
    }

    /**
     * Activates only the bounded Astral Severance lifecycle after an upstream canonical cast transaction
     * has already authorized the spell. This is not a second cast/admission path and does not select cost,
     * cooldown, progression or client presentation semantics.
     */
    public static AstralProjectionStart activateAuthorizedAstralProjection(
            MinecraftServer server,
            UUID casterId,
            int durationTicks,
            double maxRangeBlocks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");

        ServerPlayer caster = server.getPlayerList().getPlayer(casterId);
        if (caster == null) {
            return AstralProjectionStart.denied(
                    "astral_viewer_unloaded",
                    "Astral Severance requires a loaded server player body");
        }
        if (!caster.isAlive()) {
            return AstralProjectionStart.denied(
                    "astral_viewer_dead",
                    "Astral Severance requires a living physical body");
        }

        AstralProjectionPose originPose = new AstralProjectionPose(
                caster.getX(),
                caster.getY(),
                caster.getZ(),
                caster.getYRot(),
                caster.getXRot());
        ServerState state = stateFor(server);
        expireAstralProjections(server, state, server.getTickCount());
        reconcileAstralAvatars(server, state);
        AstralSeveranceRuntime.StartResult result = state.astral.start(
                casterId,
                server.getTickCount(),
                durationTicks,
                maxRangeBlocks,
                originPose);
        return switch (result) {
            case STARTED -> {
                AstralSeveranceRuntime.ActiveProjection projection =
                        state.astral.projection(casterId).orElseThrow();
                AstralProjectionEntity avatar =
                        BlackArcanaNoeticEntities.ASTRAL_PROJECTION.get().create(caster.serverLevel());
                if (avatar == null) {
                    state.astral.close(casterId, AstralSeveranceRuntime.CloseReason.AUTHORIZATION_REVOKED);
                    yield AstralProjectionStart.denied(
                            "astral_avatar_unavailable",
                            "Astral Severance could not create its server-owned viewpoint entity");
                }
                applyAstralPose(avatar, projection.currentPose());
                if (!caster.serverLevel().addFreshEntity(avatar)) {
                    avatar.discard();
                    state.astral.close(casterId, AstralSeveranceRuntime.CloseReason.AUTHORIZATION_REVOKED);
                    yield AstralProjectionStart.denied(
                            "astral_avatar_spawn_failed",
                            "Astral Severance viewpoint entity could not enter the loaded server level");
                }
                state.astralAvatars.put(
                        casterId,
                        new AstralAvatarRef(
                                projection.projectionId(),
                                caster.serverLevel().dimension(),
                                avatar.getId()));
                yield AstralProjectionStart.started(projection);
            }
            case CASTER_ALREADY_PROJECTED -> AstralProjectionStart.denied(
                    "astral_viewer_active",
                    "Caster already owns an active Astral Severance projection");
            case GLOBAL_LIMIT -> AstralProjectionStart.denied(
                    "astral_global_limit",
                    "Astral Severance global active-projection ceiling is exhausted");
            case INVALID_DURATION -> AstralProjectionStart.denied(
                    "astral_duration",
                    "Astral Severance duration is outside the hard Noetic ceiling");
            case INVALID_RANGE -> AstralProjectionStart.denied(
                    "astral_range",
                    "Astral Severance range is outside the hard Noetic ceiling");
            case IDENTITY_COLLISION -> AstralProjectionStart.denied(
                    "astral_identity_collision",
                    "Astral Severance could not allocate a unique server-owned projection identity");
        };
    }

    public static Optional<AstralSeveranceRuntime.ActiveProjection> astralProjection(
            MinecraftServer server,
            UUID casterId
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        ServerState state = STATES.get(server);
        return state == null ? Optional.empty() : state.astral.projection(casterId);
    }

    /** Applies bounded movement intent only through the canonical server-owned Astral lifecycle. */
    public static AstralSeveranceRuntime.MoveResult moveAstralProjection(
            MinecraftServer server,
            UUID casterId,
            AstralProjectionMovementIntent intent
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(intent, "intent");
        ServerState state = STATES.get(server);
        if (state == null) {
            return AstralSeveranceRuntime.MoveResult.NO_ACTIVE_PROJECTION;
        }

        AstralSeveranceRuntime.MoveResult result = state.astral.move(casterId, intent);
        if (result != AstralSeveranceRuntime.MoveResult.MOVED) {
            return result;
        }
        AstralSeveranceRuntime.ActiveProjection projection = state.astral.projection(casterId).orElse(null);
        if (projection == null || !syncAstralAvatarPose(server, state, casterId, projection)) {
            closeAstralProjection(
                    server,
                    state,
                    casterId,
                    AstralSeveranceRuntime.CloseReason.AUTHORIZATION_REVOKED);
            return AstralSeveranceRuntime.MoveResult.NO_ACTIVE_PROJECTION;
        }
        return AstralSeveranceRuntime.MoveResult.MOVED;
    }

    /** Exact-session explicit return. Wrong, stale or replayed projection identities are ignored. */
    public static boolean requestAstralReturn(MinecraftServer server, UUID casterId, UUID projectionId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(projectionId, "projectionId");
        ServerState state = STATES.get(server);
        if (state == null || !state.astral.requestReturn(casterId, projectionId)) {
            return false;
        }
        removeAstralAvatar(server, state, casterId);
        return true;
    }

    public static ArcanaDecision startStillness(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            int durationTicks
    ) {
        return stateFor(server).gaze.startStillness(server, casterId, targetId, durationTicks);
    }

    public static MinecraftNoeticGazeRuntime.NullificationResult nullify(
            MinecraftServer server,
            UUID casterId,
            UUID targetId
    ) {
        return stateFor(server).gaze.nullify(server, casterId, targetId);
    }

    public static boolean registerNullifiableEffect(MinecraftServer server, ResourceLocation effectId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(effectId, "effectId");
        return stateFor(server).nullifications.register(effectId);
    }

    public static ArcanaDecision activateSanctuary(
            MinecraftServer server,
            UUID ownerId,
            UUID familiarId,
            PactSanctuarySpec spec,
            Set<UUID> members
    ) {
        return stateFor(server).sanctuary.activate(server, ownerId, familiarId, spec, members);
    }

    public static int activeObservations(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.observations.activeCount();
    }

    public static int activeAstralProjections(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.astral.activeCount();
    }

    public static int activeGazes(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.gaze.activeGazes(server);
    }

    public static int activeSanctuaries(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.sanctuary.activeSanctuaries(server);
    }

    public static int activeStateCount(MinecraftServer server) {
        return activeObservations(server)
                + activeAstralProjections(server)
                + activeGazes(server)
                + activeSanctuaries(server);
    }

    /** Explicitly clears all Stage 07.07 state associated with an entity; repeated calls are idempotent. */
    public static int clearEntity(MinecraftServer server, UUID entityId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(entityId, "entityId");
        return clearLifecycleEntity(server, entityId, NoeticObservationSession.CloseReason.EXPLICIT);
    }

    private static void onServerStarted(ServerStartedEvent event) {
        stateFor(event.getServer());
    }

    private static void onEntityTickPre(EntityTickEvent.Pre event) {
        if (!(event.getEntity() instanceof LivingEntity living)
                || !(living.level() instanceof ServerLevel level)) {
            return;
        }
        MinecraftServer server = level.getServer();
        ServerState state = STATES.get(server);
        if (state != null) {
            state.gaze.enforceStillnessBeforeEntityTick(server, living);
        }
    }

    private static void onEntityTickPost(EntityTickEvent.Post event) {
        if (!(event.getEntity() instanceof LivingEntity living)
                || !(living.level() instanceof ServerLevel level)) {
            return;
        }
        MinecraftServer server = level.getServer();
        ServerState state = STATES.get(server);
        if (state != null) {
            state.gaze.enforceStillnessAfterEntityTick(server, living);
        }
    }

    private static void onLivingChangeTarget(LivingChangeTargetEvent event) {
        if (!(event.getEntity() instanceof Mob mob)
                || !(mob.level() instanceof ServerLevel level)) {
            return;
        }
        LivingEntity proposedTarget = event.getNewAboutToBeSetTarget();
        if (proposedTarget == null) return;
        MinecraftServer server = level.getServer();
        ServerState state = STATES.get(server);
        if (state != null && state.sanctuary.blocksTargetChange(server, mob, proposedTarget)) {
            event.setCanceled(true);
        }
    }

    /** Actual post-mitigation health loss interrupts the physical body's active projection. */
    private static void onLivingDamagePost(LivingDamageEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || event.getNewDamage() <= 0.0F) {
            return;
        }
        MinecraftServer server = player.serverLevel().getServer();
        ServerState state = STATES.get(server);
        if (state != null) {
            closeAstralProjection(
                    server,
                    state,
                    player.getUUID(),
                    AstralSeveranceRuntime.CloseReason.BODY_DAMAGED);
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;
        settlePendingDeaths(server, state);
        expireAstralProjections(server, state, server.getTickCount());
        reconcileAstralAvatars(server, state);
        state.observation.tick(server);
        syncObservationViews(server, state);
        state.gaze.tick(server);
        state.sanctuary.tick(server);
    }

    private static void syncObservationViews(MinecraftServer server, ServerState state) {
        NoeticViewSyncService.dispatch(
                state.observations,
                state.viewTransitions,
                (viewerId, targetId) -> loadedBorrowedSightTargetId(server, viewerId, targetId),
                (viewerId, payload) -> {
                    ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
                    if (viewer != null) {
                        NoeticViewNetworkBridge.send(viewer, payload);
                    }
                });
    }

    private static OptionalInt loadedBorrowedSightTargetId(
            MinecraftServer server,
            UUID viewerId,
            UUID targetId
    ) {
        ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
        if (viewer == null) return OptionalInt.empty();
        Entity target = viewer.serverLevel().getEntity(targetId);
        if (!(target instanceof LivingEntity living) || !living.isAlive()) {
            return OptionalInt.empty();
        }
        return OptionalInt.of(living.getId());
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        clearLifecycleEntity(
                server,
                event.getEntity().getUUID(),
                NoeticObservationSession.CloseReason.VIEWER_LOGOUT);
    }

    private static void onPlayerChangedDimension(PlayerEvent.PlayerChangedDimensionEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        MinecraftServer server = player.serverLevel().getServer();
        ServerState state = STATES.get(server);
        if (state != null) {
            closeAstralProjection(
                    server,
                    state,
                    player.getUUID(),
                    AstralSeveranceRuntime.CloseReason.DIMENSION_CHANGED);
        }
    }

    /**
     * A LivingDeathEvent is not final while lower-priority resurrection listeners may still cancel it.
     * Queue only bounded loaded-only cleanup work; ServerTick.Post settles the final alive/dead state.
     */
    private static void onLivingDeath(LivingDeathEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        ServerState state = STATES.get(server);
        if (state == null) return;
        if (state.pendingDeaths.size() < NoeticSafetyCeilings.MAX_PENDING_DEATH_CLEANUPS) {
            state.pendingDeaths.add(event.getEntity().getUUID());
        }
    }

    private static void settlePendingDeaths(MinecraftServer server, ServerState state) {
        if (state.pendingDeaths.isEmpty()) return;
        Set<UUID> pending = new LinkedHashSet<>(state.pendingDeaths);
        state.pendingDeaths.clear();
        for (UUID entityId : pending) {
            LivingEntity entity = findLoadedLivingEntity(server, entityId);
            if (entity != null && entity.isAlive()) {
                continue;
            }
            clearLifecycleEntity(server, entityId, NoeticObservationSession.CloseReason.VIEWER_DEATH);
        }
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static void expireAstralProjections(MinecraftServer server, ServerState state, long nowTick) {
        for (AstralSeveranceRuntime.ActiveProjection projection : state.astral.activeProjections()) {
            if (nowTick >= projection.expiresAtTick()) {
                closeAstralProjection(
                        server,
                        state,
                        projection.casterId(),
                        AstralSeveranceRuntime.CloseReason.EXPIRED);
            }
        }
    }

    /**
     * Reconciles only the bounded active projection/map entries. It never scans chunks, levels or players.
     * Missing or mismatched representation fails closed by terminating the corresponding projection.
     */
    private static void reconcileAstralAvatars(MinecraftServer server, ServerState state) {
        for (AstralSeveranceRuntime.ActiveProjection projection : state.astral.activeProjections()) {
            AstralAvatarRef ref = state.astralAvatars.get(projection.casterId());
            if (!astralAvatarMatches(server, ref, projection.projectionId())) {
                closeAstralProjection(
                        server,
                        state,
                        projection.casterId(),
                        AstralSeveranceRuntime.CloseReason.AUTHORIZATION_REVOKED);
            }
        }
        for (UUID casterId : new ArrayList<>(state.astralAvatars.keySet())) {
            if (state.astral.projection(casterId).isEmpty()) {
                removeAstralAvatar(server, state, casterId);
            }
        }
    }

    private static boolean astralAvatarMatches(
            MinecraftServer server,
            AstralAvatarRef ref,
            UUID projectionId
    ) {
        if (ref == null || !ref.projectionId().equals(projectionId)) return false;
        ServerLevel level = server.getLevel(ref.dimension());
        if (level == null) return false;
        return level.getEntity(ref.entityId()) instanceof AstralProjectionEntity;
    }

    private static boolean syncAstralAvatarPose(
            MinecraftServer server,
            ServerState state,
            UUID casterId,
            AstralSeveranceRuntime.ActiveProjection projection
    ) {
        AstralAvatarRef ref = state.astralAvatars.get(casterId);
        if (ref == null || !ref.projectionId().equals(projection.projectionId())) return false;
        ServerLevel level = server.getLevel(ref.dimension());
        if (level == null) return false;
        Entity entity = level.getEntity(ref.entityId());
        if (!(entity instanceof AstralProjectionEntity avatar)) return false;
        applyAstralPose(avatar, projection.currentPose());
        return true;
    }

    private static void applyAstralPose(AstralProjectionEntity avatar, AstralProjectionPose pose) {
        avatar.setPos(pose.x(), pose.y(), pose.z());
        avatar.setYRot(pose.yaw());
        avatar.setXRot(pose.pitch());
    }

    private static boolean closeAstralProjection(
            MinecraftServer server,
            ServerState state,
            UUID casterId,
            AstralSeveranceRuntime.CloseReason reason
    ) {
        boolean closed = state.astral.close(casterId, reason);
        if (closed || state.astral.projection(casterId).isEmpty()) {
            removeAstralAvatar(server, state, casterId);
        }
        return closed;
    }

    private static boolean removeAstralAvatar(MinecraftServer server, ServerState state, UUID casterId) {
        AstralAvatarRef ref = state.astralAvatars.remove(casterId);
        if (ref == null) return false;
        ServerLevel level = server.getLevel(ref.dimension());
        if (level == null) return true;
        Entity entity = level.getEntity(ref.entityId());
        if (entity instanceof AstralProjectionEntity) {
            entity.discard();
        }
        return true;
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.remove(server);
        if (state == null) return;
        state.pendingDeaths.clear();
        for (UUID casterId : new ArrayList<>(state.astralAvatars.keySet())) {
            removeAstralAvatar(server, state, casterId);
        }
        state.astral.clearForServerStop();
        state.observation.clearForServerStop();
        state.gaze.clearForServerStop(server);
        state.sanctuary.clearForServerStop(server);
    }

    private static int clearLifecycleEntity(
            MinecraftServer server,
            UUID entityId,
            NoeticObservationSession.CloseReason viewerReason
    ) {
        ServerState state = STATES.get(server);
        if (state == null) return 0;
        state.pendingDeaths.remove(entityId);
        int changed = 0;
        if (state.observation.clearViewer(entityId, viewerReason)) changed++;
        changed += state.observation.clearTarget(entityId);
        AstralSeveranceRuntime.CloseReason astralReason = switch (viewerReason) {
            case VIEWER_LOGOUT -> AstralSeveranceRuntime.CloseReason.VIEWER_LOGOUT;
            case VIEWER_DEATH -> AstralSeveranceRuntime.CloseReason.BODY_DEATH;
            case SERVER_STOP -> AstralSeveranceRuntime.CloseReason.SERVER_STOP;
            case EXPLICIT, EXPIRED, TARGET_UNAVAILABLE, AUTHORIZATION_REVOKED ->
                    AstralSeveranceRuntime.CloseReason.AUTHORIZATION_REVOKED;
        };
        if (closeAstralProjection(server, state, entityId, astralReason)) changed++;
        changed += state.gaze.clearEntity(server, entityId);
        changed += state.sanctuary.clearEntity(server, entityId);
        return changed;
    }

    private static ServerState stateFor(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    public record AstralProjectionStart(
            ArcanaDecision decision,
            Optional<AstralSeveranceRuntime.ActiveProjection> projection
    ) {
        public AstralProjectionStart {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(projection, "projection");
            if (decision.allowed() != projection.isPresent()) {
                throw new IllegalArgumentException("Astral projection start result must pair allow with exactly one projection");
            }
        }

        private static AstralProjectionStart started(AstralSeveranceRuntime.ActiveProjection projection) {
            return new AstralProjectionStart(ArcanaDecision.allow(), Optional.of(projection));
        }

        private static AstralProjectionStart denied(String code, String detail) {
            return new AstralProjectionStart(ArcanaDecision.deny(code, detail), Optional.empty());
        }
    }

    private record AstralAvatarRef(
            UUID projectionId,
            ResourceKey<Level> dimension,
            int entityId
    ) {
        private AstralAvatarRef {
            Objects.requireNonNull(projectionId, "projectionId");
            Objects.requireNonNull(dimension, "dimension");
            if (entityId < 0) {
                throw new IllegalArgumentException("Astral avatar entity id must be non-negative");
            }
        }
    }

    private static final class ServerState {
        private final FamiliarOwnershipRegistry familiarOwnership =
                new FamiliarOwnershipRegistry(NoeticSafetyCeilings.MAX_FAMILIAR_PROVIDERS);
        private final NoeticObservationRuntime observations =
                new NoeticObservationRuntime(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);
        private final MinecraftNoeticObservationRuntime observation =
                new MinecraftNoeticObservationRuntime(observations, familiarOwnership);
        private final NoeticViewTransitionTracker viewTransitions =
                new NoeticViewTransitionTracker(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);
        private final AstralSeveranceRuntime astral =
                new AstralSeveranceRuntime(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);
        private final Map<UUID, AstralAvatarRef> astralAvatars = new LinkedHashMap<>();
        private final NullificationRegistry nullifications =
                new NullificationRegistry(NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES);
        private final MinecraftNoeticGazeRuntime gaze = new MinecraftNoeticGazeRuntime(nullifications);
        private final MinecraftPactSanctuaryRuntime sanctuary =
                new MinecraftPactSanctuaryRuntime(familiarOwnership);
        private final LinkedHashSet<UUID> pendingDeaths = new LinkedHashSet<>();
    }
}
