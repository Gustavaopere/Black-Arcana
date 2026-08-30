package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class RiftBladesGameTests {
    private RiftBladesGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void markedStrikeDealsBoundedDamageAndUsesSafeLandingCandidate(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(7, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        float healthBefore = target.getHealth();
        double distanceBefore = caster.distanceToSqr(target);
        double landingX = target.getX() - 1.5D;
        double landingY = target.getY();
        double landingZ = target.getZ();

        Object result = resolveMarkedStrike(
            server,
            caster.getUUID(),
            target.getUUID(),
            3.0D,
            landingX,
            landingY,
            landingZ,
            8.0D);

        ArcanaDecision decision = decision(result);
        double dealt = damageDealt(result);
        helper.assertTrue(decision.allowed(), "eligible marked strike must be admitted");
        helper.assertTrue(dealt > 0.0D && dealt <= 3.0D,
            "Rift Blades must report only real bounded health loss");
        helper.assertTrue(target.getHealth() < healthBefore,
            "eligible marked strike must damage the resolved target");
        helper.assertTrue(gapClosed(result),
            "safe loaded landing candidate must allow optional gap-close; code=" + gapCloseCode(result));
        helper.assertTrue(caster.distanceToSqr(target) < distanceBefore,
            "successful gap-close must move the caster closer to the marked target");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void blockedLandingSkipsGapCloseWithoutRollingBackDamage(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(7, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        float healthBefore = target.getHealth();
        double casterXBefore = caster.getX();
        double casterYBefore = caster.getY();
        double casterZBefore = caster.getZ();
        double landingX = target.getX() - 1.5D;
        double landingY = target.getY();
        double landingZ = target.getZ();
        BlockPos blocked = BlockPos.containing(landingX, landingY, landingZ);
        helper.getLevel().setBlockAndUpdate(blocked, Blocks.STONE.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(blocked.above(), Blocks.STONE.defaultBlockState());

        Object result = resolveMarkedStrike(
            server,
            caster.getUUID(),
            target.getUUID(),
            3.0D,
            landingX,
            landingY,
            landingZ,
            8.0D);

        helper.assertTrue(decision(result).allowed(),
            "a blocked optional landing must not cancel an otherwise legal marked strike");
        helper.assertTrue(damageDealt(result) > 0.0D && target.getHealth() < healthBefore,
            "damage settlement must remain independent from optional displacement");
        helper.assertTrue(!gapClosed(result), "blocked destination must fail closed for displacement");
        helper.assertTrue(!gapCloseCode(result).isBlank(),
            "blocked displacement must expose a stable diagnostic reason");
        helper.assertTrue(Math.abs(caster.getX() - casterXBefore) < 0.01D
                && Math.abs(caster.getY() - casterYBefore) < 0.01D
                && Math.abs(caster.getZ() - casterZBefore) < 0.01D,
            "blocked gap-close must leave caster position unchanged");
        helper.succeed();
    }

    private static Object resolveMarkedStrike(
        MinecraftServer server,
        UUID casterId,
        UUID targetId,
        double requestedDamage,
        double landingX,
        double landingY,
        double landingZ,
        double maxGapCloseBlocks
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftRiftBladesRuntime");
        Method method = runtime.getMethod(
            "resolveMarkedStrike",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            double.class,
            double.class,
            double.class,
            double.class,
            double.class);
        return method.invoke(
            null,
            server,
            casterId,
            targetId,
            requestedDamage,
            landingX,
            landingY,
            landingZ,
            maxGapCloseBlocks);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static double damageDealt(Object result) throws Exception {
        return (double) result.getClass().getMethod("damageDealt").invoke(result);
    }

    private static boolean gapClosed(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("gapClosed").invoke(result);
    }

    private static String gapCloseCode(Object result) throws Exception {
        return (String) result.getClass().getMethod("gapCloseCode").invoke(result);
    }
}
