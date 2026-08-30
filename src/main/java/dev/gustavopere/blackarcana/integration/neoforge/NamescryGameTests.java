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
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class NamescryGameTests {
    private NamescryGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void namescryAllowsLoadedNonPlayerWithinRange(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        place(helper, caster, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(6, 2, 1));

        Object result = namescry(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            16.0D,
            Set.of("health", "full_nbt"));

        helper.assertTrue(decision(result).allowed(),
            "Namescry must allow a loaded same-dimension non-player target inside configured range");
        Map<String, String> metadata = metadata(result);
        helper.assertTrue(metadata.keySet().equals(Set.of("health")),
            "Namescry must expose only approved requested metadata; actual=" + metadata.keySet());
        helper.assertTrue(!metadata.containsKey("full_nbt"),
            "Namescry must never expose arbitrary NBT");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void namescryDeniesPlayerWithoutServerAuthorization(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        place(helper, caster, new BlockPos(2, 2, 1));
        place(helper, target, new BlockPos(5, 2, 1));

        Object result = namescry(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            16.0D,
            Set.of("health"));

        helper.assertTrue(!decision(result).allowed(),
            "Namescry must deny player targets unless consent/covenant authorization is resolved server-side");
        helper.assertTrue("namescry_player_authorization".equals(decision(result).code()),
            "player privacy denial must expose the canonical Namescry diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "denied player Namescry must not leak metadata");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void namescryFailsClosedOutsideRange(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        place(helper, caster, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(10, 2, 1));

        Object result = namescry(
            helper.getLevel().getServer(),
            caster.getUUID(),
            target.getUUID(),
            4.0D,
            Set.of("health"));

        helper.assertTrue(!decision(result).allowed(),
            "Namescry must fail closed when the target is outside configured range");
        helper.assertTrue("namescry_range".equals(decision(result).code()),
            "range denial must expose the canonical Namescry diagnostic");
        helper.assertTrue(metadata(result).isEmpty(),
            "denied Namescry must not leak metadata");
        helper.succeed();
    }

    private static Object namescry(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            double maxRange,
            Set<String> requestedFields
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftNamescryRuntime");
        Method method = runtime.getMethod(
            "namescry",
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
