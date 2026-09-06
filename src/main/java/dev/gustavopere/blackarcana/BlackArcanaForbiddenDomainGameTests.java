package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainMode;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSpec;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftForbiddenDomainRuntime;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaForbiddenDomainGameTests {
    private BlackArcanaForbiddenDomainGameTests() { }

    /**
     * Exercises the real dedicated GameTest server boundary rather than a pure contract double:
     * server-owned runtime lookup, loaded-chunk admission, world border/protection/world-effect gates,
     * safe recovery validation, bounded session creation, and exactly-once explicit cleanup.
     */
    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void localizedForbiddenDomainStartsAndClosesOnLiveServerWorld(GameTestHelper helper) {
        var level = helper.getLevel();
        var server = level.getServer();
        var player = helper.makeMockServerPlayerInLevel();

        helper.assertTrue(
                ArcanaServerRuntimeManager.get(server).isPresent(),
                "GameTest server must expose the canonical Black Arcana server runtime");

        BlockPos origin = player.blockPosition();
        int safeY = Math.max(
                level.getMinBuildHeight() + 2,
                Math.min(origin.getY(), level.getMaxBuildHeight() - 3));
        BlockPos landing = new BlockPos(
                (origin.getX() >> 4 << 4) + 8,
                safeY,
                (origin.getZ() >> 4 << 4) + 8);
        BlockPos ground = landing.below();
        BlockPos head = landing.above();

        BlockState priorGround = level.getBlockState(ground);
        BlockState priorLanding = level.getBlockState(landing);
        BlockState priorHead = level.getBlockState(head);
        boolean started = false;

        try {
            level.setBlockAndUpdate(ground, Blocks.STONE.defaultBlockState());
            level.setBlockAndUpdate(landing, Blocks.AIR.defaultBlockState());
            level.setBlockAndUpdate(head, Blocks.AIR.defaultBlockState());
            player.teleportTo(landing.getX() + 0.5D, landing.getY(), landing.getZ() + 0.5D);

            ForbiddenDomainSpec spec = new ForbiddenDomainSpec(
                    "black_arcana:gametest_localized_domain",
                    ForbiddenDomainMode.LOCALIZED_FIELD,
                    1,
                    20,
                    2,
                    1);

            var decision = MinecraftForbiddenDomainRuntime.start(server, player.getUUID(), spec);
            helper.assertTrue(decision.allowed(),
                    "live server world admission must permit a safe loaded localized field");
            started = decision.allowed();
            helper.assertTrue(MinecraftForbiddenDomainRuntime.activeCount(server) == 1,
                    "successful admission must create exactly one bounded session");

            helper.assertTrue(MinecraftForbiddenDomainRuntime.close(server, player.getUUID()),
                    "first explicit close must own cleanup");
            started = false;
            helper.assertTrue(!MinecraftForbiddenDomainRuntime.close(server, player.getUUID()),
                    "second explicit close must be an idempotent no-op");
            helper.assertTrue(MinecraftForbiddenDomainRuntime.activeCount(server) == 0,
                    "explicit close must leave no active session");
        } finally {
            if (started) MinecraftForbiddenDomainRuntime.close(server, player.getUUID());
            level.setBlockAndUpdate(ground, priorGround);
            level.setBlockAndUpdate(landing, priorLanding);
            level.setBlockAndUpdate(head, priorHead);
        }

        helper.succeed();
    }
}
