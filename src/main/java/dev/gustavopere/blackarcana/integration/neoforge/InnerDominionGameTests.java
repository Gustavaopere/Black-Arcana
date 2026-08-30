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
import java.util.List;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class InnerDominionGameTests {
    private InnerDominionGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void localizedSessionReturnsParticipantsToCapturedOrigins(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var guest = helper.makeMockServerPlayerInLevel();
        place(helper, owner, new BlockPos(1, 2, 1));
        place(helper, guest, new BlockPos(3, 2, 1));
        double guestOriginX = guest.getX();
        double guestOriginY = guest.getY();
        double guestOriginZ = guest.getZ();
        UUID sessionId = UUID.randomUUID();

        Object opened = open(
            helper.getLevel().getServer(),
            sessionId,
            owner.getUUID(),
            List.of(owner.getUUID(), guest.getUUID()),
            8.0D,
            200L);
        helper.assertTrue(decision(opened).allowed() && opened(opened),
            "eligible localized Inner Dominion session must open");
        helper.assertTrue(participantCount(opened) == 2,
            "session must capture the bounded participant set exactly once");

        place(helper, guest, new BlockPos(6, 2, 1));
        Object closed = close(helper.getLevel().getServer(), sessionId);
        helper.assertTrue(decision(closed).allowed() && closed(closed),
            "normal Inner Dominion termination must close after safe return settlement");
        helper.assertTrue(returnedParticipants(closed) == 2,
            "every loaded participant must receive a validated return");
        helper.assertTrue(distanceSquared(guest.getX(), guest.getY(), guest.getZ(), guestOriginX, guestOriginY, guestOriginZ) < 0.01D,
            "guest must return to the server-captured origin");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void nestedParticipantFailsClosed(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var guest = helper.makeMockServerPlayerInLevel();
        place(helper, owner, new BlockPos(1, 2, 1));
        place(helper, guest, new BlockPos(3, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        UUID firstSession = UUID.randomUUID();

        Object first = open(
            server,
            firstSession,
            owner.getUUID(),
            List.of(owner.getUUID(), guest.getUUID()),
            8.0D,
            200L);
        helper.assertTrue(decision(first).allowed(), "first Inner Dominion session must open");

        Object nested = open(
            server,
            UUID.randomUUID(),
            guest.getUUID(),
            List.of(guest.getUUID()),
            8.0D,
            200L);
        helper.assertTrue(!decision(nested).allowed(),
            "participant already bound to a domain must be denied from a nested domain");
        helper.assertTrue("inner_dominion_nested_participant".equals(decision(nested).code()),
            "nested denial must expose the canonical diagnostic");

        Object closed = close(server, firstSession);
        helper.assertTrue(decision(closed).allowed(), "first session must remain cleanly closeable after nested denial");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void participantOutsideRequestedRadiusFailsClosed(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var guest = helper.makeMockServerPlayerInLevel();
        place(helper, owner, new BlockPos(1, 2, 1));
        place(helper, guest, new BlockPos(10, 2, 1));

        Object result = open(
            helper.getLevel().getServer(),
            UUID.randomUUID(),
            owner.getUUID(),
            List.of(owner.getUUID(), guest.getUUID()),
            4.0D,
            200L);
        helper.assertTrue(!decision(result).allowed() && !opened(result),
            "participant outside the localized rulespace radius must fail closed");
        helper.assertTrue("inner_dominion_radius".equals(decision(result).code()),
            "radius rejection must expose the canonical diagnostic");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void invalidOriginUsesValidatedAlternateFallback(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var guest = helper.makeMockServerPlayerInLevel();
        BlockPos ownerRelative = new BlockPos(1, 2, 1);
        BlockPos guestRelative = new BlockPos(3, 2, 1);
        place(helper, owner, ownerRelative);
        place(helper, guest, guestRelative);
        double guestOriginX = guest.getX();
        double guestOriginY = guest.getY();
        double guestOriginZ = guest.getZ();
        UUID sessionId = UUID.randomUUID();

        Object opened = open(
            helper.getLevel().getServer(),
            sessionId,
            owner.getUUID(),
            List.of(owner.getUUID(), guest.getUUID()),
            8.0D,
            200L);
        helper.assertTrue(decision(opened).allowed(), "Inner Dominion fixture session must open");

        place(helper, guest, new BlockPos(6, 2, 1));
        BlockPos blockedOrigin = helper.absolutePos(guestRelative);
        helper.getLevel().setBlockAndUpdate(blockedOrigin, Blocks.STONE.defaultBlockState());
        helper.getLevel().setBlockAndUpdate(blockedOrigin.above(), Blocks.STONE.defaultBlockState());

        Object closed = close(helper.getLevel().getServer(), sessionId);
        helper.assertTrue(decision(closed).allowed() && closed(closed),
            "invalid origin must not strand an otherwise recoverable participant");
        int fallbackCount = fallbackReturns(closed);
        helper.assertTrue(fallbackCount == 1,
            "exactly the participant with a blocked origin must use fallback; actual=" + fallbackCount);
        helper.assertTrue(distanceSquared(guest.getX(), guest.getY(), guest.getZ(), guestOriginX, guestOriginY, guestOriginZ) > 0.25D,
            "blocked guest origin must not be reused as fallback");
        helper.assertTrue(helper.getLevel().noCollision(guest, guest.getBoundingBox()),
            "selected alternate fallback must remain collision-free after settlement");
        helper.succeed();
    }

    private static Object open(
            MinecraftServer server,
            UUID sessionId,
            UUID ownerId,
            List<UUID> participantIds,
            double radius,
            long durationTicks
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftInnerDominionRuntime");
        Method method = runtime.getMethod(
            "openLocalizedSession",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            List.class,
            double.class,
            long.class);
        return method.invoke(null, server, sessionId, ownerId, participantIds, radius, durationTicks);
    }

    private static Object close(MinecraftServer server, UUID sessionId) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftInnerDominionRuntime");
        Method method = runtime.getMethod("closeSession", MinecraftServer.class, UUID.class);
        return method.invoke(null, server, sessionId);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean opened(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("opened").invoke(result);
    }

    private static int participantCount(Object result) throws Exception {
        return (int) result.getClass().getMethod("participantCount").invoke(result);
    }

    private static boolean closed(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("closed").invoke(result);
    }

    private static int returnedParticipants(Object result) throws Exception {
        return (int) result.getClass().getMethod("returnedParticipants").invoke(result);
    }

    private static int fallbackReturns(Object result) throws Exception {
        return (int) result.getClass().getMethod("fallbackReturns").invoke(result);
    }

    private static void place(GameTestHelper helper, net.minecraft.world.entity.Entity entity, BlockPos relative) {
        BlockPos absolute = helper.absolutePos(relative);
        entity.setPos(absolute.getX() + 0.5D, absolute.getY(), absolute.getZ() + 0.5D);
    }

    private static double distanceSquared(double ax, double ay, double az, double bx, double by, double bz) {
        double dx = ax - bx;
        double dy = ay - by;
        double dz = az - bz;
        return dx * dx + dy * dy + dz * dz;
    }
}
