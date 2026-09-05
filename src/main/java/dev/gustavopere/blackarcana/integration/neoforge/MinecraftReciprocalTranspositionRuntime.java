package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.ReciprocalTranspositionPlanner;
import dev.gustavopere.blackarcana.content.space.SafeDestinationPolicy;
import dev.gustavopere.blackarcana.content.space.ThroughputWindow;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.Tags;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

public final class MinecraftReciprocalTranspositionRuntime {
    private static final SafeDestinationPolicy DESTINATION_POLICY = new SafeDestinationPolicy();
    private static final ReciprocalTranspositionPlanner PLANNER = new ReciprocalTranspositionPlanner(DESTINATION_POLICY);
    private static final Map<MinecraftServer, State> STATES = Collections.synchronizedMap(new IdentityHashMap<>());
    private MinecraftReciprocalTranspositionRuntime() { }

    public static void register(IEventBus gameBus) { Objects.requireNonNull(gameBus, "gameBus"); gameBus.addListener(MinecraftReciprocalTranspositionRuntime::onServerStopped); }

    public static ArcanaDecision configureThroughput(MinecraftServer server, int maxPerSecond) {
        Objects.requireNonNull(server, "server");
        if (maxPerSecond <= 0 || maxPerSecond > LiminalSafetyCeilings.MAX_TRANSPOSITIONS_PER_SECOND) return ArcanaDecision.deny("transposition_throughput_config", "Reciprocal Transposition throughput is outside the hard Liminal ceiling");
        synchronized (STATES) { STATES.put(server, new State(new ThroughputWindow(maxPerSecond))); }
        return ArcanaDecision.allow();
    }

    public static long snapshotVersion(MinecraftServer server, UUID entityId) {
        Objects.requireNonNull(server, "server"); Objects.requireNonNull(entityId, "entityId");
        Endpoint endpoint = findLoadedEndpoint(server, entityId); return endpoint == null ? -1L : fingerprint(endpoint.entity(), endpoint.level());
    }

    public static SwapResult swap(MinecraftServer server, UUID ownerId, UUID firstEntityId, UUID secondEntityId,
            long firstVersion, long secondVersion, long nowTick, boolean firstConsent, boolean secondConsent) {
        Objects.requireNonNull(server, "server"); Objects.requireNonNull(ownerId, "ownerId"); Objects.requireNonNull(firstEntityId, "firstEntityId"); Objects.requireNonNull(secondEntityId, "secondEntityId");
        if (nowTick < 0L || firstVersion < 0L || secondVersion < 0L) return SwapResult.denied("transposition_invalid_snapshot", "Endpoint versions and tick must be non-negative");
        if (firstEntityId.equals(secondEntityId)) return SwapResult.denied("same_entity", "Reciprocal Transposition requires two distinct endpoints");
        ServerPlayer owner = server.getPlayerList().getPlayer(ownerId);
        if (owner == null || !owner.isAlive()) return SwapResult.denied("transposition_owner_unavailable", "Caster must be loaded and alive");
        State state = STATES.get(server);
        if (state == null) return SwapResult.denied("transposition_throughput_unconfigured", "Reciprocal Transposition throughput policy is not configured");
        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) return SwapResult.denied("transposition_runtime_unavailable", "Black Arcana server runtime is unavailable");
        Endpoint first = findLoadedEndpoint(server, firstEntityId); Endpoint second = findLoadedEndpoint(server, secondEntityId);
        if (!eligible(first) || !eligible(second)) return SwapResult.denied("transposition_endpoint_unavailable", "Both endpoints must be loaded eligible entities");
        if (first.level() != second.level()) return SwapResult.denied("dimension_mismatch", "Reciprocal Transposition endpoints must share one loaded dimension");
        if (fingerprint(first.entity(), first.level()) != firstVersion || fingerprint(second.entity(), second.level()) != secondVersion) return SwapResult.denied("transposition_endpoint_changed", "An endpoint changed after the host captured its transaction snapshot");
        Position firstPosition = Position.capture(first.entity()); Position secondPosition = Position.capture(second.entity());
        SafeDestinationPolicy.Facts firstLocationForSecond = destinationFacts(server, runtime, ownerId, second.entity(), first.entity(), first.level(), firstPosition);
        SafeDestinationPolicy.Facts secondLocationForFirst = destinationFacts(server, runtime, ownerId, first.entity(), second.entity(), second.level(), secondPosition);
        ReciprocalTranspositionPlanner.Plan plan = PLANNER.plan(new ReciprocalTranspositionPlanner.Endpoint(firstEntityId, firstVersion, firstConsent, firstLocationForSecond), new ReciprocalTranspositionPlanner.Endpoint(secondEntityId, secondVersion, secondConsent, secondLocationForFirst));
        if (!plan.allowed()) return SwapResult.denied(plan.code(), "Reciprocal Transposition planner denied the transaction");
        Endpoint settlementFirst = findLoadedEndpoint(server, firstEntityId); Endpoint settlementSecond = findLoadedEndpoint(server, secondEntityId);
        if (settlementFirst == null || settlementSecond == null || settlementFirst.entity() != first.entity() || settlementSecond.entity() != second.entity() || settlementFirst.level() != first.level() || settlementSecond.level() != second.level() || fingerprint(settlementFirst.entity(), settlementFirst.level()) != plan.firstVersion() || fingerprint(settlementSecond.entity(), settlementSecond.level()) != plan.secondVersion()) return SwapResult.denied("transposition_endpoint_changed", "An endpoint changed before Reciprocal Transposition settlement");
        SafeDestinationPolicy.Facts settlementFirstLocationForSecond = destinationFacts(server, runtime, ownerId, second.entity(), first.entity(), first.level(), firstPosition);
        SafeDestinationPolicy.Facts settlementSecondLocationForFirst = destinationFacts(server, runtime, ownerId, first.entity(), second.entity(), second.level(), secondPosition);
        ReciprocalTranspositionPlanner.Plan settlementPlan = PLANNER.plan(new ReciprocalTranspositionPlanner.Endpoint(firstEntityId, plan.firstVersion(), firstConsent, settlementFirstLocationForSecond), new ReciprocalTranspositionPlanner.Endpoint(secondEntityId, plan.secondVersion(), secondConsent, settlementSecondLocationForFirst));
        if (!settlementPlan.allowed()) return SwapResult.denied(settlementPlan.code(), "Reciprocal Transposition destination changed before settlement");
        synchronized (state) {
            if (STATES.get(server) != state) return SwapResult.denied("transposition_throughput_changed", "Throughput policy changed before Reciprocal Transposition settlement");
            if (!state.throughput.tryAcquire(ownerId, nowTick)) return SwapResult.denied("transposition_throughput", "Reciprocal Transposition throughput is exhausted for this owner/window");
        }
        try { first.entity().setPos(secondPosition.x(), secondPosition.y(), secondPosition.z()); second.entity().setPos(firstPosition.x(), firstPosition.y(), firstPosition.z()); }
        catch (RuntimeException settlementFailure) {
            try { first.entity().setPos(firstPosition.x(), firstPosition.y(), firstPosition.z()); } catch (RuntimeException ignored) { }
            try { second.entity().setPos(secondPosition.x(), secondPosition.y(), secondPosition.z()); } catch (RuntimeException ignored) { }
            return SwapResult.denied("transposition_settlement_failed", "Reciprocal Transposition movement could not be settled atomically");
        }
        return SwapResult.allowedResult();
    }

    private static boolean eligible(Endpoint endpoint) { if (endpoint == null || endpoint.entity().isRemoved()) return false; Entity e = endpoint.entity(); return !e.getType().is(Tags.EntityTypes.TELEPORTING_NOT_SUPPORTED) && !e.isPassenger() && !e.isVehicle(); }
    private static SafeDestinationPolicy.Facts destinationFacts(MinecraftServer server, ArcanaServerRuntime runtime, UUID ownerId, Entity mover, Entity counterpartLeavingDestination, ServerLevel level, Position destination) {
        BlockPos landing = BlockPos.containing(destination.x(), destination.y(), destination.z());
        boolean loaded = level.getChunkSource().getChunkNow(landing.getX() >> 4, landing.getZ() >> 4) != null;
        AABB landingBox = mover.getBoundingBox().move(destination.x() - mover.getX(), destination.y() - mover.getY(), destination.z() - mover.getZ());
        boolean border = level.getWorldBorder().isWithinBounds(landingBox);
        boolean blockCollisionFree = loaded && level.noBlockCollision(mover, landingBox);
        boolean thirdEntityCollisionFree = loaded && level.getEntities(mover, landingBox, candidate -> candidate != counterpartLeavingDestination && !candidate.isRemoved()).isEmpty();
        boolean collisionFree = blockCollisionFree && thirdEntityCollisionFree;
        boolean fluidAllowed = loaded && level.getFluidState(landing).isEmpty() && level.getFluidState(landing.above()).isEmpty();
        boolean vehicleUnsafe = mover.isPassenger() || mover.isVehicle();
        boolean protectionAllowed = false;
        if (loaded) {
            var guard = runtime.protectedDestinationGuard().orElse(null);
            if (guard != null) {
                String dimensionId = level.dimension().location().toString();
                ArcanaDecision protection = guard.authorize(new ChunkRef(dimensionId, landing.getX() >> 4, landing.getZ() >> 4), new ProtectionQuery(ownerId, dimensionId, mover.getUUID().toString(), EntityInteractionType.DISPLACEMENT));
                protectionAllowed = protection.allowed();
            }
        }
        return new SafeDestinationPolicy.Facts(loaded, border, collisionFree, collisionFree, fluidAllowed, true, protectionAllowed, vehicleUnsafe);
    }
    private static Endpoint findLoadedEndpoint(MinecraftServer server, UUID entityId) { for (ServerLevel level : server.getAllLevels()) { Entity entity = level.getEntity(entityId); if (entity != null) return new Endpoint(level, entity); } return null; }
    private static long fingerprint(Entity entity, ServerLevel level) { long hash = 0xcbf29ce484222325L; hash = mix(hash, entity.getUUID().getMostSignificantBits()); hash = mix(hash, entity.getUUID().getLeastSignificantBits()); hash = mix(hash, level.dimension().location().hashCode()); hash = mix(hash, Double.doubleToLongBits(entity.getX())); hash = mix(hash, Double.doubleToLongBits(entity.getY())); hash = mix(hash, Double.doubleToLongBits(entity.getZ())); hash = mix(hash, entity.isRemoved() ? 1L : 0L); return hash & Long.MAX_VALUE; }
    private static long mix(long current, long value) { return (current ^ value) * 0x100000001b3L; }
    private static void onServerStopped(ServerStoppedEvent event) { STATES.remove(event.getServer()); }
    private record Endpoint(ServerLevel level, Entity entity) { private Endpoint { Objects.requireNonNull(level, "level"); Objects.requireNonNull(entity, "entity"); } }
    private record Position(double x, double y, double z) { private Position { if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) throw new IllegalArgumentException("Reciprocal Transposition position must be finite"); } private static Position capture(Entity entity) { return new Position(entity.getX(), entity.getY(), entity.getZ()); } }
    public record SwapResult(ArcanaDecision decision, boolean swapped) { public SwapResult { Objects.requireNonNull(decision, "decision"); if (!decision.allowed() && swapped) throw new IllegalArgumentException("denied Reciprocal Transposition cannot report a completed swap"); } private static SwapResult allowedResult() { return new SwapResult(ArcanaDecision.allow(), true); } private static SwapResult denied(String code, String detail) { return new SwapResult(ArcanaDecision.deny(code, detail), false); } }
    private static final class State { private final ThroughputWindow throughput; private State(ThroughputWindow throughput) { this.throughput = Objects.requireNonNull(throughput, "throughput"); } }
}
