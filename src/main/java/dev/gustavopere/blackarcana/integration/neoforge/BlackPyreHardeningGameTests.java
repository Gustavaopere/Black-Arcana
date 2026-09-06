package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreDomainSpecifications;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreHardeningGameTests {
    private BlackPyreHardeningGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void alliedTargetIsNotDamagedByBlackPyre(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(net.minecraft.world.entity.EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        Scoreboard scoreboard = helper.getLevel().getScoreboard();
        String teamName = "ba_pyre_ally";
        PlayerTeam existing = scoreboard.getPlayerTeam(teamName);
        if (existing != null) scoreboard.removePlayerTeam(existing);
        PlayerTeam team = scoreboard.addPlayerTeam(teamName);
        float healthBefore = target.getHealth();
        try {
            scoreboard.addPlayerToTeam(caster.getScoreboardName(), team);
            scoreboard.addPlayerToTeam(target.getScoreboardName(), team);
            Object result = igniteDefault(
                helper.getLevel().getServer(), caster.getUUID(), List.of(target.getUUID()), 8.0D, false,
                caster.blockPosition());
            helper.assertTrue(damagedTargets(result) == 0,
                "Black Pyre must preserve canonical allied-target protection");
            helper.assertTrue(Math.abs(target.getHealth() - healthBefore) < 0.001F,
                "allied target health must remain unchanged");
        } finally {
            scoreboard.removePlayerTeam(team);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void permanentMutationRequiresFullModeAndCommitsOnlyAfterOptIn(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.makeMockServerPlayerInLevel();
        BlockPos pos = helper.absolutePos(new BlockPos(2, 1, 2));
        helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        String dimension = helper.getLevel().dimension().location().toString();
        TemporaryMutationKey key = new TemporaryMutationKey(dimension, pos.asLong());
        ChunkRef chunk = new ChunkRef(dimension, pos.getX() >> 4, pos.getZ() >> 4);
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.LIMITED, 4096, true, Map.of()));
            ArcanaCastRequest limitedRequest = request(caster.getUUID(), dimension, server.getTickCount());
            ArcanaDecision denied = runtime.permanentBlockGateway().orElseThrow().replace(
                limitedRequest,
                ArcanaServices.TargetResolution.resolved("block:" + pos.asLong()),
                chunk,
                key,
                MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()),
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT);
            helper.assertTrue(!denied.allowed(), "PERMANENT Black Pyre work must be denied below FULL mode");
            helper.assertTrue(runtime.worldEffectBudgets().usedUnits(limitedRequest.castId()) == 0,
                "mode denial must happen before canonical budget consumption");
            helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.STONE),
                "denied PERMANENT work must not mutate the real Minecraft backend");

            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.FULL, 4096, true, Map.of()));
            ArcanaCastRequest fullRequest = request(caster.getUUID(), dimension, server.getTickCount() + 1L);
            ArcanaDecision allowed = runtime.permanentBlockGateway().orElseThrow().replace(
                fullRequest,
                ArcanaServices.TargetResolution.resolved("block:" + pos.asLong()),
                chunk,
                key,
                MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()),
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT);
            helper.assertTrue(allowed.allowed(), "FULL mode must admit bounded protected PERMANENT Black Pyre work");
            helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.BLACKSTONE),
                "FULL/PERMANENT settlement must reach the real backend exactly once");
        } finally {
            runtime.configureWorldEffects(previous);
            helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void permanentGatewayRejectsStaleMinecraftStateWithoutOverwrite(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.makeMockServerPlayerInLevel();
        BlockPos pos = helper.absolutePos(new BlockPos(4, 1, 2));
        helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        String dimension = helper.getLevel().dimension().location().toString();
        TemporaryMutationKey key = new TemporaryMutationKey(dimension, pos.asLong());
        ChunkRef chunk = new ChunkRef(dimension, pos.getX() >> 4, pos.getZ() >> 4);
        ArcanaCastRequest request = request(caster.getUUID(), dimension, server.getTickCount());
        AtomicInteger calls = new AtomicInteger();
        String adapterId = "gt_pyre_stale_" + Integer.toUnsignedString(pos.hashCode());
        runtime.worldMutationProtectionAdapters().register(adapterId, query -> {
            if (query.castId().equals(request.castId()) && query.key().equals(key) && calls.incrementAndGet() == 2) {
                helper.getLevel().setBlock(pos, Blocks.DIAMOND_BLOCK.defaultBlockState(), Block.UPDATE_ALL);
            }
            return ArcanaDecision.allow();
        });
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.FULL, 4096, true, Map.of()));
            ArcanaDecision decision = runtime.permanentBlockGateway().orElseThrow().replace(
                request,
                ArcanaServices.TargetResolution.resolved("block:" + pos.asLong()),
                chunk,
                key,
                MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()),
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT);
            helper.assertTrue(!decision.allowed() && "world_state_changed".equals(decision.code()),
                "state changed after admission must fail the final compare-and-set");
            helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.DIAMOND_BLOCK),
                "stale Black Pyre settlement must not overwrite the intervening player/world edit");
            helper.assertTrue(runtime.worldEffectBudgets().usedUnits(request.castId()) == 1,
                "one admitted stale attempt may consume budget once, never more than once");
        } finally {
            runtime.configureWorldEffects(previous);
            helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 120)
    public static void restartSimulationKeepsRollbackButNeverRevivesFrontier(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.makeMockServerPlayerInLevel();
        BlockPos seed = helper.absolutePos(new BlockPos(6, 1, 2));
        BlockPos neighbor = seed.east();
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        helper.getLevel().setBlock(neighbor, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(), 1.0D, true, seed);
            ArcanaCastId castId = castId(result);
            helper.assertTrue(terrainApplied(result), "restart fixture must create one temporary Black Pyre mutation");
            helper.assertTrue(isFrontierActive(server, castId), "restart fixture must begin with an active ephemeral frontier");

            BlackArcanaSavedData data = new BlackArcanaSavedData();
            data.capture(runtime.cooldowns(), runtime.charges(), runtime.loadouts(), runtime.temporaryMutations(), now);
            CompoundTag encoded = data.save(new CompoundTag(), helper.getLevel().registryAccess());
            BlackArcanaSavedData decoded = BlackArcanaSavedData.load(encoded, helper.getLevel().registryAccess());

            invokeBlackPyreLifecycle("onServerStopped", ServerStoppedEvent.class, new ServerStoppedEvent(server));
            helper.assertTrue(!isFrontierActive(server, castId),
                "server stop must clear the ephemeral frontier before any restart restore occurs");
            invokeBlackPyreLifecycle("onServerStarted", ServerStartedEvent.class, new ServerStartedEvent(server));
            helper.assertTrue(!isFrontierActive(server, castId),
                "server start must create fresh frontier state rather than revive persisted spread work");

            ArcanaServerRuntime restored = ArcanaServerRuntime.createDefault();
            decoded.restore(restored.cooldowns(), restored.charges(), restored.loadouts(), restored.temporaryMutations(), now);
            helper.assertTrue(restored.temporaryMutations().snapshot().stream().anyMatch(m -> m.castId().equals(castId)),
                "temporary rollback ownership must survive the same persistence round-trip that excludes frontier state");
        } finally {
            runtime.configureWorldEffects(previous);
            runtime.tick(now + BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS + 1L);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 120)
    public static void fullModeCannotExceedConcurrentFrontierCeiling(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.makeMockServerPlayerInLevel();
        resetBlackPyreState(server);
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.FULL, 4096, true, Map.of()));
            for (int i = 0; i < BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS; i++) {
                BlockPos seed = helper.absolutePos(new BlockPos(1 + i * 2, 1, 6));
                helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
                helper.getLevel().setBlock(seed.north(), Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
                Object result = igniteDefault(server, caster.getUUID(), List.of(), 1.0D, true, seed);
                helper.assertTrue(terrainApplied(result), "each frontier up to the hard concurrent cap must be admitted");
            }
            helper.assertTrue(activeFrontiers(server) == BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS,
                "FULL mode must still stop at the hard concurrent-frontier ceiling");

            BlockPos overflowSeed = helper.absolutePos(new BlockPos(1, 1, 9));
            helper.getLevel().setBlock(overflowSeed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
            helper.getLevel().setBlock(overflowSeed.north(), Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
            Object overflow = igniteDefault(server, caster.getUUID(), List.of(), 1.0D, true, overflowSeed);
            helper.assertTrue(!terrainApplied(overflow) && "black_pyre_frontier_capacity".equals(terrainCode(overflow)),
                "ninth FULL frontier must fail closed instead of raising the technical ceiling");
            helper.assertTrue(activeFrontiers(server) == BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS,
                "overflow attempt must not alter the bounded active-frontier count");
        } finally {
            runtime.configureWorldEffects(previous);
            resetBlackPyreState(server);
        }
        helper.succeed();
    }

    private static ArcanaServerRuntime requireRuntime(MinecraftServer server) {
        return ArcanaServerRuntimeManager.get(server).orElseThrow();
    }

    private static ArcanaCastRequest request(UUID casterId, String dimension, long nowTick) {
        return new ArcanaCastRequest(
            ArcanaCastId.random(),
            new ArcanaSpellDefinition(
                BlackPyreDomainSpecifications.BLACK_PYRE,
                "spell.black_arcana.black_pyre",
                "black_arcana:black_pyre",
                ArcanaCost.none(),
                true),
            new ArcanaCastContext(casterId, Math.max(0L, nowTick), dimension));
    }

    private static Object igniteDefault(
        MinecraftServer server,
        UUID casterId,
        List<UUID> targets,
        double damage,
        boolean terrainRequested,
        BlockPos seed
    ) throws Exception {
        Method method = MinecraftBlackPyreRuntime.class.getMethod(
            "igniteDefault", MinecraftServer.class, UUID.class, List.class, double.class, boolean.class,
            int.class, int.class, int.class);
        return method.invoke(null, server, casterId, targets, damage, terrainRequested, seed.getX(), seed.getY(), seed.getZ());
    }

    private static void invokeBlackPyreLifecycle(String name, Class<?> eventType, Object event) throws Exception {
        Method method = MinecraftBlackPyreRuntime.class.getDeclaredMethod(name, eventType);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static void resetBlackPyreState(MinecraftServer server) throws Exception {
        invokeBlackPyreLifecycle("onServerStopped", ServerStoppedEvent.class, new ServerStoppedEvent(server));
        invokeBlackPyreLifecycle("onServerStarted", ServerStartedEvent.class, new ServerStartedEvent(server));
    }

    private static boolean isFrontierActive(MinecraftServer server, ArcanaCastId castId) {
        return MinecraftBlackPyreRuntime.isFrontierActive(server, castId);
    }

    private static int activeFrontiers(MinecraftServer server) {
        return MinecraftBlackPyreRuntime.activeFrontiers(server);
    }

    private static int damagedTargets(Object result) throws Exception {
        return (int) result.getClass().getMethod("damagedTargets").invoke(result);
    }

    private static boolean terrainApplied(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("terrainApplied").invoke(result);
    }

    private static String terrainCode(Object result) throws Exception {
        return (String) result.getClass().getMethod("terrainCode").invoke(result);
    }

    private static ArcanaCastId castId(Object result) throws Exception {
        return (ArcanaCastId) result.getClass().getMethod("castId").invoke(result);
    }
}
