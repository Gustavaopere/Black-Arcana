package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.ThroughputWindow;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Server-authoritative Threshold Gate registry and transfer boundary.
 *
 * Host integrations (for example Ars) own threshold presentation/detection and submit explicit
 * paired endpoints. Black Arcana owns pair identity/ownership, loaded-destination validation,
 * player consent, throughput and the actual movement of an existing entity. This class never
 * force-loads chunks and never moves blocks/block entities.
 */
public final class MinecraftThresholdGateRuntime {
    private static final int MAX_GATE_PAIRS_PER_SERVER = 4096;
    private static final int MAX_DIMENSION_ID_LENGTH = 160;

    private static final Map<MinecraftServer, State> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftThresholdGateRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftThresholdGateRuntime::onServerStopped);
    }

    public static ArcanaDecision registerPair(
            MinecraftServer server,
            UUID gateId,
            UUID ownerId,
            String dimensionId,
            double ax,
            double ay,
            double az,
            double bx,
            double by,
            double bz,
            int maxPerSecond
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(gateId, "gateId");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(dimensionId, "dimensionId");

        if (!validDimensionId(dimensionId)) {
            return ArcanaDecision.deny("threshold_gate_dimension", "Gate dimension id is invalid or unbounded");
        }
        if (!finite(ax, ay, az) || !finite(bx, by, bz)) {
            return ArcanaDecision.deny("threshold_gate_position", "Gate endpoints must use finite coordinates");
        }
        if (maxPerSecond <= 0 || maxPerSecond > LiminalSafetyCeilings.MAX_GATE_THROUGHPUT_PER_SECOND) {
            return ArcanaDecision.deny("threshold_gate_throughput_config", "Gate throughput is outside the hard Liminal ceiling");
        }
        if (ax == bx && ay == by && az == bz) {
            return ArcanaDecision.deny("threshold_gate_same_endpoint", "Gate endpoints must be distinct");
        }

        State state = state(server);
        synchronized (state) {
            if (!state.pairs.containsKey(gateId) && state.pairs.size() >= MAX_GATE_PAIRS_PER_SERVER) {
                return ArcanaDecision.deny("threshold_gate_pair_capacity", "Server gate-pair capacity is full");
            }
            state.pairs.put(
                gateId,
                new GatePair(
                    gateId,
                    ownerId,
                    dimensionId,
                    new Endpoint(ax, ay, az),
                    new Endpoint(bx, by, bz),
                    new ThroughputWindow(maxPerSecond)));
        }
        return ArcanaDecision.allow();
    }

    public static TransferResult transfer(
            MinecraftServer server,
            UUID gateId,
            UUID requestingOwnerId,
            int sourceIndex,
            UUID entityId,
            long nowTick,
            boolean playerConsent
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(gateId, "gateId");
        Objects.requireNonNull(requestingOwnerId, "requestingOwnerId");
        Objects.requireNonNull(entityId, "entityId");
        if (sourceIndex != 0 && sourceIndex != 1) {
            return TransferResult.denied("threshold_gate_source", "Gate source index must be 0 or 1");
        }
        if (nowTick < 0L) {
            return TransferResult.denied("threshold_gate_time", "Gate transfer tick must be non-negative");
        }

        State state = STATES.get(server);
        if (state == null) {
            return TransferResult.denied("threshold_gate_missing", "Threshold Gate pair is not registered");
        }

        final GatePair pair;
        synchronized (state) {
            pair = state.pairs.get(gateId);
        }
        if (pair == null) {
            return TransferResult.denied("threshold_gate_missing", "Threshold Gate pair is not registered");
        }
        if (!pair.ownerId().equals(requestingOwnerId)) {
            return TransferResult.denied("threshold_gate_owner_mismatch", "Gate owner context does not match the registered pair");
        }

        ServerPlayer gateOwner = server.getPlayerList().getPlayer(pair.ownerId());
        if (gateOwner == null || !gateOwner.isAlive()) {
            return TransferResult.denied("threshold_gate_owner_unavailable", "Registered gate owner must be loaded and alive");
        }

        LoadedEntity loaded = findLoadedEntity(server, entityId);
        if (loaded == null || !(loaded.entity() instanceof LivingEntity living) || !living.isAlive()) {
            return TransferResult.denied("threshold_gate_entity_ineligible", "Threshold Gate only moves loaded eligible living entities");
        }
        if (!loaded.level().dimension().location().toString().equals(pair.dimensionId())) {
            return TransferResult.denied("dimension_denied", "Entity is not in the registered gate dimension");
        }
        if (living instanceof ServerPlayer player
                && !player.getUUID().equals(pair.ownerId())
                && !playerConsent) {
            return TransferResult.denied("threshold_gate_player_consent", "Moving another player requires explicit host/server consent");
        }

        Endpoint destination = sourceIndex == 0 ? pair.second() : pair.first();
        ServerLevel destinationLevel = findLoadedLevel(server, pair.dimensionId());
        if (destinationLevel == null) {
            return TransferResult.denied("destination_unloaded", "Registered gate dimension is not loaded");
        }

        MinecraftSafeDestinationResolver.Result firstCheck = MinecraftSafeDestinationResolver.evaluate(
            server,
            living,
            destinationLevel,
            destination.x(),
            destination.y(),
            destination.z());
        if (!firstCheck.allowed()) {
            return TransferResult.denied(firstCheck.code(), "Threshold Gate destination failed safe-destination validation");
        }

        // Immediate revalidation before consuming throughput or mutating position.
        LoadedEntity settlement = findLoadedEntity(server, entityId);
        if (settlement == null
                || settlement.entity() != living
                || settlement.level() != loaded.level()
                || !living.isAlive()) {
            return TransferResult.denied("threshold_gate_entity_changed", "Gate entity changed before transfer settlement");
        }
        MinecraftSafeDestinationResolver.Result settlementCheck = MinecraftSafeDestinationResolver.evaluate(
            server,
            living,
            destinationLevel,
            destination.x(),
            destination.y(),
            destination.z());
        if (!settlementCheck.allowed()) {
            return TransferResult.denied(settlementCheck.code(), "Threshold Gate destination changed before settlement");
        }

        synchronized (state) {
            if (STATES.get(server) != state || state.pairs.get(gateId) != pair) {
                return TransferResult.denied("threshold_gate_pair_changed", "Gate pair changed before transfer settlement");
            }
            if (!pair.throughput().tryAcquire(pair.ownerId(), nowTick)) {
                return TransferResult.denied("threshold_gate_throughput", "Gate throughput is exhausted for this window");
            }
        }

        try {
            living.setPos(destination.x(), destination.y(), destination.z());
        } catch (RuntimeException movementFailure) {
            return TransferResult.denied("threshold_gate_settlement_failed", "Gate movement could not be settled");
        }
        return TransferResult.allowedResult();
    }

    private static State state(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new State());
        }
    }

    private static LoadedEntity findLoadedEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity != null) return new LoadedEntity(level, entity);
        }
        return null;
    }

    private static ServerLevel findLoadedLevel(MinecraftServer server, String dimensionId) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dimensionId)) return level;
        }
        return null;
    }

    private static boolean finite(double x, double y, double z) {
        return Double.isFinite(x) && Double.isFinite(y) && Double.isFinite(z);
    }

    private static boolean validDimensionId(String dimensionId) {
        String normalized = dimensionId.trim();
        if (normalized.isEmpty() || normalized.length() > MAX_DIMENSION_ID_LENGTH) return false;
        for (int i = 0; i < normalized.length(); i++) {
            if (Character.isISOControl(normalized.charAt(i))) return false;
        }
        return true;
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private record LoadedEntity(ServerLevel level, Entity entity) {
        private LoadedEntity {
            Objects.requireNonNull(level, "level");
            Objects.requireNonNull(entity, "entity");
        }
    }

    private record Endpoint(double x, double y, double z) {
        private Endpoint {
            if (!finite(x, y, z)) throw new IllegalArgumentException("Gate endpoint must be finite");
        }
    }

    private record GatePair(
        UUID gateId,
        UUID ownerId,
        String dimensionId,
        Endpoint first,
        Endpoint second,
        ThroughputWindow throughput
    ) {
        private GatePair {
            Objects.requireNonNull(gateId, "gateId");
            Objects.requireNonNull(ownerId, "ownerId");
            Objects.requireNonNull(dimensionId, "dimensionId");
            Objects.requireNonNull(first, "first");
            Objects.requireNonNull(second, "second");
            Objects.requireNonNull(throughput, "throughput");
        }
    }

    public record TransferResult(ArcanaDecision decision, boolean transferred) {
        public TransferResult {
            Objects.requireNonNull(decision, "decision");
            if (!decision.allowed() && transferred) {
                throw new IllegalArgumentException("denied Threshold Gate transfer cannot report movement");
            }
        }

        private static TransferResult allowedResult() {
            return new TransferResult(ArcanaDecision.allow(), true);
        }

        private static TransferResult denied(String code, String detail) {
            return new TransferResult(ArcanaDecision.deny(code, detail), false);
        }
    }

    private static final class State {
        private final Map<UUID, GatePair> pairs = new LinkedHashMap<>();
    }
}
