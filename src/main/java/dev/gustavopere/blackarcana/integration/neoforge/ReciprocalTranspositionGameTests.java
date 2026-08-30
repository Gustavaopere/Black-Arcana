package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class ReciprocalTranspositionGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftReciprocalTranspositionRuntime";

    private ReciprocalTranspositionGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void twoLivingEndpointsSwapAtomicallyAfterFreshRevalidation(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(6, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        clearEntitySpace(helper, first);
        clearEntitySpace(helper, second);
        helper.assertTrue(configureThroughput(server, 2).allowed(), "fixture throughput policy must configure");

        double firstX = first.getX();
        double firstY = first.getY();
        double firstZ = first.getZ();
        double secondX = second.getX();
        double secondY = second.getY();
        double secondZ = second.getZ();
        long firstVersion = snapshotVersion(server, first.getUUID());
        long secondVersion = snapshotVersion(server, second.getUUID());

        Object result = swap(
            server,
            owner.getUUID(),
            first.getUUID(),
            second.getUUID(),
            firstVersion,
            secondVersion,
            server.getTickCount(),
            true,
            true);

        helper.assertTrue(decision(result).allowed() && swapped(result),
            "two eligible fresh endpoints must settle one reciprocal transposition");
        helper.assertTrue(near(first, secondX, secondY, secondZ),
            "first endpoint must finish at the second endpoint's original position");
        helper.assertTrue(near(second, firstX, firstY, firstZ),
            "second endpoint must finish at the first endpoint's original position");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void staleEndpointOrDeniedConsentMutatesNeitherEndpoint(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(6, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        clearEntitySpace(helper, first);
        clearEntitySpace(helper, second);
        helper.assertTrue(configureThroughput(server, 4).allowed(), "fixture throughput policy must configure");

        long firstVersion = snapshotVersion(server, first.getUUID());
        long staleSecondVersion = snapshotVersion(server, second.getUUID());
        second.setPos(second.getX() + 1.0D, second.getY(), second.getZ());
        double firstX = first.getX();
        double secondX = second.getX();

        Object stale = swap(
            server,
            owner.getUUID(),
            first.getUUID(),
            second.getUUID(),
            firstVersion,
            staleSecondVersion,
            server.getTickCount(),
            true,
            true);
        helper.assertTrue(!decision(stale).allowed()
                && "transposition_endpoint_changed".equals(decision(stale).code()),
            "stale endpoint version must abort the whole transposition before movement");
        helper.assertTrue(Math.abs(first.getX() - firstX) < 0.01D && Math.abs(second.getX() - secondX) < 0.01D,
            "stale endpoint denial must leave both current positions untouched");

        long freshFirst = snapshotVersion(server, first.getUUID());
        long freshSecond = snapshotVersion(server, second.getUUID());
        Object consent = swap(
            server,
            owner.getUUID(),
            first.getUUID(),
            second.getUUID(),
            freshFirst,
            freshSecond,
            server.getTickCount() + 1L,
            false,
            true);
        helper.assertTrue(!decision(consent).allowed() && "consent_denied".equals(decision(consent).code()),
            "host-denied player/PvP consent must fail closed through the shared planner");
        helper.assertTrue(Math.abs(first.getX() - firstX) < 0.01D && Math.abs(second.getX() - secondX) < 0.01D,
            "consent denial must not move either endpoint");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void throughputLimitRejectsSecondSuccessfulSwapInSameWindow(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(6, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        clearEntitySpace(helper, first);
        clearEntitySpace(helper, second);
        helper.assertTrue(configureThroughput(server, 1).allowed(), "one-per-second fixture policy must configure");
        long now = server.getTickCount();

        Object firstSwap = swap(
            server,
            owner.getUUID(),
            first.getUUID(),
            second.getUUID(),
            snapshotVersion(server, first.getUUID()),
            snapshotVersion(server, second.getUUID()),
            now,
            true,
            true);
        helper.assertTrue(decision(firstSwap).allowed(), "first transposition in a throughput window must settle");
        double afterFirstX = first.getX();
        double afterSecondX = second.getX();

        Object overflow = swap(
            server,
            owner.getUUID(),
            first.getUUID(),
            second.getUUID(),
            snapshotVersion(server, first.getUUID()),
            snapshotVersion(server, second.getUUID()),
            now,
            true,
            true);
        helper.assertTrue(!decision(overflow).allowed()
                && "transposition_throughput".equals(decision(overflow).code()),
            "second successful transposition attempt in the same one-per-second window must fail closed");
        helper.assertTrue(Math.abs(first.getX() - afterFirstX) < 0.01D
                && Math.abs(second.getX() - afterSecondX) < 0.01D,
            "throughput denial must not partially move endpoints");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void itemEntityEndpointSwapsWithoutCloningOrConsumingStack(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var living = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var level = helper.getLevel();
        ItemEntity item = new ItemEntity(
            level,
            living.getX() + 4.0D,
            living.getY(),
            living.getZ(),
            new ItemStack(Items.DIAMOND, 3));
        level.addFreshEntity(item);
        MinecraftServer server = level.getServer();
        clearEntitySpace(helper, living);
        clearEntitySpace(helper, item);
        helper.assertTrue(configureThroughput(server, 2).allowed(), "item-endpoint throughput policy must configure");
        int itemEntitiesBefore = level.getEntitiesOfClass(ItemEntity.class, item.getBoundingBox().inflate(16.0D)).size();
        int stackCountBefore = item.getItem().getCount();
        double livingX = living.getX();
        double itemX = item.getX();

        Object result = swap(
            server,
            owner.getUUID(),
            living.getUUID(),
            item.getUUID(),
            snapshotVersion(server, living.getUUID()),
            snapshotVersion(server, item.getUUID()),
            server.getTickCount(),
            true,
            true);

        helper.assertTrue(decision(result).allowed() && swapped(result),
            "eligible ItemEntity endpoint must participate in the same atomic swap contract");
        helper.assertTrue(Math.abs(living.getX() - itemX) < 0.01D && Math.abs(item.getX() - livingX) < 0.01D,
            "living and item endpoints must exchange their original positions");
        helper.assertTrue(item.getItem().is(Items.DIAMOND) && item.getItem().getCount() == stackCountBefore,
            "transposition must not consume or rewrite the ItemEntity stack");
        helper.assertTrue(level.getEntitiesOfClass(ItemEntity.class, item.getBoundingBox().inflate(16.0D)).size() == itemEntitiesBefore,
            "transposition must not clone ItemEntity endpoints");
        helper.succeed();
    }

    private static ArcanaDecision configureThroughput(MinecraftServer server, int maxPerSecond) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("configureThroughput", MinecraftServer.class, int.class);
        return (ArcanaDecision) method.invoke(null, server, maxPerSecond);
    }

    private static long snapshotVersion(MinecraftServer server, UUID entityId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("snapshotVersion", MinecraftServer.class, UUID.class);
        return (long) method.invoke(null, server, entityId);
    }

    private static Object swap(
            MinecraftServer server,
            UUID ownerId,
            UUID firstEntityId,
            UUID secondEntityId,
            long firstVersion,
            long secondVersion,
            long nowTick,
            boolean firstConsent,
            boolean secondConsent
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "swap",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            UUID.class,
            long.class,
            long.class,
            long.class,
            boolean.class,
            boolean.class);
        return method.invoke(
            null,
            server,
            ownerId,
            firstEntityId,
            secondEntityId,
            firstVersion,
            secondVersion,
            nowTick,
            firstConsent,
            secondConsent);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean swapped(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("swapped").invoke(result);
    }

    private static void clearEntitySpace(GameTestHelper helper, net.minecraft.world.entity.Entity entity) {
        BlockPos base = BlockPos.containing(entity.getX(), entity.getY(), entity.getZ());
        helper.getLevel().setBlockAndUpdate(base, Blocks.AIR.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(base.above(), Blocks.AIR.defaultBlockState());
    }

    private static boolean near(net.minecraft.world.entity.Entity entity, double x, double y, double z) {
        return Math.abs(entity.getX() - x) < 0.01D
            && Math.abs(entity.getY() - y) < 0.01D
            && Math.abs(entity.getZ() - z) < 0.01D;
    }
}
