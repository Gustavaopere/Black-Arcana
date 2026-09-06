package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreCell;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreDomainSpecifications;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreFrontierScheduler;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectOverride;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfile;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Server-authoritative Black Pyre damage and protected terrain ignition boundary. */
public final class MinecraftBlackPyreRuntime {
    /** Technical ceiling only. Stage 08 may tune below this value. */
    public static final double ABSOLUTE_MAX_RAW_DAMAGE = 100.0D;
    public static final long DEFAULT_TEMPORARY_LIFETIME_TICKS = BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS;

    private static final String TERRAIN_NOT_REQUESTED = "terrain_not_requested";
    private static final String COSMETIC_ONLY = "black_pyre_cosmetic_only";
    private static final String WORLD_EFFECT_OFF = "black_pyre_world_effect_off";
    private static final String WORLD_BACKEND_UNAVAILABLE = "black_pyre_world_backend_unavailable";
    private static final String CHUNK_UNLOADED = "world_chunk_unloaded";
    private static final String FRONTIER_CAPACITY = "black_pyre_frontier_capacity";

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    /**
     * Internal world-safety descriptor only. Provider-facing mana/cooldown/progression settlement remains
     * upstream; this definition exists so every terrain write is admitted by the canonical Stage 04 gates.
     */
    private static final ArcanaSpellDefinition WORLD_SAFETY_SPELL = new ArcanaSpellDefinition(
        BlackPyreDomainSpecifications.BLACK_PYRE,
        "spell.black_arcana.black_pyre",
        "black_arcana:black_pyre",
        ArcanaCost.none(),
        true);

    private MinecraftBlackPyreRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        ArcanaServerRuntimeManager.addInitializer(MinecraftBlackPyreRuntime::installWorldProfile);
        gameBus.addListener(MinecraftBlackPyreRuntime::onServerStarted);
        gameBus.addListener(MinecraftBlackPyreRuntime::onServerTick);
        gameBus.addListener(MinecraftBlackPyreRuntime::onServerStopped);
    }

    private static void onServerStarted(ServerStartedEvent event) {
        STATES.put(event.getServer(), new ServerState());
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        tickFrontiers(event.getServer(), event.getServer().overworld().getGameTime());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        ServerState removed = STATES.remove(event.getServer());
        if (removed == null) return;
        synchronized (removed) {
            removed.scheduler.clear();
            removed.contexts.clear();
        }
    }

    private static void installWorldProfile(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        if (runtime.worldEffectProfiles().find(BlackPyreDomainSpecifications.BLACK_PYRE).isPresent()) return;
        runtime.worldEffectProfiles().register(
            BlackPyreDomainSpecifications.BLACK_PYRE,
            new WorldEffectProfile(
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT,
                BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER,
                true));
    }

    public static BlackPyreResult igniteDefault(
        MinecraftServer server,
        UUID casterId,
        List<UUID> targetIds,
        double requestedDamage,
        boolean terrainRequested,
        int seedX,
        int seedY,
        int seedZ
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetIds, "targetIds");
        ArcanaCastId castId = ArcanaCastId.random();

        if (!Double.isFinite(requestedDamage) || requestedDamage <= 0.0D) {
            return BlackPyreResult.denied(
                castId,
                "black_pyre_invalid_damage",
                "Requested Black Pyre damage must be finite and positive",
                terrainRequested ? WORLD_EFFECT_OFF : TERRAIN_NOT_REQUESTED);
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return BlackPyreResult.denied(
                castId,
                "black_pyre_caster_unavailable",
                "Black Pyre caster must be a loaded living server entity",
                terrainRequested ? WORLD_EFFECT_OFF : TERRAIN_NOT_REQUESTED);
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return BlackPyreResult.denied(
                castId,
                "black_pyre_runtime_unavailable",
                "Black Arcana server runtime is unavailable",
                terrainRequested ? WORLD_BACKEND_UNAVAILABLE : TERRAIN_NOT_REQUESTED);
        }

        DamageSettlement damage = settleEntityDamage(runtime, server, level, caster, targetIds, requestedDamage);
        TerrainSettlement terrain = terrainRequested
            ? settleSeed(server, runtime, level, casterId, castId, new BlockPos(seedX, seedY, seedZ))
            : TerrainSettlement.notApplied(TERRAIN_NOT_REQUESTED, ArcanaDecision.allow());

        ArcanaDecision overall;
        if (damage.damagedTargets() > 0 || terrain.applied()) {
            overall = ArcanaDecision.allow();
        } else if (!damage.decision().allowed()) {
            overall = damage.decision();
        } else {
            overall = terrain.decision();
        }

        return new BlackPyreResult(
            castId,
            overall,
            damage.damagedTargets(),
            damage.damageDealt(),
            terrain.applied(),
            terrain.code(),
            terrain.cells());
    }

    public static int activeFrontiers(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        if (state == null) return 0;
        synchronized (state) {
            return state.scheduler.activeFrontiers();
        }
    }

    public static boolean isFrontierActive(MinecraftServer server, ArcanaCastId castId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(castId, "castId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        UUID frontierId = castId.value();
        synchronized (state) {
            return state.contexts.containsKey(frontierId) && state.scheduler.seenCells(frontierId) > 0;
        }
    }

    /**
     * Drives only ephemeral propagation state. All world settlement remains delegated to the Stage 04
     * gateways and temporary restoration persistence remains owned by the canonical world-safety runtime.
     */
    public static void tickFrontiers(MinecraftServer server, long nowTick) {
        Objects.requireNonNull(server, "server");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        ServerState state = STATES.get(server);
        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (state == null || runtime == null) return;

        List<UUID> frontierIds;
        synchronized (state) {
            frontierIds = List.copyOf(state.contexts.keySet());
        }

        for (UUID frontierId : frontierIds) {
            FrontierContext context;
            synchronized (state) {
                context = state.contexts.get(frontierId);
            }
            if (context == null) continue;

            ServerLevel level = findLevel(server, context.dimensionId());
            LivingEntity caster = findLoadedLivingEntity(server, context.casterId());
            if (level == null || caster == null || !caster.isAlive() || caster.level() != level) {
                finishFrontier(state, frontierId);
                continue;
            }

            WorldEffectMode mode = effectiveMode(runtime);
            if (mode == WorldEffectMode.OFF || mode == WorldEffectMode.COSMETIC) {
                finishFrontier(state, frontierId);
                continue;
            }

            List<BlackPyreCell> admitted;
            synchronized (state) {
                admitted = state.scheduler.tick(frontierId, nowTick, cell -> isLoaded(level, cell));
                if (state.scheduler.seenCells(frontierId) == 0) {
                    state.contexts.remove(frontierId);
                    continue;
                }
            }

            List<BlackPyreCell> nextCandidates = new ArrayList<>();
            for (BlackPyreCell cell : admitted) {
                BlockPos pos = new BlockPos(cell.x(), cell.y(), cell.z());
                if (!isSpreadableLoadedCell(level, pos)) continue;
                TerrainSettlement settlement = settleCell(
                    runtime,
                    level,
                    context.casterId(),
                    context.castId(),
                    pos,
                    context.expiresAtTick());
                if (settlement.applied()) {
                    nextCandidates.addAll(spreadableNeighbors(level, cell));
                }
            }

            synchronized (state) {
                if (!nextCandidates.isEmpty()) {
                    state.scheduler.offer(frontierId, nextCandidates);
                }
                if (state.scheduler.pendingCells(frontierId) == 0) {
                    state.scheduler.finish(frontierId);
                    state.contexts.remove(frontierId);
                }
            }
        }
    }

    private static DamageSettlement settleEntityDamage(
        ArcanaServerRuntime runtime,
        MinecraftServer server,
        ServerLevel level,
        LivingEntity caster,
        List<UUID> targetIds,
        double requestedDamage
    ) {
        if (!entityDamageAllowed(runtime)) {
            return new DamageSettlement(
                ArcanaDecision.deny("world_entity_damage_disabled", "Entity damage is disabled for Black Pyre"),
                0,
                0.0D);
        }

        Set<UUID> uniqueTargets = new LinkedHashSet<>();
        for (UUID targetId : targetIds) {
            if (targetId == null || targetId.equals(caster.getUUID())) continue;
            uniqueTargets.add(targetId);
            if (uniqueTargets.size() >= ArcanaTargetSpec.ABSOLUTE_MAX_TARGETS) break;
        }
        if (uniqueTargets.isEmpty()) {
            return new DamageSettlement(
                ArcanaDecision.deny("black_pyre_no_targets", "No distinct Black Pyre target identities were supplied"),
                0,
                0.0D);
        }

        double boundedDamage = Math.min(requestedDamage, ABSOLUTE_MAX_RAW_DAMAGE);
        int damagedTargets = 0;
        double totalDamageDealt = 0.0D;
        for (UUID targetId : uniqueTargets) {
            LivingEntity target = findLoadedLivingEntity(server, targetId);
            if (target == null || !target.isAlive() || target.level() != level) continue;

            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization authorization = authorizeDamage(runtime, level, caster, target, facts);
            if (!authorization.decision().allowed()) continue;

            LivingEntity settlementTarget = findLoadedLivingEntity(server, targetId);
            if (settlementTarget == null || settlementTarget != target || !target.isAlive() || target.level() != level) {
                continue;
            }
            EntityProtectionFacts settlementFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization settlementAuthorization =
                authorizeDamage(runtime, level, caster, target, settlementFacts);
            if (!settlementAuthorization.decision().allowed()) continue;

            double policyMultiplier = Math.min(1.0D, settlementAuthorization.limits().damageMultiplierCap());
            double settlementDamage = boundedDamage * policyMultiplier;
            if (!Double.isFinite(settlementDamage) || settlementDamage <= 0.0D) continue;

            float healthBefore = target.getHealth();
            target.hurt(target.damageSources().indirectMagic(caster, caster), (float) settlementDamage);
            double actualDamage = Math.max(0.0D, (double) healthBefore - target.getHealth());
            if (actualDamage <= 0.0D) continue;
            damagedTargets++;
            totalDamageDealt += actualDamage;
        }

        if (damagedTargets == 0) {
            return new DamageSettlement(
                ArcanaDecision.deny(
                    "black_pyre_no_authorized_targets",
                    "No supplied target remained eligible for Black Pyre damage settlement"),
                0,
                0.0D);
        }
        return new DamageSettlement(ArcanaDecision.allow(), damagedTargets, totalDamageDealt);
    }

    private static TerrainSettlement settleSeed(
        MinecraftServer server,
        ArcanaServerRuntime runtime,
        ServerLevel level,
        UUID casterId,
        ArcanaCastId castId,
        BlockPos seed
    ) {
        String dimensionId = level.dimension().location().toString();
        if (level.getChunkSource().getChunkNow(seed.getX() >> 4, seed.getZ() >> 4) == null) {
            return TerrainSettlement.notApplied(
                CHUNK_UNLOADED,
                ArcanaDecision.deny(CHUNK_UNLOADED, "Black Pyre terrain target chunk is not loaded"));
        }

        WorldEffectMode mode = effectiveMode(runtime);
        if (mode == WorldEffectMode.OFF) {
            return TerrainSettlement.notApplied(
                WORLD_EFFECT_OFF,
                ArcanaDecision.deny("world_effect_mode", "Black Pyre terrain effects are disabled"));
        }
        if (mode == WorldEffectMode.COSMETIC) {
            return TerrainSettlement.notApplied(COSMETIC_ONLY, ArcanaDecision.allow());
        }

        long startedAtTick = level.getGameTime();
        long expiresAtTick = saturatingAdd(startedAtTick, DEFAULT_TEMPORARY_LIFETIME_TICKS);
        UUID frontierId = castId.value();
        BlackPyreCell seedCell = new BlackPyreCell(dimensionId, seed.getX(), seed.getY(), seed.getZ());
        ServerState state = stateFor(server);
        synchronized (state) {
            if (!state.scheduler.start(frontierId, seedCell, startedAtTick)) {
                return TerrainSettlement.notApplied(
                    FRONTIER_CAPACITY,
                    ArcanaDecision.deny(FRONTIER_CAPACITY, "Black Pyre frontier capacity is exhausted"));
            }
            state.contexts.put(frontierId, new FrontierContext(casterId, castId, dimensionId, expiresAtTick));
        }

        TerrainSettlement settlement = settleCell(runtime, level, casterId, castId, seed, expiresAtTick);
        if (!settlement.applied()) {
            finishFrontier(state, frontierId);
            return settlement;
        }

        List<BlackPyreCell> initialCandidates = spreadableNeighbors(level, seedCell);
        synchronized (state) {
            // The seed already settled synchronously; remove its scheduler queue entry without settling it twice.
            state.scheduler.tick(frontierId, startedAtTick, ignored -> true);
            if (!initialCandidates.isEmpty()) {
                state.scheduler.offer(frontierId, initialCandidates);
            }
            if (state.scheduler.pendingCells(frontierId) == 0) {
                state.scheduler.finish(frontierId);
                state.contexts.remove(frontierId);
            }
        }
        return settlement;
    }

    private static TerrainSettlement settleCell(
        ArcanaServerRuntime runtime,
        ServerLevel level,
        UUID casterId,
        ArcanaCastId castId,
        BlockPos pos,
        long expiresAtTick
    ) {
        String dimensionId = level.dimension().location().toString();
        if (level.getChunkSource().getChunkNow(pos.getX() >> 4, pos.getZ() >> 4) == null) {
            return TerrainSettlement.notApplied(
                CHUNK_UNLOADED,
                ArcanaDecision.deny(CHUNK_UNLOADED, "Black Pyre terrain target chunk is not loaded"));
        }

        WorldEffectMode mode = effectiveMode(runtime);
        if (mode == WorldEffectMode.OFF) {
            return TerrainSettlement.notApplied(
                WORLD_EFFECT_OFF,
                ArcanaDecision.deny("world_effect_mode", "Black Pyre terrain effects are disabled"));
        }
        if (mode == WorldEffectMode.COSMETIC) {
            return TerrainSettlement.notApplied(COSMETIC_ONLY, ArcanaDecision.allow());
        }

        long nowTick = level.getGameTime();
        String targetId = blockTargetId(dimensionId, pos);
        ArcanaCastRequest request = new ArcanaCastRequest(
            castId,
            WORLD_SAFETY_SPELL,
            new ArcanaCastContext(casterId, nowTick, dimensionId),
            0,
            targetId);
        ArcanaServices.TargetResolution target = ArcanaServices.TargetResolution.resolved(targetId);
        ChunkRef chunk = new ChunkRef(dimensionId, pos.getX() >> 4, pos.getZ() >> 4);
        TemporaryMutationKey key = new TemporaryMutationKey(dimensionId, pos.asLong());
        String replacementState = MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState());

        ArcanaDecision decision;
        if (mode == WorldEffectMode.TEMPORARY) {
            var gateway = runtime.temporaryBlockGateway().orElse(null);
            if (gateway == null) {
                return TerrainSettlement.notApplied(
                    WORLD_BACKEND_UNAVAILABLE,
                    ArcanaDecision.deny(WORLD_BACKEND_UNAVAILABLE, "Temporary Black Pyre world gateway is unavailable"));
            }
            decision = gateway.replaceProtected(
                request,
                target,
                chunk,
                key,
                replacementState,
                expiresAtTick,
                WorldMutationType.FIRE_SPREAD,
                runtime.worldMutationProtectionAdapters());
        } else {
            var gateway = runtime.permanentBlockGateway().orElse(null);
            if (gateway == null) {
                return TerrainSettlement.notApplied(
                    WORLD_BACKEND_UNAVAILABLE,
                    ArcanaDecision.deny(WORLD_BACKEND_UNAVAILABLE, "Permanent Black Pyre world gateway is unavailable"));
            }
            WorldMutationClass mutationClass = mode == WorldEffectMode.LIMITED
                ? WorldMutationClass.LIMITED
                : WorldMutationClass.PERMANENT;
            decision = gateway.replace(
                request,
                target,
                chunk,
                key,
                replacementState,
                WorldMutationType.FIRE_SPREAD,
                mutationClass);
        }

        if (!decision.allowed()) return TerrainSettlement.notApplied(decision.code(), decision);
        return new TerrainSettlement(true, "ok", 1, decision);
    }

    private static List<BlackPyreCell> spreadableNeighbors(ServerLevel level, BlackPyreCell cell) {
        List<BlackPyreCell> candidates = new ArrayList<>(4);
        addSpreadable(level, candidates, cell.dimensionId(), cell.x() + 1, cell.y(), cell.z());
        addSpreadable(level, candidates, cell.dimensionId(), cell.x() - 1, cell.y(), cell.z());
        addSpreadable(level, candidates, cell.dimensionId(), cell.x(), cell.y(), cell.z() + 1);
        addSpreadable(level, candidates, cell.dimensionId(), cell.x(), cell.y(), cell.z() - 1);
        return List.copyOf(candidates);
    }

    private static void addSpreadable(
        ServerLevel level,
        List<BlackPyreCell> candidates,
        String dimensionId,
        int x,
        int y,
        int z
    ) {
        BlockPos pos = new BlockPos(x, y, z);
        if (!isSpreadableLoadedCell(level, pos)) return;
        candidates.add(new BlackPyreCell(dimensionId, x, y, z));
    }

    private static boolean isSpreadableLoadedCell(ServerLevel level, BlockPos pos) {
        if (level.getChunkSource().getChunkNow(pos.getX() >> 4, pos.getZ() >> 4) == null) return false;
        var state = level.getBlockState(pos);
        return !state.isAir() && state.getFluidState().isEmpty() && !state.is(Blocks.BLACKSTONE);
    }

    private static boolean isLoaded(ServerLevel level, BlackPyreCell cell) {
        return level.dimension().location().toString().equals(cell.dimensionId())
            && level.getChunkSource().getChunkNow(cell.x() >> 4, cell.z() >> 4) != null;
    }

    private static ServerLevel findLevel(MinecraftServer server, String dimensionId) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dimensionId)) return level;
        }
        return null;
    }

    private static ServerState stateFor(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    private static void finishFrontier(ServerState state, UUID frontierId) {
        synchronized (state) {
            state.scheduler.finish(frontierId);
            state.contexts.remove(frontierId);
        }
    }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    private static WorldEffectMode effectiveMode(ArcanaServerRuntime runtime) {
        WorldEffectPolicyConfig config = runtime.worldEffectPolicy().config();
        WorldEffectOverride override = config.spellOverrides().get(BlackPyreDomainSpecifications.BLACK_PYRE);
        return override == null
            ? config.globalMode()
            : WorldEffectMode.mostRestrictive(config.globalMode(), override.modeCap());
    }

    private static boolean entityDamageAllowed(ArcanaServerRuntime runtime) {
        WorldEffectPolicyConfig config = runtime.worldEffectPolicy().config();
        WorldEffectOverride override = config.spellOverrides().get(BlackPyreDomainSpecifications.BLACK_PYRE);
        return config.entityDamageAllowed() && (override == null || override.entityDamageAllowed());
    }

    private static EntityInteractionAuthorization authorizeDamage(
        ArcanaServerRuntime runtime,
        ServerLevel level,
        LivingEntity caster,
        LivingEntity target,
        EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE));
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static String blockTargetId(String dimensionId, BlockPos pos) {
        return dimensionId + ":" + pos.getX() + "," + pos.getY() + "," + pos.getZ();
    }

    private static final class ServerState {
        final BlackPyreFrontierScheduler scheduler = new BlackPyreFrontierScheduler(
            BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS,
            BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER,
            BlackPyreSafetyCeilings.MAX_SPREAD_PER_TICK,
            BlackPyreSafetyCeilings.MAX_RADIUS_BLOCKS,
            BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS);
        final Map<UUID, FrontierContext> contexts = new LinkedHashMap<>();
    }

    private record FrontierContext(
        UUID casterId,
        ArcanaCastId castId,
        String dimensionId,
        long expiresAtTick
    ) {
        private FrontierContext {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(castId, "castId");
            Objects.requireNonNull(dimensionId, "dimensionId");
            if (dimensionId.isBlank()) throw new IllegalArgumentException("dimensionId cannot be blank");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
        }
    }

    private record DamageSettlement(ArcanaDecision decision, int damagedTargets, double damageDealt) {
        private DamageSettlement {
            Objects.requireNonNull(decision, "decision");
            if (damagedTargets < 0) throw new IllegalArgumentException("damagedTargets cannot be negative");
            if (!Double.isFinite(damageDealt) || damageDealt < 0.0D) {
                throw new IllegalArgumentException("damageDealt must be finite and non-negative");
            }
        }
    }

    private record TerrainSettlement(boolean applied, String code, int cells, ArcanaDecision decision) {
        private TerrainSettlement {
            Objects.requireNonNull(code, "code");
            Objects.requireNonNull(decision, "decision");
            if (code.isBlank()) throw new IllegalArgumentException("terrain code cannot be blank");
            if (cells < 0 || (!applied && cells != 0)) throw new IllegalArgumentException("invalid terrain cell count");
        }

        static TerrainSettlement notApplied(String code, ArcanaDecision decision) {
            return new TerrainSettlement(false, code, 0, decision);
        }
    }

    public record BlackPyreResult(
        ArcanaCastId castId,
        ArcanaDecision decision,
        int damagedTargets,
        double damageDealt,
        boolean terrainApplied,
        String terrainCode,
        int terrainCells
    ) {
        public BlackPyreResult {
            Objects.requireNonNull(castId, "castId");
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(terrainCode, "terrainCode");
            if (damagedTargets < 0 || terrainCells < 0) throw new IllegalArgumentException("result counts cannot be negative");
            if (!Double.isFinite(damageDealt) || damageDealt < 0.0D) {
                throw new IllegalArgumentException("damageDealt must be finite and non-negative");
            }
            if (terrainCode.isBlank()) throw new IllegalArgumentException("terrainCode cannot be blank");
            if (!terrainApplied && terrainCells != 0) throw new IllegalArgumentException("unapplied terrain cannot report cells");
        }

        static BlackPyreResult denied(ArcanaCastId castId, String code, String detail, String terrainCode) {
            return new BlackPyreResult(
                castId,
                ArcanaDecision.deny(code, detail),
                0,
                0.0D,
                false,
                terrainCode,
                0);
        }
    }
}
