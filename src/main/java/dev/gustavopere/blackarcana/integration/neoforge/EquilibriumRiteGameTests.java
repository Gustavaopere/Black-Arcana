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
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class EquilibriumRiteGameTests {
    private EquilibriumRiteGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void transferConservesHealthAndRespectsCapacityAndFloor(GameTestHelper helper) throws Exception {
        var source = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(5, 2, 1));
        source.setHealth(10.0F);
        target.setHealth(2.0F);

        MinecraftServer server = helper.getLevel().getServer();
        Object result = transfer(server, source.getUUID(), target.getUUID(), 8.0D, 1.0D);
        ArcanaDecision decision = decision(result);
        double transferred = transferred(result);

        helper.assertTrue(decision.allowed(), "eligible loaded living endpoints must transfer health");
        helper.assertTrue(transferred == 8.0D, "transfer must use the bounded requested amount");
        helper.assertTrue(source.getHealth() == 2.0F, "source health must decrease by the exact transfer");
        helper.assertTrue(target.getHealth() == 10.0F, "target health must not over-heal past capacity");
        helper.assertTrue(source.getHealth() + target.getHealth() == 12.0F, "Equilibrium Rite must not create health");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void hostilePlayerHealthExchangeIsDisabledByDefault(GameTestHelper helper) throws Exception {
        var source = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.makeMockServerPlayerInLevel();
        target.setGameMode(GameType.SURVIVAL);
        target.getAbilities().invulnerable = false;
        target.getAbilities().instabuild = false;
        target.onUpdateAbilities();

        MinecraftServer server = helper.getLevel().getServer();
        Object result = transfer(server, source.getUUID(), target.getUUID(), 4.0D, 1.0D);
        ArcanaDecision decision = decision(result);

        helper.assertTrue(!decision.allowed(), "hostile player health exchange must be disabled by default");
        helper.assertTrue("equilibrium_player_target_disabled".equals(decision.code()),
            "player denial must use the explicit Equilibrium policy code");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void bossHealthExchangeIsDisabledByDefault(GameTestHelper helper) throws Exception {
        var source = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.WITHER, new BlockPos(5, 2, 1));

        MinecraftServer server = helper.getLevel().getServer();
        Object result = transfer(server, source.getUUID(), target.getUUID(), 4.0D, 1.0D);
        ArcanaDecision decision = decision(result);

        helper.assertTrue(!decision.allowed(), "boss health exchange must be disabled by default");
        helper.assertTrue("equilibrium_boss_target_disabled".equals(decision.code()),
            "boss denial must use the explicit Equilibrium policy code");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void deadEndpointCannotBeResurrected(GameTestHelper helper) throws Exception {
        var source = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(5, 2, 1));
        target.setHealth(0.0F);
        float sourceBefore = source.getHealth();

        MinecraftServer server = helper.getLevel().getServer();
        Object result = transfer(server, source.getUUID(), target.getUUID(), 4.0D, 1.0D);
        ArcanaDecision decision = decision(result);

        helper.assertTrue(!decision.allowed(), "dead endpoints must be rejected rather than resurrected");
        helper.assertTrue("equilibrium_endpoint_not_alive".equals(decision.code()),
            "dead endpoint denial must remain explicit and deterministic");
        helper.assertTrue(transferred(result) == 0.0D, "denied transfer must report zero transferred health");
        helper.assertTrue(source.getHealth() == sourceBefore, "denied transfer must not mutate the living endpoint");
        helper.assertTrue(target.getHealth() == 0.0F, "Equilibrium Rite must not resurrect a dead target");
        helper.succeed();
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static double transferred(Object result) throws Exception {
        return (double) result.getClass().getMethod("transferred").invoke(result);
    }

    private static Object transfer(
        MinecraftServer server,
        UUID source,
        UUID target,
        double requested,
        double sourceFloor
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftEquilibriumRiteRuntime");
        Method transfer = runtime.getMethod(
            "transfer",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            double.class,
            double.class);
        return transfer.invoke(null, server, source, target, requested, sourceFloor);
    }
}
