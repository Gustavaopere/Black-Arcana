package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.List;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class InnerDominionExpiryGameTests {
    private InnerDominionExpiryGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void expiredSessionAutomaticallyReturnsLoadedParticipant(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        place(helper, owner, new BlockPos(3, 2, 1));
        double originX = owner.getX();
        double originY = owner.getY();
        double originZ = owner.getZ();
        MinecraftServer server = helper.getLevel().getServer();
        UUID sessionId = UUID.randomUUID();

        Object opened = open(server, sessionId, owner.getUUID(), List.of(owner.getUUID()), 8.0D, 1L);
        helper.assertTrue(decision(opened).allowed(), "expiry fixture Inner Dominion session must open");
        place(helper, owner, new BlockPos(6, 2, 1));

        helper.runAtTickTime(5L, () -> {
            boolean returnedBeforeProbe = distanceSquared(
                owner.getX(), owner.getY(), owner.getZ(), originX, originY, originZ) < 0.01D;
            Object probe;
            try {
                probe = close(server, sessionId);
            } catch (Exception exception) {
                throw new RuntimeException(exception);
            }

            helper.assertTrue(returnedBeforeProbe,
                "expired Inner Dominion session must automatically return a loaded participant");
            try {
                helper.assertTrue(!decision(probe).allowed()
                        && "inner_dominion_session_missing".equals(decision(probe).code()),
                    "expiry recovery must settle and close its specific session before the probe");
            } catch (Exception exception) {
                throw new RuntimeException(exception);
            }
            helper.succeed();
        });
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
