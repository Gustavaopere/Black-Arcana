package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class MinecraftSafeDestinationGameTests {
    private static final String RESOLVER =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSafeDestinationResolver";

    private MinecraftSafeDestinationGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void realWorldFactsAcceptSafeAirAndRejectCollisionFluidAndUnloadedChunks(GameTestHelper helper) throws Exception {
        var entity = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        double x = entity.getX() + 2.0D;
        double y = entity.getY();
        double z = entity.getZ();
        BlockPos landing = BlockPos.containing(x, y, z);

        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());
        Object safe = evaluate(server, entity, level, x, y, z);
        helper.assertTrue(allowed(safe), "loaded collision-free dry destination must be admitted; code=" + code(safe));

        level.setBlockAndUpdate(landing, Blocks.STONE.defaultBlockState());
        Object collision = evaluate(server, entity, level, x, y, z);
        helper.assertTrue(!allowed(collision) && "collision_blocked".equals(code(collision)),
            "solid landing geometry must fail closed as collision_blocked");

        level.setBlockAndUpdate(landing, Blocks.WATER.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());
        Object fluid = evaluate(server, entity, level, x, y, z);
        helper.assertTrue(!allowed(fluid) && "fluid_denied".equals(code(fluid)),
            "fluid landing must fail closed as fluid_denied");

        double farX = entity.getX() + 4096.0D;
        Object unloaded = evaluate(server, entity, level, farX, y, z);
        helper.assertTrue(!allowed(unloaded) && "destination_unloaded".equals(code(unloaded)),
            "safe destination resolution must never force-load a distant chunk");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void lowHeadroomSuffocationGeometryFailsClosed(GameTestHelper helper) throws Exception {
        var entity = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        double x = entity.getX() + 2.0D;
        double y = entity.getY();
        double z = entity.getZ();
        BlockPos landing = BlockPos.containing(x, y, z);

        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.STONE.defaultBlockState());
        Object lowHeadroom = evaluate(server, entity, level, x, y, z);
        helper.assertTrue(!allowed(lowHeadroom) && "collision_blocked".equals(code(lowHeadroom)),
            "low-headroom/suffocation geometry must be rejected by the authoritative full-entity collision check");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80, batch = "space_world_border")
    public static void loadedDestinationOutsideLiveWorldBorderFailsClosed(GameTestHelper helper) throws Exception {
        var entity = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        var border = level.getWorldBorder();
        double previousCenterX = border.getCenterX();
        double previousCenterZ = border.getCenterZ();
        double previousSize = border.getSize();

        double x = entity.getX() + 3.0D;
        double y = entity.getY();
        double z = entity.getZ();
        BlockPos landing = BlockPos.containing(x, y, z);
        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());

        try {
            border.setCenter(entity.getX(), entity.getZ());
            border.setSize(4.0D);
            Object outside = evaluate(server, entity, level, x, y, z);
            helper.assertTrue(!allowed(outside) && "world_border".equals(code(outside)),
                "loaded collision-free destination outside the live world border must fail closed as world_border");
        } finally {
            border.setCenter(previousCenterX, previousCenterZ);
            border.setSize(previousSize);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void dimensionMismatchAndVehiclesFailClosedBeforeTeleport(GameTestHelper helper) throws Exception {
        var entity = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        double x = entity.getX() + 2.0D;
        double y = entity.getY();
        double z = entity.getZ();
        BlockPos landing = BlockPos.containing(x, y, z);
        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());

        ServerLevel nether = server.getLevel(Level.NETHER);
        helper.assertTrue(nether != null, "GameTest server must expose Nether for dimension mismatch validation");
        Object wrongDimension = evaluate(server, entity, nether, x, y, z);
        helper.assertTrue(!allowed(wrongDimension) && "dimension_denied".equals(code(wrongDimension)),
            "cross-dimension destination must fail closed unless an explicit spell policy allows it");

        LivingEntity mount = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        helper.assertTrue(entity.startRiding(mount, true), "vehicle fixture must mount the test player");
        Object vehicle = evaluate(server, entity, level, x, y, z);
        helper.assertTrue(!allowed(vehicle) && "vehicle_unsafe".equals(code(vehicle)),
            "passenger/vehicle state must fail closed before displacement");
        helper.succeed();
    }

    private static Object evaluate(
        MinecraftServer server,
        LivingEntity entity,
        ServerLevel destinationLevel,
        double x,
        double y,
        double z
    ) throws Exception {
        Class<?> resolver = Class.forName(RESOLVER);
        Method method = resolver.getMethod(
            "evaluate",
            MinecraftServer.class,
            LivingEntity.class,
            ServerLevel.class,
            double.class,
            double.class,
            double.class);
        return method.invoke(null, server, entity, destinationLevel, x, y, z);
    }

    private static boolean allowed(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("allowed").invoke(result);
    }

    private static String code(Object result) throws Exception {
        return (String) result.getClass().getMethod("code").invoke(result);
    }
}
