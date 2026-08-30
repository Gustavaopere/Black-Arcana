package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.projectile.Snowball;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class AnchorRecallGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftAnchorRecallRuntime";

    private AnchorRecallGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void ownedMarkedProjectileRecallsCasterToCurrentSafeLoadedPosition(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        long now = server.getTickCount();

        Snowball projectile = new Snowball(level, caster);
        double targetX = caster.getX() + 4.0D;
        double targetY = caster.getY();
        double targetZ = caster.getZ();
        BlockPos landing = BlockPos.containing(targetX, targetY, targetZ);
        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());
        projectile.setPos(targetX, targetY, targetZ);
        helper.assertTrue(level.addFreshEntity(projectile), "Anchor Recall fixture projectile must join the loaded level");

        ArcanaDecision marked = mark(server, caster.getUUID(), projectile.getUUID(), now, 40L, 16.0D);
        helper.assertTrue(marked.allowed(), "owned loaded projectile must be accepted as an Anchor Recall mark");
        double distanceBefore = caster.distanceToSqr(projectile);

        Object recalled = recall(server, caster.getUUID(), now + 1L);
        helper.assertTrue(decision(recalled).allowed(), "valid marked projectile recall must be admitted");
        helper.assertTrue(teleported(recalled), "valid Anchor Recall must teleport the caster");
        helper.assertTrue(caster.distanceToSqr(projectile) < distanceBefore,
            "successful recall must move caster to the current marked-projectile position");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void foreignExpiredUnavailableAndBlockedAnchorsFailClosed(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var stranger = helper.makeMockServerPlayerInLevel();
        ServerLevel level = helper.getLevel();
        MinecraftServer server = level.getServer();
        long now = server.getTickCount();

        Snowball projectile = new Snowball(level, caster);
        double targetX = caster.getX() + 3.0D;
        double targetY = caster.getY();
        double targetZ = caster.getZ();
        BlockPos landing = BlockPos.containing(targetX, targetY, targetZ);
        level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(landing.above(), Blocks.AIR.defaultBlockState());
        projectile.setPos(targetX, targetY, targetZ);
        helper.assertTrue(level.addFreshEntity(projectile), "Anchor Recall fixture projectile must join the loaded level");

        ArcanaDecision foreign = mark(server, stranger.getUUID(), projectile.getUUID(), now, 20L, 16.0D);
        helper.assertTrue(!foreign.allowed() && "anchor_recall_foreign_projectile".equals(foreign.code()),
            "a projectile owned by another entity must never be markable");

        ArcanaDecision marked = mark(server, caster.getUUID(), projectile.getUUID(), now, 2L, 16.0D);
        helper.assertTrue(marked.allowed(), "owned projectile must be markable for expiry test");
        Object expired = recall(server, caster.getUUID(), now + 3L);
        helper.assertTrue(!decision(expired).allowed() && "projectile_expired".equals(decision(expired).code()),
            "expired marked projectile must fail closed through AnchorRecallValidator");

        marked = mark(server, caster.getUUID(), projectile.getUUID(), now, 20L, 16.0D);
        helper.assertTrue(marked.allowed(), "owned projectile must be re-markable");
        projectile.discard();
        Object unavailable = recall(server, caster.getUUID(), now + 1L);
        helper.assertTrue(!decision(unavailable).allowed()
                && "anchor_recall_projectile_unavailable".equals(decision(unavailable).code()),
            "unloaded/discarded marked projectile must fail closed without chunk loading");

        Snowball blockedProjectile = new Snowball(level, caster);
        blockedProjectile.setPos(targetX, targetY, targetZ);
        helper.assertTrue(level.addFreshEntity(blockedProjectile), "blocked fixture projectile must join the level");
        helper.assertTrue(mark(server, caster.getUUID(), blockedProjectile.getUUID(), now, 20L, 16.0D).allowed(),
            "owned blocked-destination projectile must still be markable");
        level.setBlockAndUpdate(landing, Blocks.STONE.defaultBlockState());
        double beforeX = caster.getX();
        double beforeY = caster.getY();
        double beforeZ = caster.getZ();
        Object blocked = recall(server, caster.getUUID(), now + 1L);
        helper.assertTrue(!decision(blocked).allowed() && "collision_blocked".equals(decision(blocked).code()),
            "blocked projectile destination must fail closed through shared destination resolver");
        helper.assertTrue(Math.abs(caster.getX() - beforeX) < 0.01D
                && Math.abs(caster.getY() - beforeY) < 0.01D
                && Math.abs(caster.getZ() - beforeZ) < 0.01D,
            "denied Anchor Recall must leave caster position unchanged");
        helper.succeed();
    }

    private static ArcanaDecision mark(
        MinecraftServer server,
        UUID casterId,
        UUID projectileId,
        long nowTick,
        long maxAgeTicks,
        double maxRange
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "markProjectile",
            MinecraftServer.class,
            UUID.class,
            UUID.class,
            long.class,
            long.class,
            double.class);
        return (ArcanaDecision) method.invoke(null, server, casterId, projectileId, nowTick, maxAgeTicks, maxRange);
    }

    private static Object recall(MinecraftServer server, UUID casterId, long nowTick) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod("recall", MinecraftServer.class, UUID.class, long.class);
        return method.invoke(null, server, casterId, nowTick);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean teleported(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("teleported").invoke(result);
    }
}
