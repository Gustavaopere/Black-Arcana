package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.List;
import java.util.Map;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreFrontierDiagnosticGameTests {
    private BlackPyreFrontierDiagnosticGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void reportFrontierCountDeltaAroundSynchronousIgnition(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server)
            .orElseThrow(() -> new IllegalStateException("Black Arcana runtime unavailable"));
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        BlockPos seed = caster.blockPosition().offset(1, -1, 0);
        helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        helper.getLevel().setBlock(seed.east(), Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            int before = MinecraftBlackPyreRuntime.activeFrontiers(server);
            var result = MinecraftBlackPyreRuntime.igniteDefault(
                server, caster.getUUID(), List.of(target.getUUID()), 2.0D, true,
                seed.getX(), seed.getY(), seed.getZ());
            int after = MinecraftBlackPyreRuntime.activeFrontiers(server);
            helper.assertTrue(false,
                "diagnostic frontier counts before=" + before + " after=" + after
                    + " terrainApplied=" + result.terrainApplied()
                    + " terrainCode=" + result.terrainCode());
        } finally {
            runtime.configureWorldEffects(previous);
        }
    }
}
