package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class OccultAppraisalGameTests {
    private static final BlockPos TARGET_POS = new BlockPos(0, 1, 0);
    private static final BlockPos CASTER_POS = new BlockPos(-4, 1, 0);
    private static final double TEST_RANGE = 16.0D;

    private OccultAppraisalGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void appraisalReturnsOnlyApprovedSanitizedMetadata(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);
        target.setHealth(Math.max(1.0F, target.getMaxHealth() - 2.0F));
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200, 1));
        target.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.DIAMOND_SWORD, 1));

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            TEST_RANGE,
            Set.of("health", "status_effects", "held_item", "full_nbt", "container_inventory", "capabilities"));

        helper.assertTrue(decision(result).allowed(),
            "loaded in-range non-player target must be eligible for approved Occult Appraisal metadata");
        Map<String, String> metadata = metadata(result);
        helper.assertTrue(metadata.keySet().equals(Set.of("health", "status_effects", "held_item")),
            "Occult Appraisal must return only approved requested metadata fields; actual=" + metadata.keySet());
        helper.assertTrue("minecraft:diamond_sword".equals(metadata.get("held_item")),
            "held-item projection must expose only the registry id, not ItemStack components");
        helper.assertTrue(!metadata.containsKey("full_nbt")
                && !metadata.containsKey("container_inventory")
                && !metadata.containsKey("capabilities"),
            "Occult Appraisal must never expose arbitrary NBT, container inventory or capability fields");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void playerTargetsFailClosedWithoutExplicitPrivacyPolicy(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        place(helper, caster, CASTER_POS);
        place(helper, target, TARGET_POS);

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            TEST_RANGE,
            Set.of("health", "held_item"));

        helper.assertTrue(!decision(result).allowed(),
            "player appraisal must fail closed until an explicit server privacy/consent policy is wired");
        helper.assertTrue("occult_appraisal_player_privacy".equals(decision(result).code()),
            "player privacy denial must expose the canonical Occult Appraisal diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "privacy-denied player appraisal must not leak metadata");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void unknownOnlyRequestFailsClosedWithoutMetadata(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            TEST_RANGE,
            Set.of("full_nbt", "container_inventory", "capabilities"));

        helper.assertTrue(!decision(result).allowed(),
            "request containing no approved metadata field must fail closed");
        helper.assertTrue("occult_appraisal_no_approved_metadata".equals(decision(result).code()),
            "empty whitelist projection must expose the canonical diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "unknown-only appraisal must expose no metadata");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void invalidRangeAndBlockedLosFailClosed(GameTestHelper helper) throws Exception {
        clearSightCorridor(helper);
        var caster = helper.makeMockServerPlayerInLevel();
        var target = target(helper);
        place(helper, caster, CASTER_POS);

        Object invalidRange = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            Double.NaN,
            Set.of("health"));
        helper.assertTrue(!decision(invalidRange).allowed(),
            "non-finite appraisal range must fail closed");
        helper.assertTrue("occult_appraisal_range_config".equals(decision(invalidRange).code()),
            "invalid range must expose the canonical Occult Appraisal diagnostic");
        helper.assertTrue(metadata(invalidRange).isEmpty(),
            "invalid range appraisal must not leak metadata");

        helper.getLevel().setBlockAndUpdate(helper.absolutePos(new BlockPos(-2, 1, 0)), Blocks.STONE.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(helper.absolutePos(new BlockPos(-2, 2, 0)), Blocks.STONE.defaultBlockState());
        Object blockedLos = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            TEST_RANGE,
            Set.of("health"));
        helper.assertTrue(!decision(blockedLos).allowed(),
            "Occult Appraisal must fail closed when server LOS is blocked");
        helper.assertTrue("occult_appraisal_los".equals(decision(blockedLos).code()),
            "blocked LOS must expose the canonical Occult Appraisal diagnostic");
        helper.assertTrue(metadata(blockedLos).isEmpty(),
            "LOS-denied Occult Appraisal must not leak metadata");
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

    private static Object appraise(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            double maxRange,
            Set<String> requestedFields
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftOccultAppraisalRuntime");
        Method method = runtime.getMethod(
            "appraise",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            double.class,
            Set.class);
        return method.invoke(null, server, casterId, targetId, maxRange, requestedFields);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, String> metadata(Object result) throws Exception {
        return (Map<String, String>) result.getClass().getMethod("metadata").invoke(result);
    }

    private static void place(GameTestHelper helper, net.minecraft.world.entity.Entity entity, BlockPos relative) {
        BlockPos absolute = helper.absolutePos(relative);
        entity.setPos(absolute.getX() + 0.5D, absolute.getY(), absolute.getZ() + 0.5D);
    }
}
