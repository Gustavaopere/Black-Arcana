package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class GazeOfStillnessGameTests {
    private GazeOfStillnessGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void reciprocalFacingSuppressesHorizontalMovement(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(6, 2, 1));
        place(helper, caster, new BlockPos(2, 2, 1));
        faceEachOther(caster, target);

        Object result = start(
            helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            20L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        helper.assertTrue(decision(result).allowed(),
            "reciprocal facing with LOS must start Gaze of Stillness on an authorized ordinary target");

        target.setDeltaMovement(new Vec3(0.8D, 0.0D, 0.4D));
        helper.runAfterDelay(2L, () -> {
            helper.assertTrue(active(helper.getLevel().getServer(), target.getUUID()),
                "valid reciprocal gaze must remain active during its bounded duration; "
                    + diagnostic(helper.getLevel().getServer(), caster, target));
            Vec3 movement = target.getDeltaMovement();
            helper.assertTrue(movement.x * movement.x + movement.z * movement.z < 1.0E-6D,
                "active Gaze of Stillness must suppress horizontal movement at the configured multiplier");
            helper.succeed();
        });
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void breakingReciprocalFacingEndsSuppression(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(6, 2, 1));
        place(helper, caster, new BlockPos(2, 2, 1));
        faceEachOther(caster, target);

        Object result = start(
            helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            20L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        helper.assertTrue(decision(result).allowed(), "fixture gaze must start");

        target.setYRot(-90.0F);
        target.setYHeadRot(-90.0F);
        target.setDeltaMovement(new Vec3(0.8D, 0.0D, 0.0D));
        helper.runAfterDelay(2L, () -> {
            helper.assertTrue(!active(helper.getLevel().getServer(), target.getUUID()),
                "breaking reciprocal facing must end the control session immediately");
            helper.assertTrue(Math.abs(target.getDeltaMovement().x) > 0.05D,
                "movement must not remain artificially suppressed after gaze breaks");
            helper.succeed();
        });
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void durationAboveNoeticCeilingFailsClosed(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(6, 2, 1));
        place(helper, caster, new BlockPos(2, 2, 1));
        faceEachOther(caster, target);

        Object result = start(
            helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            161L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        helper.assertTrue(!decision(result).allowed(),
            "Gaze of Stillness must reject durations above the frozen 160-tick safety ceiling");
        helper.assertTrue("gaze_stillness_duration".equals(decision(result).code()),
            "duration denial must expose the canonical Gaze diagnostic");
        helper.succeed();
    }

    private static Object start(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            long durationTicks,
            double maxRange,
            double horizontalMovementMultiplier,
            double playerDurationMultiplier,
            double bossDurationMultiplier,
            long playerImmunityTicks
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftGazeOfStillnessRuntime");
        Method method = runtime.getMethod(
            "start",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            long.class,
            double.class,
            double.class,
            double.class,
            double.class,
            long.class);
        return method.invoke(null, server, casterId, targetId, durationTicks, maxRange,
            horizontalMovementMultiplier, playerDurationMultiplier, bossDurationMultiplier, playerImmunityTicks);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean active(MinecraftServer server, UUID targetId) {
        try {
            Class<?> runtime = Class.forName(
                "dev.gustavopere.blackarcana.integration.neoforge.MinecraftGazeOfStillnessRuntime");
            return (boolean) runtime.getMethod("isActive", MinecraftServer.class, UUID.class)
                .invoke(null, server, targetId);
        } catch (ReflectiveOperationException exception) {
            throw new IllegalStateException(exception);
        }
    }

    private static String diagnostic(MinecraftServer server, LivingEntity caster, LivingEntity target) {
        boolean sameLevel = caster.level() == target.level();
        double distance = Math.sqrt(caster.distanceToSqr(target));
        boolean casterLos = caster.hasLineOfSight(target);
        boolean targetLos = target.hasLineOfSight(caster);
        double casterDot = facingDot(caster, target);
        double targetDot = facingDot(target, caster);
        String authorization = "runtime-missing";
        if (sameLevel && caster.level() instanceof ServerLevel level) {
            var runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
            if (runtime != null) {
                var facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
                var decision = runtime.entityInteractionAdmission().authorize(
                    EntityInteractionType.CONTROL,
                    facts,
                    new ProtectionQuery(
                        caster.getUUID(),
                        level.dimension().location().toString(),
                        target.getUUID().toString(),
                        EntityInteractionType.CONTROL)).decision();
                authorization = decision.allowed() ? "allowed" : decision.code();
            }
        }
        return "casterAlive=" + caster.isAlive()
            + ", targetAlive=" + target.isAlive()
            + ", sameLevel=" + sameLevel
            + ", distance=" + distance
            + ", casterLos=" + casterLos
            + ", targetLos=" + targetLos
            + ", casterDot=" + casterDot
            + ", targetDot=" + targetDot
            + ", casterYaw=" + caster.getYRot()
            + ", casterHeadYaw=" + caster.getYHeadRot()
            + ", targetYaw=" + target.getYRot()
            + ", targetHeadYaw=" + target.getYHeadRot()
            + ", authorization=" + authorization;
    }

    private static double facingDot(LivingEntity source, LivingEntity target) {
        Vec3 direction = target.getEyePosition().subtract(source.getEyePosition());
        double lengthSquared = direction.lengthSqr();
        if (!Double.isFinite(lengthSquared) || lengthSquared <= 1.0E-12D) return Double.NaN;
        return source.getLookAngle().dot(direction.scale(1.0D / Math.sqrt(lengthSquared)));
    }

    private static void faceEachOther(LivingEntity caster, LivingEntity target) {
        caster.setYRot(-90.0F);
        caster.setYHeadRot(-90.0F);
        target.setYRot(90.0F);
        target.setYHeadRot(90.0F);
    }

    private static void place(GameTestHelper helper, net.minecraft.world.entity.Entity entity, BlockPos relative) {
        BlockPos absolute = helper.absolutePos(relative);
        entity.setPos(absolute.getX() + 0.5D, absolute.getY(), absolute.getZ() + 0.5D);
    }
}
