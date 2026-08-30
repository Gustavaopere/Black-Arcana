package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
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
    private static final BlockPos TARGET_POS = new BlockPos(0, 1, 0);
    private static final BlockPos CASTER_POS = new BlockPos(-4, 1, 0);

    private GazeOfStillnessGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void reciprocalFacingSuppressesHorizontalMovement(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        faceEachOther(caster, target);
        helper.assertTrue(helper.getBounds().contains(target.position()), "target fixture must start inside GameTest bounds");

        Object result = start(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            20L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        ArcanaDecision startDecision = decision(result);
        helper.assertTrue(startDecision.allowed(), "valid reciprocal Gaze must start; " + initialDiagnostic(startDecision, caster, target));

        target.setDeltaMovement(new Vec3(0.1D, 0.0D, 0.0D));
        helper.runAfterDelay(2L, () -> {
            helper.assertTrue(active(helper.getLevel().getServer(), target.getUUID()), "valid reciprocal Gaze must remain active");
            helper.assertTrue(target.isAlive() && !target.isRemoved(), "active Gaze must not remove its target");
            Vec3 movement = target.getDeltaMovement();
            helper.assertTrue(movement.x * movement.x + movement.z * movement.z < 1.0E-6D,
                "active Gaze must suppress horizontal movement at multiplier zero");
            helper.succeed();
        });
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void breakingReciprocalFacingEndsSuppression(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        faceEachOther(caster, target);

        Object result = start(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            20L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        ArcanaDecision startDecision = decision(result);
        helper.assertTrue(startDecision.allowed(), "fixture Gaze must start; " + initialDiagnostic(startDecision, caster, target));

        target.setYRot(-90.0F);
        target.setYHeadRot(-90.0F);
        target.setDeltaMovement(new Vec3(0.1D, 0.0D, 0.0D));
        helper.runAfterDelay(2L, () -> {
            helper.assertTrue(!active(helper.getLevel().getServer(), target.getUUID()),
                "breaking reciprocal facing must end control immediately");
            helper.assertTrue(target.isAlive() && !target.isRemoved(), "breaking Gaze must not remove the target");
            helper.assertTrue(Math.abs(target.getDeltaMovement().x) > 0.005D,
                "movement must not remain artificially suppressed after Gaze breaks");
            helper.succeed();
        });
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void durationAboveNoeticCeilingFailsClosed(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        faceEachOther(caster, target);

        Object result = start(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(),
            161L, 16.0D, 0.0D, 0.5D, 0.5D, 80L);
        helper.assertTrue(!decision(result).allowed(), "Gaze must reject durations above 160 ticks");
        helper.assertTrue("gaze_stillness_duration".equals(decision(result).code()),
            "duration denial must expose the canonical Gaze diagnostic");
        helper.succeed();
    }

    private static LivingEntity target(GameTestHelper helper) {
        var target = helper.spawnWithNoFreeWill(EntityType.SHEEP, TARGET_POS);
        target.setNoGravity(true);
        return target;
    }

    private static Object start(MinecraftServer server, UUID casterId, UUID targetId,
                                long durationTicks, double maxRange, double movementMultiplier,
                                double playerMultiplier, double bossMultiplier, long immunityTicks) throws Exception {
        Class<?> runtime = Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftGazeOfStillnessRuntime");
        Method method = runtime.getMethod("start", MinecraftServer.class, UUID.class, UUID.class,
            long.class, double.class, double.class, double.class, double.class, long.class);
        return method.invoke(null, server, casterId, targetId, durationTicks, maxRange, movementMultiplier,
            playerMultiplier, bossMultiplier, immunityTicks);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean active(MinecraftServer server, UUID targetId) {
        try {
            Class<?> runtime = Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftGazeOfStillnessRuntime");
            return (boolean) runtime.getMethod("isActive", MinecraftServer.class, UUID.class).invoke(null, server, targetId);
        } catch (ReflectiveOperationException exception) {
            throw new IllegalStateException(exception);
        }
    }

    private static String initialDiagnostic(ArcanaDecision decision, LivingEntity caster, LivingEntity target) {
        return "code=" + decision.code()
            + ", casterPos=" + caster.position()
            + ", targetPos=" + target.position()
            + ", casterAlive=" + caster.isAlive()
            + ", targetAlive=" + target.isAlive()
            + ", distance=" + Math.sqrt(caster.distanceToSqr(target))
            + ", casterLos=" + caster.hasLineOfSight(target)
            + ", targetLos=" + target.hasLineOfSight(caster)
            + ", casterDot=" + facingDot(caster, target)
            + ", targetDot=" + facingDot(target, caster);
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
