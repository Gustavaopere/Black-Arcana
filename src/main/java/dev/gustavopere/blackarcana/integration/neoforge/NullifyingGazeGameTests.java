package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.Optional;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class NullifyingGazeGameTests {
    private static final BlockPos TARGET_POS = new BlockPos(0, 1, 0);
    private static final BlockPos CASTER_POS = new BlockPos(-4, 1, 0);
    private static final ResourceLocation SPEED = ResourceLocation.fromNamespaceAndPath("minecraft", "speed");
    private static final ResourceLocation STRENGTH = ResourceLocation.fromNamespaceAndPath("minecraft", "strength");

    private NullifyingGazeGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void registeredEffectRemovedUnknownEffectUntouched(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200));
        target.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 200));

        reset(helper.getLevel().getServer());
        registerNullifiable(helper.getLevel().getServer(), SPEED);
        Object result = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.0D);

        helper.assertTrue(decision(result).allowed(), "registered nullifiable effect must be removable");
        helper.assertTrue(!target.hasEffect(MobEffects.MOVEMENT_SPEED), "registered speed effect must be removed");
        helper.assertTrue(target.hasEffect(MobEffects.DAMAGE_BOOST), "unknown strength effect must remain untouched");
        helper.assertTrue(removedEffect(result).filter(SPEED::equals).isPresent(), "result must identify the removed effect");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void twoEligibleEffectsRemoveExactlyOne(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200));
        target.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 200));

        reset(helper.getLevel().getServer());
        registerNullifiable(helper.getLevel().getServer(), SPEED);
        registerNullifiable(helper.getLevel().getServer(), STRENGTH);
        Object result = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.0D);

        helper.assertTrue(decision(result).allowed(), "one eligible effect must be nullified");
        int remaining = (target.hasEffect(MobEffects.MOVEMENT_SPEED) ? 1 : 0)
            + (target.hasEffect(MobEffects.DAMAGE_BOOST) ? 1 : 0);
        helper.assertTrue(remaining == 1, "Nullifying Gaze must remove exactly one effect per cast");
        helper.assertTrue(removedEffect(result).isPresent(), "successful result must identify one removed effect");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void unknownEffectFailsClosedWithoutMutation(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200));

        reset(helper.getLevel().getServer());
        Object result = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.0D);

        helper.assertTrue(!decision(result).allowed(), "unknown effect must fail closed");
        helper.assertTrue("nullifying_gaze_no_eligible_effect".equals(decision(result).code()),
            "unknown effect denial must expose canonical diagnostic");
        helper.assertTrue(target.hasEffect(MobEffects.MOVEMENT_SPEED), "unknown effect must remain untouched");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void protectedEffectOverridesNullifiableRegistration(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200));

        reset(helper.getLevel().getServer());
        registerNullifiable(helper.getLevel().getServer(), SPEED);
        registerProtected(helper.getLevel().getServer(), SPEED);
        Object result = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.0D);

        helper.assertTrue(!decision(result).allowed(), "protected effect must not be nullified");
        helper.assertTrue(target.hasEffect(MobEffects.MOVEMENT_SPEED), "protected effect must remain untouched");
        helper.assertTrue(removedEffect(result).isEmpty(), "denied result must not report a removed effect");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void invalidRangeAndBlockedLosDoNotMutateTarget(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200));

        reset(helper.getLevel().getServer());
        registerNullifiable(helper.getLevel().getServer(), SPEED);
        Object invalidRange = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.01D);
        helper.assertTrue(!decision(invalidRange).allowed(), "range above hard ceiling must fail closed");
        helper.assertTrue("nullifying_gaze_range_config".equals(decision(invalidRange).code()),
            "range ceiling denial must expose canonical diagnostic");
        helper.assertTrue(target.hasEffect(MobEffects.MOVEMENT_SPEED), "invalid range must not mutate target effects");

        helper.getLevel().setBlockAndUpdate(helper.absolutePos(new BlockPos(-2, 1, 0)), Blocks.STONE.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(helper.absolutePos(new BlockPos(-2, 2, 0)), Blocks.STONE.defaultBlockState());
        Object blockedLos = nullify(helper.getLevel().getServer(), caster.getUUID(), target.getUUID(), 14.0D);
        helper.assertTrue(!decision(blockedLos).allowed(), "blocked LOS must deny Nullifying Gaze");
        helper.assertTrue("nullifying_gaze_los".equals(decision(blockedLos).code()),
            "LOS denial must expose canonical diagnostic");
        helper.assertTrue(target.hasEffect(MobEffects.MOVEMENT_SPEED), "blocked LOS must not mutate target effects");
        helper.succeed();
    }

    private static LivingEntity target(GameTestHelper helper) {
        var target = helper.spawnWithNoFreeWill(EntityType.SHEEP, TARGET_POS);
        target.setNoGravity(true);
        return target;
    }

    private static void clearSightCorridor(GameTestHelper helper) {
        for (int x = CASTER_POS.getX(); x <= TARGET_POS.getX(); x++) {
            for (int y = 1; y <= 2; y++) {
                helper.getLevel().setBlockAndUpdate(helper.absolutePos(new BlockPos(x, y, 0)), Blocks.AIR.defaultBlockState());
            }
        }
    }

    private static void place(GameTestHelper helper, net.minecraft.world.entity.Entity entity, BlockPos relative) {
        BlockPos absolute = helper.absolutePos(relative);
        entity.setPos(absolute.getX() + 0.5D, absolute.getY(), absolute.getZ() + 0.5D);
    }

    private static Object nullify(MinecraftServer server, UUID casterId, UUID targetId, double maxRange) throws Exception {
        Class<?> runtime = runtime();
        Method method = runtime.getMethod("nullify", MinecraftServer.class, UUID.class, UUID.class, double.class);
        return method.invoke(null, server, casterId, targetId, maxRange);
    }

    private static void registerNullifiable(MinecraftServer server, ResourceLocation effectId) throws Exception {
        runtime().getMethod("registerNullifiableEffect", MinecraftServer.class, ResourceLocation.class)
            .invoke(null, server, effectId);
    }

    private static void registerProtected(MinecraftServer server, ResourceLocation effectId) throws Exception {
        runtime().getMethod("registerProtectedEffect", MinecraftServer.class, ResourceLocation.class)
            .invoke(null, server, effectId);
    }

    private static void reset(MinecraftServer server) throws Exception {
        runtime().getMethod("resetEffectPolicyForTests", MinecraftServer.class).invoke(null, server);
    }

    private static Class<?> runtime() throws ClassNotFoundException {
        return Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftNullifyingGazeRuntime");
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    @SuppressWarnings("unchecked")
    private static Optional<ResourceLocation> removedEffect(Object result) throws Exception {
        return (Optional<ResourceLocation>) result.getClass().getMethod("removedEffectId").invoke(result);
    }
}
