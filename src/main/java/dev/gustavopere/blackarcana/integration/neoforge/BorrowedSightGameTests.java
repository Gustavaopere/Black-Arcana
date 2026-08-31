package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BorrowedSightGameTests {
    private BorrowedSightGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void ownedLoadedFamiliarStartsWithoutMovingViewer(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        Entity familiar = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(5, 2, 1));
        place(helper, viewer, new BlockPos(1, 2, 1));
        double x = viewer.getX();
        double y = viewer.getY();
        double z = viewer.getZ();
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, viewer.getUUID(), familiar.getUUID());

        Object result = start(server, viewer.getUUID(), familiar.getUUID(), 16.0D, 200L);

        helper.assertTrue(decision(result).allowed() && active(result),
            "owned loaded same-dimension familiar must start Borrowed Sight");
        helper.assertTrue(familiar.getUUID().equals(targetId(result)),
            "successful Borrowed Sight must expose the authoritative target id");
        helper.assertTrue(distanceSquared(viewer.getX(), viewer.getY(), viewer.getZ(), x, y, z) < 0.000001D,
            "Borrowed Sight must never teleport the viewer's server-side body");
        helper.assertTrue(isActive(server, viewer.getUUID()),
            "successful Borrowed Sight must create one active viewer session");
        stop(server, viewer.getUUID());
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void foreignFamiliarFailsClosed(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        var otherOwner = helper.makeMockServerPlayerInLevel();
        Entity familiar = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(5, 2, 1));
        place(helper, viewer, new BlockPos(1, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, otherOwner.getUUID(), familiar.getUUID());

        Object result = start(server, viewer.getUUID(), familiar.getUUID(), 16.0D, 200L);

        helper.assertTrue(!decision(result).allowed() && !active(result),
            "foreign familiar must fail closed");
        helper.assertTrue("borrowed_sight_ownership".equals(decision(result).code()),
            "foreign familiar denial must expose the canonical ownership diagnostic");
        helper.assertTrue(!isActive(server, viewer.getUUID()),
            "denied Borrowed Sight must not create a session");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void playerTargetFailsClosedEvenIfBound(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        var target = helper.makeMockServerPlayerInLevel();
        place(helper, viewer, new BlockPos(1, 2, 1));
        place(helper, target, new BlockPos(4, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, viewer.getUUID(), target.getUUID());

        Object result = start(server, viewer.getUUID(), target.getUUID(), 16.0D, 200L);

        helper.assertTrue(!decision(result).allowed() && !active(result),
            "player target must fail closed until explicit consenting-bond policy exists");
        helper.assertTrue("borrowed_sight_player_policy".equals(decision(result).code()),
            "player denial must expose the canonical Borrowed Sight privacy diagnostic");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void rangeAndDurationSafetyCeilingsFailClosed(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        Entity familiar = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(3, 2, 1));
        place(helper, viewer, new BlockPos(1, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, viewer.getUUID(), familiar.getUUID());

        Object range = start(server, viewer.getUUID(), familiar.getUUID(), 97.0D, 200L);
        helper.assertTrue(!decision(range).allowed(), "range above 96 blocks must fail closed");
        helper.assertTrue("borrowed_sight_range_config".equals(decision(range).code()),
            "range ceiling denial must expose the canonical diagnostic");

        Object duration = start(server, viewer.getUUID(), familiar.getUUID(), 16.0D, 401L);
        helper.assertTrue(!decision(duration).allowed(), "duration above 400 ticks must fail closed");
        helper.assertTrue("borrowed_sight_duration_config".equals(decision(duration).code()),
            "duration ceiling denial must expose the canonical diagnostic");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void familiarUnloadClosesSession(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        Entity familiar = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(4, 2, 1));
        place(helper, viewer, new BlockPos(1, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, viewer.getUUID(), familiar.getUUID());
        Object opened = start(server, viewer.getUUID(), familiar.getUUID(), 16.0D, 200L);
        helper.assertTrue(decision(opened).allowed(), "precondition: owned familiar session must open");

        familiar.discard();
        maintain(server);

        helper.assertTrue(!isActive(server, viewer.getUUID()),
            "unloaded/removed familiar must deterministically return the viewer by closing the session");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void viewerLogoutClosesSession(GameTestHelper helper) throws Exception {
        var viewer = helper.makeMockServerPlayerInLevel();
        Entity familiar = helper.spawnWithNoFreeWill(EntityType.SHEEP, new BlockPos(4, 2, 1));
        place(helper, viewer, new BlockPos(1, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        bind(server, viewer.getUUID(), familiar.getUUID());
        Object opened = start(server, viewer.getUUID(), familiar.getUUID(), 16.0D, 200L);
        helper.assertTrue(decision(opened).allowed(), "precondition: owned familiar session must open");

        NeoForge.EVENT_BUS.post(new PlayerEvent.PlayerLoggedOutEvent(viewer));

        helper.assertTrue(!isActive(server, viewer.getUUID()),
            "viewer logout must close Borrowed Sight before player removal");
        helper.succeed();
    }

    private static void bind(MinecraftServer server, UUID ownerId, UUID familiarId) throws Exception {
        runtime().getMethod("bindFamiliar", MinecraftServer.class, UUID.class, UUID.class)
            .invoke(null, server, ownerId, familiarId);
    }

    private static Object start(MinecraftServer server, UUID viewerId, UUID targetId, double range, long duration) throws Exception {
        return runtime().getMethod("start", MinecraftServer.class, UUID.class, UUID.class, double.class, long.class)
            .invoke(null, server, viewerId, targetId, range, duration);
    }

    private static void stop(MinecraftServer server, UUID viewerId) throws Exception {
        runtime().getMethod("stop", MinecraftServer.class, UUID.class).invoke(null, server, viewerId);
    }

    private static void maintain(MinecraftServer server) throws Exception {
        runtime().getMethod("maintain", MinecraftServer.class).invoke(null, server);
    }

    private static boolean isActive(MinecraftServer server, UUID viewerId) throws Exception {
        return (boolean) runtime().getMethod("isActive", MinecraftServer.class, UUID.class).invoke(null, server, viewerId);
    }

    private static Class<?> runtime() throws ClassNotFoundException {
        return Class.forName("dev.gustavopere.blackarcana.integration.neoforge.MinecraftBorrowedSightRuntime");
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean active(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("active").invoke(result);
    }

    private static UUID targetId(Object result) throws Exception {
        return (UUID) result.getClass().getMethod("targetId").invoke(result);
    }

    private static void place(GameTestHelper helper, Entity entity, BlockPos relative) {
        BlockPos absolute = helper.absolutePos(relative);
        entity.setPos(absolute.getX() + 0.5D, absolute.getY(), absolute.getZ() + 0.5D);
    }

    private static double distanceSquared(double x1, double y1, double z1, double x2, double y2, double z2) {
        double dx = x1 - x2;
        double dy = y1 - y2;
        double dz = z1 - z2;
        return dx * dx + dy * dy + dz * dz;
    }
}
