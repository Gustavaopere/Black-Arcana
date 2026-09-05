package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class RiftBladeProjectileLifecycleGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftRiftBladesRuntime";

    private RiftBladeProjectileLifecycleGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void projectileVolleyExpiresAndReleasesEveryBudgetSlot(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        Object result = launchProjectileVolley(server, owner.getUUID(), nowTick, 3, 5L);

        helper.assertTrue(decision(result).allowed(), "bounded Rift Blades volley must be admitted");
        helper.assertTrue(launchedCount(result) == 3, "admitted volley must create exactly the requested ephemeral handles");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 3,
            "active projectile accounting must match the admitted volley exactly");

        tickProjectiles(server, nowTick + 5L);
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "expired Rift Blades projectiles must release every active budget slot");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void projectileSpamCannotExceedActiveProjectionBudget(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        Object saturated = launchProjectileVolley(
            server,
            owner.getUUID(),
            nowTick,
            ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            200L);
        helper.assertTrue(decision(saturated).allowed(),
            "owner must be able to fill, but not exceed, the frozen active projection ceiling");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "active projectile accounting must stop at the hard ceiling");

        Object overflow = launchProjectileVolley(server, owner.getUUID(), nowTick, 1, 200L);
        helper.assertTrue(!decision(overflow).allowed(), "49th concurrent projection must fail closed");
        helper.assertTrue(launchedCount(overflow) == 0, "denied overflow must not partially launch a projectile");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "denied overflow must leave the saturated budget unchanged");

        tickProjectiles(server, nowTick + 200L);
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "expiry after saturation must release all projectile budget");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void ownerLogoutCleansAllRiftBladeProjectileHandles(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        Object result = launchProjectileVolley(server, owner.getUUID(), nowTick, 4, 200L);
        helper.assertTrue(decision(result).allowed(), "test volley must be admitted before logout cleanup");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 4,
            "test owner must begin with four tracked projectiles");

        onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(owner));
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "owner logout must atomically remove Rift Blades handles and release their budget");
        helper.succeed();
    }

    private static Object launchProjectileVolley(
        MinecraftServer server,
        UUID ownerId,
        long nowTick,
        int count,
        long lifetimeTicks
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "launchProjectileVolley",
            MinecraftServer.class,
            UUID.class,
            long.class,
            int.class,
            long.class);
        return method.invoke(null, server, ownerId, nowTick, count, lifetimeTicks);
    }

    private static int activeProjectiles(MinecraftServer server, UUID ownerId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("activeProjectiles", MinecraftServer.class, UUID.class);
        return (int) method.invoke(null, server, ownerId);
    }

    private static void tickProjectiles(MinecraftServer server, long nowTick) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("tickProjectiles", MinecraftServer.class, long.class);
        method.invoke(null, server, nowTick);
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getDeclaredMethod("onPlayerLoggedOut", PlayerEvent.PlayerLoggedOutEvent.class);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static int launchedCount(Object result) throws Exception {
        return (int) result.getClass().getMethod("launchedCount").invoke(result);
    }
}
