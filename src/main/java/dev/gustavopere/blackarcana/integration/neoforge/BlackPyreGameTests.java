package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreGameTests {
    private BlackPyreGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void entityDamageRemainsIndependentWhenTerrainIsNotRequested(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        float healthBefore = target.getHealth();
        Object result = igniteDefault(helper.getLevel().getServer(), caster.getUUID(), List.of(target.getUUID()), 3.0D, false, caster.blockPosition());
        helper.assertTrue(decision(result).allowed(), "eligible Black Pyre entity damage must settle");
        helper.assertTrue(damagedTargets(result) == 1, "one eligible target must be damaged once");
        helper.assertTrue(damageDealt(result) > 0.0D && damageDealt(result) <= 3.0D, "Black Pyre must report only bounded real health loss");
        helper.assertTrue(target.getHealth() < healthBefore, "eligible target must lose health");
        helper.assertTrue(!terrainApplied(result), "entity-only cast must not mutate terrain");
        helper.assertTrue("terrain_not_requested".equals(terrainCode(result)), "entity-only cast must expose terrain_not_requested");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void cosmeticModeNeverMutatesBlocks(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.COSMETIC, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            helper.assertTrue(decision(result).allowed(), "terrain degradation must not undo authorized entity damage");
            helper.assertTrue(!terrainApplied(result), "COSMETIC mode cannot mutate terrain");
            helper.assertTrue(helper.getLevel().getBlockState(seed).is(Blocks.STONE), "COSMETIC mode must leave the seed unchanged");
            helper.assertTrue("black_pyre_cosmetic_only".equals(terrainCode(result)), "COSMETIC degradation must be explicit");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void temporaryModeMutatesAndRestoresUnchangedCell(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            helper.assertTrue(terrainApplied(result), "TEMPORARY mode must settle the loaded authorized seed");
            helper.assertTrue(terrainCells(result) == 1, "initial ignition must mutate exactly one seed cell");
            helper.assertTrue(!helper.getLevel().getBlockState(seed).is(Blocks.STONE), "temporary cell must visibly replace the seed");
            runtime.tick(now + 1_201L);
            helper.assertTrue(helper.getLevel().getBlockState(seed).is(Blocks.STONE), "unchanged temporary cell must restore after expiry");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void temporaryRestorationNeverOverwritesLaterWorldEdit(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            helper.assertTrue(terrainApplied(result), "temporary seed must settle before edit-protection test");
            helper.getLevel().setBlock(seed, Blocks.DIAMOND_BLOCK.defaultBlockState(), Block.UPDATE_ALL);
            runtime.tick(now + 1_201L);
            helper.assertTrue(helper.getLevel().getBlockState(seed).is(Blocks.DIAMOND_BLOCK), "restoration CAS must not overwrite a later world/player edit");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void mutationProtectionDenialDoesNotBurnWorldBudget(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(2, -1, 2);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long deniedPackedPos = seed.asLong();
        String adapterId = "gt_black_pyre_" + Integer.toUnsignedString(seed.hashCode());
        runtime.worldMutationProtectionAdapters().register(adapterId, query ->
            query.key().packedBlockPos() == deniedPackedPos
                ? ArcanaDecision.deny("world_mutation_protected_test", "GameTest protected Black Pyre cell")
                : ArcanaDecision.allow());
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            ArcanaCastId castId = castId(result);
            helper.assertTrue(!terrainApplied(result), "protected cell must never mutate");
            helper.assertTrue("world_mutation_protected_test".equals(terrainCode(result)), "protection denial code must propagate");
            helper.assertTrue(runtime.worldEffectBudgets().usedUnits(castId) == 0, "protection denial must occur before world budget consumption");
            helper.assertTrue(helper.getLevel().getBlockState(seed).is(Blocks.STONE), "protected seed must remain unchanged");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void limitedModeCommitsBoundedPermanentCell(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.LIMITED, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            helper.assertTrue(terrainApplied(result), "LIMITED mode must permit bounded permanent settlement");
            helper.assertTrue(terrainCells(result) == 1, "initial LIMITED ignition must commit exactly one cell");
            helper.assertTrue(!helper.getLevel().getBlockState(seed).is(Blocks.STONE), "LIMITED cell must replace the seed");
            var committed = helper.getLevel().getBlockState(seed);
            runtime.tick(now + 1_201L);
            helper.assertTrue(helper.getLevel().getBlockState(seed).equals(committed), "LIMITED mutation must not enter temporary restoration tracking");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void unloadedTerrainCandidateNeverForceLoadsChunk(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos far = new BlockPos(100_000, 64, 100_000);
        int chunkX = far.getX() >> 4;
        int chunkZ = far.getZ() >> 4;
        helper.assertTrue(helper.getLevel().getChunkSource().getChunkNow(chunkX, chunkZ) == null, "far GameTest chunk must start unloaded");
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, far);
            helper.assertTrue(!terrainApplied(result), "unloaded candidate must fail terrain settlement");
            helper.assertTrue("world_chunk_unloaded".equals(terrainCode(result)), "unloaded denial must be explicit");
            helper.assertTrue(helper.getLevel().getChunkSource().getChunkNow(chunkX, chunkZ) == null, "Black Pyre must never acquire/load the rejected chunk");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void blackPyreNeverDelegatesToVanillaFireCascade(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        BlockPos neighbor = seed.east();
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        helper.getLevel().setBlock(neighbor, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            helper.assertTrue(terrainApplied(result), "bounded seed must settle");
            helper.assertTrue(terrainCells(result) == 1, "ignite call must settle only its scheduler-admitted seed work");
            helper.assertTrue(helper.getLevel().getBlockState(neighbor).is(Blocks.STONE), "neighbor cannot change through vanilla fire/random-tick cascade");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void frontierAdvancesOnlyWhenRuntimeTickProcessesPendingCells(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        List<BlockPos> neighbors = List.of(seed.east(), seed.west(), seed.north(), seed.south());
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        neighbors.forEach(pos -> helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL));
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            ArcanaCastId frontierCastId = castId(result);
            helper.assertTrue(terrainApplied(result), "seed ignition must settle before the frontier starts");
            helper.assertTrue(isFrontierActive(server, frontierCastId), "successful terrain ignition must keep its own bounded frontier active");
            helper.assertTrue(neighbors.stream().allMatch(pos -> helper.getLevel().getBlockState(pos).is(Blocks.STONE)),
                "frontier neighbors must remain untouched until a runtime tick admits them");
            helper.assertTrue(tickBlackPyreFrontiers(server, now + 1L), "Black Pyre runtime must expose its server-owned tick path");
            long mutated = neighbors.stream().filter(pos -> !helper.getLevel().getBlockState(pos).is(Blocks.STONE)).count();
            helper.assertTrue(mutated > 0L, "one runtime tick must advance at least one loaded frontier cell");
            helper.assertTrue(mutated <= 16L, "one runtime tick must never exceed the hard per-frontier spread budget");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void expiredFrontierIsRemovedBeforeFurtherSettlement(GameTestHelper helper) throws Exception {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        BlockPos neighbor = seed.east();
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        helper.getLevel().setBlock(neighbor, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        long now = helper.getLevel().getGameTime();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            Object result = igniteDefault(server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true, seed);
            ArcanaCastId frontierCastId = castId(result);
            helper.assertTrue(terrainApplied(result), "seed ignition must settle before expiry test");
            helper.assertTrue(isFrontierActive(server, frontierCastId), "frontier must exist before its lifetime ceiling");
            helper.assertTrue(tickBlackPyreFrontiers(server, now + 1_200L), "Black Pyre runtime must process expiry through its tick path");
            helper.assertTrue(!isFrontierActive(server, frontierCastId), "the same frontier must be removed exactly at its lifetime ceiling");
            helper.assertTrue(helper.getLevel().getBlockState(neighbor).is(Blocks.STONE),
                "expired pending work must not settle after frontier removal");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    private static ArcanaServerRuntime requireRuntime(MinecraftServer server) {
        return ArcanaServerRuntimeManager.get(server).orElseThrow(() -> new IllegalStateException("Black Arcana runtime unavailable"));
    }

    private static Object igniteDefault(MinecraftServer server, UUID casterId, List<UUID> targets, double damage, boolean terrainRequested, BlockPos seed) throws Exception {
        Class<?> runtime = Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftBlackPyreRuntime");
        Method method = runtime.getMethod("igniteDefault", MinecraftServer.class, UUID.class, List.class, double.class, boolean.class, int.class, int.class, int.class);
        return method.invoke(null, server, casterId, targets, damage, terrainRequested, seed.getX(), seed.getY(), seed.getZ());
    }

    private static boolean isFrontierActive(MinecraftServer server, ArcanaCastId castId) {
        try {
            Class<?> runtime = Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftBlackPyreRuntime");
            Method method = runtime.getMethod("isFrontierActive", MinecraftServer.class, ArcanaCastId.class);
            return (boolean) method.invoke(null, server, castId);
        } catch (ReflectiveOperationException failure) {
            return false;
        }
    }

    private static boolean tickBlackPyreFrontiers(MinecraftServer server, long nowTick) {
        try {
            Class<?> runtime = Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftBlackPyreRuntime");
            Method method = runtime.getMethod("tickFrontiers", MinecraftServer.class, long.class);
            method.invoke(null, server, nowTick);
            return true;
        } catch (ReflectiveOperationException failure) {
            return false;
        }
    }

    private static ArcanaDecision decision(Object result) throws Exception { return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result); }
    private static int damagedTargets(Object result) throws Exception { return (int) result.getClass().getMethod("damagedTargets").invoke(result); }
    private static double damageDealt(Object result) throws Exception { return (double) result.getClass().getMethod("damageDealt").invoke(result); }
    private static boolean terrainApplied(Object result) throws Exception { return (boolean) result.getClass().getMethod("terrainApplied").invoke(result); }
    private static String terrainCode(Object result) throws Exception { return (String) result.getClass().getMethod("terrainCode").invoke(result); }
    private static int terrainCells(Object result) throws Exception { return (int) result.getClass().getMethod("terrainCells").invoke(result); }
    private static ArcanaCastId castId(Object result) throws Exception { return (ArcanaCastId) result.getClass().getMethod("castId").invoke(result); }
}
