package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SanguineHarvestGameTests {
    private SanguineHarvestGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void boundedHarvestSettlesActualHealthAndRespectsRangeAndAntiFarmWeight(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(4, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(6, 2, 1));
        var far = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(20, 2, 1));
        helper.assertTrue(first.getArmorValue() == 0 && second.getArmorValue() == 0 && far.getArmorValue() == 0,
            "fixture targets must not add armor mitigation");

        MinecraftServer server = helper.getLevel().getServer();
        Object result = harvest(
            server,
            caster.getUUID(),
            List.of(first.getUUID(), second.getUUID(), far.getUUID()),
            2,
            5.0D,
            4.0D,
            8.0D,
            Map.of(first.getUUID(), 1.0D, second.getUUID(), 0.50D, far.getUUID(), 1.0D));

        ArcanaDecision decision = (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
        double totalYield = (double) result.getClass().getMethod("totalYield").invoke(result);
        int drainedTargets = (int) result.getClass().getMethod("drainedTargets").invoke(result);

        helper.assertTrue(decision.allowed(), "eligible loaded Sanguine Harvest pulse must settle");
        helper.assertTrue(close(totalYield, 5.0D), "actual health loss must equal the bounded harvest yield");
        helper.assertTrue(drainedTargets == 2, "only the two eligible in-range targets may be drained");
        helper.assertTrue(close(first.getHealth(), 6.0D), "first target must lose the full 4 HP weighted drain");
        helper.assertTrue(close(second.getHealth(), 9.0D), "second target must lose only the 1 HP remaining budget");
        helper.assertTrue(close(far.getHealth(), 10.0D), "out-of-range target must remain untouched");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void playerAndBossTargetsAreExcludedByDefault(GameTestHelper helper) throws Exception {
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var ordinary = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(4, 2, 1));
        var boss = helper.spawnWithNoFreeWill(EntityType.WITHER, new BlockPos(6, 2, 1));
        var player = helper.makeMockServerPlayerInLevel();
        player.setGameMode(GameType.SURVIVAL);
        player.getAbilities().invulnerable = false;
        player.getAbilities().instabuild = false;
        player.onUpdateAbilities();
        player.setPos(caster.getX() + 2.0D, caster.getY(), caster.getZ() + 2.0D);

        double bossBefore = boss.getHealth();
        double playerBefore = player.getHealth();
        MinecraftServer server = helper.getLevel().getServer();
        Object result = harvest(
            server,
            caster.getUUID(),
            List.of(player.getUUID(), boss.getUUID(), ordinary.getUUID()),
            3,
            12.0D,
            4.0D,
            12.0D,
            Map.of(player.getUUID(), 1.0D, boss.getUUID(), 1.0D, ordinary.getUUID(), 1.0D));

        ArcanaDecision decision = (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
        double totalYield = (double) result.getClass().getMethod("totalYield").invoke(result);
        int drainedTargets = (int) result.getClass().getMethod("drainedTargets").invoke(result);

        helper.assertTrue(decision.allowed(), "mixed pulse may continue when conservative policy excludes unsafe targets");
        helper.assertTrue(close(totalYield, 4.0D), "only the ordinary eligible target may contribute yield");
        helper.assertTrue(drainedTargets == 1, "player and boss targets must not count as drained");
        helper.assertTrue(close(ordinary.getHealth(), 6.0D), "ordinary target must be drained normally");
        helper.assertTrue(close(player.getHealth(), playerBefore), "hostile player drain must be disabled by default");
        helper.assertTrue(close(boss.getHealth(), bossBefore), "boss drain must be disabled by default");
        helper.succeed();
    }

    private static Object harvest(
        MinecraftServer server,
        UUID casterId,
        List<UUID> targetIds,
        int maxTargets,
        double maxTotalYield,
        double maxDrainPerTarget,
        double range,
        Map<UUID, Double> antiFarmWeights
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSanguineHarvestRuntime");
        Method harvest = runtime.getMethod(
            "harvest",
            MinecraftServer.class,
            UUID.class,
            List.class,
            int.class,
            double.class,
            double.class,
            double.class,
            Map.class);
        return harvest.invoke(
            null,
            server,
            casterId,
            targetIds,
            maxTargets,
            maxTotalYield,
            maxDrainPerTarget,
            range,
            antiFarmWeights);
    }

    private static boolean close(double actual, double expected) {
        return Math.abs(actual - expected) <= 0.01D;
    }
}
