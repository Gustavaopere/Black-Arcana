package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.DivinationVisibilityPolicy;
import dev.gustavopere.blackarcana.content.noetic.FamiliarBondRegistry;
import dev.gustavopere.blackarcana.content.noetic.FamiliarSafetyCeilings;
import dev.gustavopere.blackarcana.network.BorrowedSightCameraPayload;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Server-authoritative lifecycle and ownership boundary for Borrowed Sight. */
public final class MinecraftBorrowedSightRuntime {
    private static final int ABSOLUTE_MAX_OWNERSHIP_PROVIDERS = 32;
    private static final UUID NO_TARGET = new UUID(0L, 0L);
    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    @FunctionalInterface
    public interface OwnershipProvider {
        boolean owns(UUID ownerId, Entity target);
    }

    private MinecraftBorrowedSightRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftBorrowedSightRuntime::onServerStarted);
        gameBus.addListener(MinecraftBorrowedSightRuntime::onServerTick);
        gameBus.addListener(MinecraftBorrowedSightRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftBorrowedSightRuntime::onServerStopped);
    }

    public static FamiliarBondRegistry.BindResult bindFamiliar(MinecraftServer server, UUID ownerId, UUID familiarId) {
        Objects.requireNonNull(server, "server");
        return state(server).bonds.bind(
            Objects.requireNonNull(ownerId, "ownerId"),
            Objects.requireNonNull(familiarId, "familiarId"));
    }

    public static boolean unbindFamiliar(MinecraftServer server, UUID ownerId, UUID familiarId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(familiarId, "familiarId");
        ServerState state = state(server);
        boolean removed = state.bonds.unbind(ownerId, familiarId);
        if (removed) maintain(server);
        return removed;
    }

    public static ArcanaDecision registerOwnershipProvider(MinecraftServer server, String providerId, OwnershipProvider provider) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(providerId, "providerId");
        Objects.requireNonNull(provider, "provider");
        if (providerId.isBlank() || providerId.length() > 128 || providerId.indexOf(':') <= 0) {
            return ArcanaDecision.deny("borrowed_sight_provider_id", "Borrowed Sight ownership provider id must be a bounded namespaced identifier");
        }
        ServerState state = state(server);
        synchronized (state) {
            if (!state.ownershipProviders.containsKey(providerId)
                    && state.ownershipProviders.size() >= ABSOLUTE_MAX_OWNERSHIP_PROVIDERS) {
                return ArcanaDecision.deny("borrowed_sight_provider_capacity", "Borrowed Sight ownership provider registry reached its bounded capacity");
            }
            state.ownershipProviders.put(providerId, provider);
        }
        return ArcanaDecision.allow();
    }

    public static BorrowedSightResult start(MinecraftServer server, UUID viewerId, UUID targetId, double maxRange, long durationTicks) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(targetId, "targetId");
        if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > FamiliarSafetyCeilings.MAX_SCRY_RANGE) {
            return BorrowedSightResult.denied("borrowed_sight_range_config", "Borrowed Sight range is outside the noetic safety ceiling");
        }
        if (durationTicks <= 0L || durationTicks > FamiliarSafetyCeilings.MAX_REMOTE_VIEW_TICKS) {
            return BorrowedSightResult.denied("borrowed_sight_duration_config", "Borrowed Sight duration is outside the noetic safety ceiling");
        }

        ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
        if (viewer == null || !viewer.isAlive()) {
            return BorrowedSightResult.denied("borrowed_sight_viewer_unavailable", "Borrowed Sight requires a loaded living server player");
        }
        Entity target = viewer.serverLevel().getEntity(targetId);
        if (target == null || !target.isAlive()) {
            return BorrowedSightResult.denied("borrowed_sight_target_unavailable", "Borrowed Sight requires a currently loaded target in the viewer dimension");
        }
        if (target instanceof Player) {
            return BorrowedSightResult.denied("borrowed_sight_player_policy", "Borrowed Sight player targets require a future explicit consenting-bond policy");
        }
        if (!(target instanceof LivingEntity)) {
            return BorrowedSightResult.denied("borrowed_sight_target_type", "Borrowed Sight requires a living familiar target");
        }

        ServerState state = state(server);
        if (!ownedBy(state, viewerId, target)) {
            return BorrowedSightResult.denied("borrowed_sight_ownership", "Borrowed Sight target is not owned by the viewer");
        }
        double distanceSquared = viewer.distanceToSqr(target);
        if (!Double.isFinite(distanceSquared)) {
            return BorrowedSightResult.denied("borrowed_sight_target_invalid", "Borrowed Sight target distance is not finite");
        }
        double distance = Math.sqrt(distanceSquared);
        if (distance > maxRange) {
            return BorrowedSightResult.denied("borrowed_sight_range", "Borrowed Sight target is outside configured range");
        }

        DivinationVisibilityPolicy visibility = new DivinationVisibilityPolicy(maxRange);
        if (!visibility.canBorrowSight(new DivinationVisibilityPolicy.Facts(true, true, false, false, true, distance))) {
            return BorrowedSightResult.denied("borrowed_sight_policy", "Borrowed Sight target was denied by the server visibility policy");
        }

        long expiresAt = saturatingAdd(server.overworld().getGameTime(), durationTicks);
        synchronized (state) {
            state.sessions.put(viewerId, new Session(targetId, maxRange, expiresAt));
        }
        ArcanaNetworkBridge.sendBorrowedSightCamera(viewer, BorrowedSightCameraPayload.start(target.getId(), targetId));
        return new BorrowedSightResult(ArcanaDecision.allow(), true, targetId);
    }

    public static boolean stop(MinecraftServer server, UUID viewerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        boolean removed;
        synchronized (state) {
            removed = state.sessions.remove(viewerId) != null;
        }
        if (!removed) return false;
        ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
        if (viewer != null) ArcanaNetworkBridge.sendBorrowedSightCamera(viewer, BorrowedSightCameraPayload.reset());
        return true;
    }

    public static boolean isActive(MinecraftServer server, UUID viewerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(viewerId, "viewerId");
        maintain(server);
        ServerState state = STATES.get(server);
        if (state == null) return false;
        synchronized (state) {
            return state.sessions.containsKey(viewerId);
        }
    }

    public static void maintain(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        if (state == null) return;
        long now = server.overworld().getGameTime();
        List<UUID> invalid = new ArrayList<>();
        List<Map.Entry<UUID, Session>> snapshot;
        synchronized (state) {
            snapshot = List.copyOf(state.sessions.entrySet());
        }
        for (Map.Entry<UUID, Session> entry : snapshot) {
            UUID viewerId = entry.getKey();
            Session session = entry.getValue();
            ServerPlayer viewer = server.getPlayerList().getPlayer(viewerId);
            if (viewer == null || !viewer.isAlive() || now >= session.expiresAtTick()) {
                invalid.add(viewerId);
                continue;
            }
            Entity target = viewer.serverLevel().getEntity(session.targetId());
            if (target == null || !target.isAlive() || target instanceof Player || !(target instanceof LivingEntity)) {
                invalid.add(viewerId);
                continue;
            }
            if (!ownedBy(state, viewerId, target)) {
                invalid.add(viewerId);
                continue;
            }
            double distanceSquared = viewer.distanceToSqr(target);
            if (!Double.isFinite(distanceSquared) || distanceSquared > session.maxRange() * session.maxRange()) invalid.add(viewerId);
        }
        invalid.forEach(viewerId -> stop(server, viewerId));
    }

    private static boolean ownedBy(ServerState state, UUID ownerId, Entity target) {
        if (state.bonds.isOwnedBy(target.getUUID(), ownerId)) return true;
        List<OwnershipProvider> providers;
        synchronized (state) {
            providers = List.copyOf(state.ownershipProviders.values());
        }
        for (OwnershipProvider provider : providers) {
            try {
                if (provider.owns(ownerId, target)) return true;
            } catch (RuntimeException | LinkageError ignored) {
                // Optional provider failure never grants authority.
            }
        }
        return false;
    }

    private static ServerState state(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    private static void onServerStarted(ServerStartedEvent event) { state(event.getServer()); }
    private static void onServerTick(ServerTickEvent.Post event) { maintain(event.getServer()); }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        if (event.getEntity() instanceof ServerPlayer player) stop(player.serverLevel().getServer(), player.getUUID());
    }

    private static void onServerStopped(ServerStoppedEvent event) { STATES.remove(event.getServer()); }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    private static final class ServerState {
        private final FamiliarBondRegistry bonds = new FamiliarBondRegistry(FamiliarSafetyCeilings.MAX_FAMILIARS_PER_OWNER);
        private final Map<String, OwnershipProvider> ownershipProviders = new LinkedHashMap<>();
        private final Map<UUID, Session> sessions = new LinkedHashMap<>();
    }

    private record Session(UUID targetId, double maxRange, long expiresAtTick) {
        private Session {
            Objects.requireNonNull(targetId, "targetId");
            if (!Double.isFinite(maxRange) || maxRange <= 0.0D) throw new IllegalArgumentException("maxRange must be finite and positive");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
        }
    }

    public record BorrowedSightResult(ArcanaDecision decision, boolean active, UUID targetId) {
        public BorrowedSightResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(targetId, "targetId");
            if (!decision.allowed() && active) throw new IllegalArgumentException("denied Borrowed Sight cannot be active");
        }

        private static BorrowedSightResult denied(String code, String detail) {
            return new BorrowedSightResult(ArcanaDecision.deny(code, detail), false, NO_TARGET);
        }
    }
}
