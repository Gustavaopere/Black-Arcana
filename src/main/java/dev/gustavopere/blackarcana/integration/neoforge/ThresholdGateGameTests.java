package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class ThresholdGateGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftThresholdGateRuntime";

    private ThresholdGateGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void ownedLoadedPairTransfersExistingEntityToValidatedDestination(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var entity = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var server = helper.getLevel().getServer();
        var level = helper.getLevel();
        UUID gateId = UUID.randomUUID();
        String dimension = level.dimension().location().toString();
        Vec3 destination = helper.absoluteVec(new Vec3(6.5D, 2.0D, 1.5D));

        clearLanding(helper, new BlockPos(6, 2, 1));
        ArcanaDecision registration = registerPair(
            server, gateId, owner.getUUID(), dimension,
            entity.getX(), entity.getY(), entity.getZ(),
            destination.x, destination.y, destination.z,
            4);
        helper.assertTrue(registration.allowed(), "valid loaded gate pair must register");

        Object result = transfer(server, gateId, owner.getUUID(), 0, entity.getUUID(), server.getTickCount(), true);
        helper.assertTrue(decision(result).allowed() && transferred(result),
            "owned loaded gate must move an eligible existing entity");
        helper.assertTrue(samePosition(entity, destination.x, destination.y, destination.z),
            "entity must land exactly at the paired endpoint supplied by the host");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void blockedDestinationAndWrongOwnerFailClosedWithoutMovement(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var entity = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var server = helper.getLevel().getServer();
        var level = helper.getLevel();
        UUID gateId = UUID.randomUUID();
        String dimension = level.dimension().location().toString();
        double x = entity.getX();
        double y = entity.getY();
        double z = entity.getZ();
        Vec3 destination = helper.absoluteVec(new Vec3(6.5D, 2.0D, 1.5D));

        helper.setBlock(new BlockPos(6, 2, 1), Blocks.STONE);
        ArcanaDecision registration = registerPair(
            server, gateId, owner.getUUID(), dimension,
            x, y, z,
            destination.x, destination.y, destination.z,
            4);
        helper.assertTrue(registration.allowed(), "pair registration must not force-load or pre-authorize future destination state");

        Object wrongOwner = transfer(server, gateId, UUID.randomUUID(), 0, entity.getUUID(), server.getTickCount(), true);
        helper.assertTrue(!decision(wrongOwner).allowed()
                && "threshold_gate_owner_mismatch".equals(decision(wrongOwner).code()),
            "only the gate owner/authorized host context may settle this server-owned pair");
        helper.assertTrue(samePosition(entity, x, y, z), "owner denial must not move the entity");

        Object blocked = transfer(server, gateId, owner.getUUID(), 0, entity.getUUID(), server.getTickCount(), true);
        helper.assertTrue(!decision(blocked).allowed(), "blocked destination must fail closed");
        helper.assertTrue("collision_blocked".equals(decision(blocked).code()),
            "blocked gate destination must preserve the shared safe-destination denial code");
        helper.assertTrue(samePosition(entity, x, y, z), "blocked destination must not partially move the entity");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void throughputAndPlayerConsentAreEnforcedBeforeMovement(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(2, 2, 1));
        var otherPlayer = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        var level = helper.getLevel();
        UUID gateId = UUID.randomUUID();
        String dimension = level.dimension().location().toString();
        long nowTick = server.getTickCount();
        Vec3 firstDestination = helper.absoluteVec(new Vec3(6.5D, 2.0D, 1.5D));
        Vec3 playerDestination = helper.absoluteVec(new Vec3(8.5D, 2.0D, 1.5D));

        clearLanding(helper, new BlockPos(6, 2, 1));
        clearLanding(helper, new BlockPos(8, 2, 1));
        ArcanaDecision registration = registerPair(
            server, gateId, owner.getUUID(), dimension,
            first.getX(), first.getY(), first.getZ(),
            firstDestination.x, firstDestination.y, firstDestination.z,
            1);
        helper.assertTrue(registration.allowed(), "throughput=1 must be a valid bounded gate configuration");

        Object firstTransfer = transfer(server, gateId, owner.getUUID(), 0, first.getUUID(), nowTick, true);
        helper.assertTrue(decision(firstTransfer).allowed() && transferred(firstTransfer),
            "first transfer in the throughput window must succeed");
        helper.assertTrue(samePosition(first, firstDestination.x, firstDestination.y, firstDestination.z),
            "successful throughput fixture transfer must land at the absolute paired endpoint");

        double secondX = second.getX();
        double secondY = second.getY();
        double secondZ = second.getZ();
        Object overflow = transfer(server, gateId, owner.getUUID(), 0, second.getUUID(), nowTick, true);
        helper.assertTrue(!decision(overflow).allowed()
                && "threshold_gate_throughput".equals(decision(overflow).code()),
            "second transfer in a saturated window must fail closed");
        helper.assertTrue(samePosition(second, secondX, secondY, secondZ),
            "throughput denial must not move another entity");

        UUID playerGate = UUID.randomUUID();
        helper.assertTrue(registerPair(
            server, playerGate, owner.getUUID(), dimension,
            otherPlayer.getX(), otherPlayer.getY(), otherPlayer.getZ(),
            playerDestination.x, playerDestination.y, playerDestination.z,
            4).allowed(), "player-consent fixture pair must register");
        double playerX = otherPlayer.getX();
        double playerY = otherPlayer.getY();
        double playerZ = otherPlayer.getZ();
        Object noConsent = transfer(server, playerGate, owner.getUUID(), 0, otherPlayer.getUUID(), nowTick, false);
        helper.assertTrue(!decision(noConsent).allowed()
                && "threshold_gate_player_consent".equals(decision(noConsent).code()),
            "moving a different player through a gate requires explicit host/server consent");
        helper.assertTrue(samePosition(otherPlayer, playerX, playerY, playerZ),
            "consent denial must leave player position unchanged");
        helper.succeed();
    }

    private static ArcanaDecision registerPair(
        net.minecraft.server.MinecraftServer server,
        UUID gateId,
        UUID ownerId,
        String dimensionId,
        double ax, double ay, double az,
        double bx, double by, double bz,
        int maxPerSecond
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "registerPair",
            net.minecraft.server.MinecraftServer.class,
            UUID.class,
            UUID.class,
            String.class,
            double.class, double.class, double.class,
            double.class, double.class, double.class,
            int.class);
        return (ArcanaDecision) method.invoke(
            null, server, gateId, ownerId, dimensionId,
            ax, ay, az, bx, by, bz, maxPerSecond);
    }

    private static Object transfer(
        net.minecraft.server.MinecraftServer server,
        UUID gateId,
        UUID requestingOwnerId,
        int sourceIndex,
        UUID entityId,
        long nowTick,
        boolean playerConsent
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "transfer",
            net.minecraft.server.MinecraftServer.class,
            UUID.class,
            UUID.class,
            int.class,
            UUID.class,
            long.class,
            boolean.class);
        return method.invoke(null, server, gateId, requestingOwnerId, sourceIndex, entityId, nowTick, playerConsent);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean transferred(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("transferred").invoke(result);
    }

    private static boolean samePosition(net.minecraft.world.entity.Entity entity, double x, double y, double z) {
        return Math.abs(entity.getX() - x) < 0.001D
            && Math.abs(entity.getY() - y) < 0.001D
            && Math.abs(entity.getZ() - z) < 0.001D;
    }

    private static void clearLanding(GameTestHelper helper, BlockPos base) {
        helper.setBlock(base, Blocks.AIR);
        helper.setBlock(base.above(), Blocks.AIR);
    }
}
