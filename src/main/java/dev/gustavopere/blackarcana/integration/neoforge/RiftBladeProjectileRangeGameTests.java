package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class RiftBladeProjectileRangeGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftRiftBladesRuntime";

    private RiftBladeProjectileRangeGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void collisionTerminatesProjectileAndReleasesBudgetImmediately(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        Object volley = launchProjectileVolley(server, owner.getUUID(), nowTick, 1, 200L, 8.0D);
        helper.assertTrue(decision(volley).allowed(), "bounded range-aware projectile must launch");
        UUID projectileId = firstProjectileId(volley);
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 1,
            "test must begin with one active projectile handle");

        Object step = updateProjectile(
            server,
            projectileId,
            owner.getX(),
            owner.getY(),
            owner.getZ(),
            true);

        helper.assertTrue(!stepActive(step), "collision must terminate the projectile handle immediately");
        helper.assertTrue("collision".equals(stepCode(step)), "collision termination must expose a stable reason");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "collision termination must release the active projection budget immediately");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void projectileRemainsWithinRangeThenTerminatesPastRange(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();
        double originX = owner.getX();
        double originY = owner.getY();
        double originZ = owner.getZ();

        Object volley = launchProjectileVolley(server, owner.getUUID(), nowTick, 1, 200L, 4.0D);
        helper.assertTrue(decision(volley).allowed(), "bounded range-aware projectile must launch");
        UUID projectileId = firstProjectileId(volley);

        Object inside = updateProjectile(server, projectileId, originX + 3.0D, originY, originZ, false);
        helper.assertTrue(stepActive(inside), "projectile inside configured range must remain active");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 1,
            "within-range update must preserve exactly one budget slot");

        Object outside = updateProjectile(server, projectileId, originX + 5.0D, originY, originZ, false);
        helper.assertTrue(!stepActive(outside), "projectile past configured range must terminate");
        helper.assertTrue("range_exceeded".equals(stepCode(outside)),
            "range termination must expose a stable reason");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "range termination must release the projectile budget slot");
        helper.succeed();
    }

    private static Object launchProjectileVolley(
        MinecraftServer server,
        UUID ownerId,
        long nowTick,
        int count,
        long lifetimeTicks,
        double maxRangeBlocks
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "launchProjectileVolley",
            MinecraftServer.class,
            UUID.class,
            long.class,
            int.class,
            long.class,
            double.class);
        return method.invoke(null, server, ownerId, nowTick, count, lifetimeTicks, maxRangeBlocks);
    }

    private static Object updateProjectile(
        MinecraftServer server,
        UUID projectileId,
        double x,
        double y,
        double z,
        boolean collided
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "updateProjectile",
            MinecraftServer.class,
            UUID.class,
            double.class,
            double.class,
            double.class,
            boolean.class);
        return method.invoke(null, server, projectileId, x, y, z, collided);
    }

    private static int activeProjectiles(MinecraftServer server, UUID ownerId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("activeProjectiles", MinecraftServer.class, UUID.class);
        return (int) method.invoke(null, server, ownerId);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static UUID firstProjectileId(Object volley) throws Exception {
        @SuppressWarnings("unchecked")
        List<Object> projectiles = (List<Object>) volley.getClass().getMethod("projectiles").invoke(volley);
        Object first = projectiles.getFirst();
        return (UUID) first.getClass().getMethod("projectileId").invoke(first);
    }

    private static boolean stepActive(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("active").invoke(result);
    }

    private static String stepCode(Object result) throws Exception {
        return (String) result.getClass().getMethod("code").invoke(result);
    }
}
