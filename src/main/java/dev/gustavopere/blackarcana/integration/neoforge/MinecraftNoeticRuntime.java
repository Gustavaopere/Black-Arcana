package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationSession;
import dev.gustavopere.blackarcana.content.noetic.NoeticPerceptionSnapshot;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.NullificationRegistry;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
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
        gameBus.addListener(MinecraftNoeticRuntime::onServerTick);
        gameBus.addListener(MinecraftNoeticRuntime::onPlayerLoggedOut);
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
        return activeObservations(server) + activeGazes(server) + activeSanctuaries(server);
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

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;
        state.observation.tick(server);
        state.gaze.tick(server);
        state.sanctuary.tick(server);
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        clearLifecycleEntity(
                server,
                event.getEntity().getUUID(),
                NoeticObservationSession.CloseReason.VIEWER_LOGOUT);
    }

    private static void onLivingDeath(LivingDeathEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        clearLifecycleEntity(
                server,
                event.getEntity().getUUID(),
                NoeticObservationSession.CloseReason.VIEWER_DEATH);
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.remove(server);
        if (state == null) return;
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
        int changed = 0;
        if (state.observation.clearViewer(entityId, viewerReason)) changed++;
        changed += state.observation.clearTarget(entityId);
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

    private static final class ServerState {
        private final FamiliarOwnershipRegistry familiarOwnership =
                new FamiliarOwnershipRegistry(NoeticSafetyCeilings.MAX_FAMILIAR_PROVIDERS);
        private final NoeticObservationRuntime observations =
                new NoeticObservationRuntime(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);
        private final MinecraftNoeticObservationRuntime observation =
                new MinecraftNoeticObservationRuntime(observations, familiarOwnership);
        private final NullificationRegistry nullifications =
                new NullificationRegistry(NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES);
        private final MinecraftNoeticGazeRuntime gaze = new MinecraftNoeticGazeRuntime(nullifications);
        private final MinecraftPactSanctuaryRuntime sanctuary =
                new MinecraftPactSanctuaryRuntime(familiarOwnership);
    }
}
