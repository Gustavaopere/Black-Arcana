package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreGameTests {
    private BlackPyreGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void safeModeEntityDamageWorksWithoutTerrainMutation(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        float healthBefore = target.getHealth();

        Object result = igniteDefault(
            server,
            caster.getUUID(),
            List.of(target.getUUID()),
            3.0D,
            false);

        helper.assertTrue(decision(result).allowed(), "eligible Black Pyre entity damage must settle");
        helper.assertTrue(damagedTargets(result) == 1, "one eligible target must be damaged once");
        helper.assertTrue(damageDealt(result) > 0.0D && damageDealt(result) <= 3.0D,
            "Black Pyre must report only bounded real health loss");
        helper.assertTrue(target.getHealth() < healthBefore, "eligible Black Pyre target must lose health");
        helper.assertTrue(!terrainApplied(result), "safe-mode cast must not mutate terrain");
        helper.assertTrue("terrain_not_requested".equals(terrainCode(result)),
            "safe-mode cast must report that terrain was not requested");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void alliedTargetFailsClosedForBlackPyreDamage(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        Scoreboard scoreboard = helper.getLevel().getScoreboard();
        PlayerTeam existing = scoreboard.getPlayerTeam("ba_gt_pyre_ally");
        if (existing != null) scoreboard.removePlayerTeam(existing);
        PlayerTeam team = scoreboard.addPlayerTeam("ba_gt_pyre_ally");
        float healthBefore = target.getHealth();
        try {
            scoreboard.addPlayerToTeam(caster.getScoreboardName(), team);
            scoreboard.addPlayerToTeam(target.getScoreboardName(), team);

            Object result = igniteDefault(
                helper.getLevel().getServer(),
                caster.getUUID(),
                List.of(target.getUUID()),
                3.0D,
                false);

            helper.assertTrue(!decision(result).allowed(), "allied target must be rejected by Black Pyre");
            helper.assertTrue(damagedTargets(result) == 0, "allied target must not count as damaged");
            helper.assertTrue(damageDealt(result) == 0.0D, "allied target must not lose Black Pyre health");
            helper.assertTrue(Math.abs(target.getHealth() - healthBefore) < 0.001F,
                "allied target health must remain unchanged");
        } finally {
            scoreboard.removePlayerTeam(team);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void terrainRequestDegradesExplicitlyUntilBlockProtectionContractExists(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        float healthBefore = target.getHealth();

        Object result = igniteDefault(
            helper.getLevel().getServer(),
            caster.getUUID(),
            List.of(target.getUUID()),
            3.0D,
            true);

        helper.assertTrue(decision(result).allowed(),
            "terrain presentation failure must not roll back independently authorized entity damage");
        helper.assertTrue(target.getHealth() < healthBefore,
            "Black Pyre entity damage must remain functional when terrain mutation fails closed");
        helper.assertTrue(!terrainApplied(result),
            "terrain must remain untouched without an authoritative block-protection route");
        helper.assertTrue("black_pyre_terrain_protection_contract_missing".equals(terrainCode(result)),
            "terrain degradation must expose the frozen Stage 04 contract gap explicitly");
        helper.succeed();
    }

    private static Object igniteDefault(
            MinecraftServer server,
            UUID casterId,
            List<UUID> targetIds,
            double requestedDamage,
            boolean terrainRequested
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftBlackPyreRuntime");
        Method method = runtime.getMethod(
            "igniteDefault",
            MinecraftServer.class,
            UUID.class,
            List.class,
            double.class,
            boolean.class);
        return method.invoke(null, server, casterId, targetIds, requestedDamage, terrainRequested);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static int damagedTargets(Object result) throws Exception {
        return (int) result.getClass().getMethod("damagedTargets").invoke(result);
    }

    private static double damageDealt(Object result) throws Exception {
        return (double) result.getClass().getMethod("damageDealt").invoke(result);
    }

    private static boolean terrainApplied(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("terrainApplied").invoke(result);
    }

    private static String terrainCode(Object result) throws Exception {
        return (String) result.getClass().getMethod("terrainCode").invoke(result);
    }
}
