package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class VectorReversalGameTests {
    private VectorReversalGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void defaultVectorReversalAppliesBoundedImpulseOncePerTarget(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();

        Object result = applyDefault(
            server,
            caster.getUUID(),
            List.of(target.getUUID(), target.getUUID()),
            10.0D,
            0.0D,
            0.0D);

        helper.assertTrue(decision(result).allowed(), "eligible Vector Reversal must settle");
        helper.assertTrue(affectedTargets(result) == 1,
            "duplicate target UUIDs must be deduplicated before displacement");
        helper.assertTrue(target.getDeltaMovement().length() <= 2.500001D,
            "Vector Reversal velocity must respect the configured speed clamp");
        helper.assertTrue(target.getDeltaMovement().x > 1.49D && target.getDeltaMovement().x < 1.51D,
            "duplicate target must receive exactly one default 1.5 impulse");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void invalidDirectionFailsClosedWithoutMotion(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();

        Object result = applyDefault(
            server,
            caster.getUUID(),
            List.of(target.getUUID()),
            0.0D,
            0.0D,
            0.0D);

        helper.assertTrue(!decision(result).allowed(), "zero vector must fail closed");
        helper.assertTrue(affectedTargets(result) == 0, "failed vector must not affect targets");
        helper.assertTrue(target.getDeltaMovement().lengthSqr() < 1.0E-12D,
            "failed vector must leave target motion unchanged");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void targetCapPreventsFifthSettlement(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 2));
        var third = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        var fourth = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 2));
        var fifth = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 3));
        MinecraftServer server = helper.getLevel().getServer();

        Object result = applyDefault(
            server,
            caster.getUUID(),
            List.of(first.getUUID(), second.getUUID(), third.getUUID(), fourth.getUUID(), fifth.getUUID()),
            1.0D,
            0.0D,
            0.0D);

        helper.assertTrue(decision(result).allowed(), "first four eligible targets must settle");
        helper.assertTrue(affectedTargets(result) == 4, "hard Vector Reversal target cap must be four");
        helper.assertTrue(fifth.getDeltaMovement().lengthSqr() < 1.0E-12D,
            "fifth supplied target must remain untouched by the bounded settlement");
        helper.succeed();
    }

    private static Object applyDefault(
            MinecraftServer server,
            UUID casterId,
            List<UUID> targetIds,
            double x,
            double y,
            double z
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftVectorReversalRuntime");
        Method method = runtime.getMethod(
            "applyDefault",
            MinecraftServer.class,
            UUID.class,
            List.class,
            double.class,
            double.class,
            double.class);
        return method.invoke(null, server, casterId, targetIds, x, y, z);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static int affectedTargets(Object result) throws Exception {
        return (int) result.getClass().getMethod("affectedTargets").invoke(result);
    }
}
