package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
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
    private OccultAppraisalGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void appraisalReturnsOnlyApprovedMetadata(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        place(helper, caster, new BlockPos(3, 2, 1));
        place(helper, target, new BlockPos(5, 2, 1));

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            16.0D,
            Set.of("health", "held_item", "full_nbt", "container_inventory"));

        helper.assertTrue(decision(result).allowed(),
            "loaded in-range visible target must be eligible for Occult Appraisal");
        Map<String, String> metadata = metadata(result);
        helper.assertTrue(metadata.keySet().equals(Set.of("health", "held_item")),
            "Occult Appraisal must return only server-approved requested metadata fields; actual=" + metadata.keySet());
        helper.assertTrue(!metadata.containsKey("full_nbt") && !metadata.containsKey("container_inventory"),
            "Occult Appraisal must never expose arbitrary NBT or container inventory fields");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void appraisalFailsClosedOutsideRequestedRange(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        place(helper, caster, new BlockPos(1, 2, 1));
        place(helper, target, new BlockPos(10, 2, 1));

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            4.0D,
            Set.of("health"));

        helper.assertTrue(!decision(result).allowed(),
            "Occult Appraisal must fail closed when the loaded target is outside configured range");
        helper.assertTrue("occult_appraisal_range".equals(decision(result).code()),
            "range denial must expose the canonical Occult Appraisal diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "denied Occult Appraisal must not leak metadata");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void appraisalFailsClosedWhenLineOfSightIsBlocked(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        BlockPos casterPos = new BlockPos(2, 2, 1);
        BlockPos targetPos = new BlockPos(6, 2, 1);
        place(helper, caster, casterPos);
        place(helper, target, targetPos);

        BlockPos wall = helper.absolutePos(new BlockPos(4, 2, 1));
        helper.getLevel().setBlockAndUpdate(wall, Blocks.STONE.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(wall.above(), Blocks.STONE.defaultBlockState());

        Object result = appraise(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            16.0D,
            Set.of("health", "held_item"));

        helper.assertTrue(!decision(result).allowed(),
            "Occult Appraisal must fail closed when server LOS is blocked");
        helper.assertTrue("occult_appraisal_los".equals(decision(result).code()),
            "blocked LOS must expose the canonical Occult Appraisal diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "LOS-denied Occult Appraisal must not leak metadata");
        helper.succeed();
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
