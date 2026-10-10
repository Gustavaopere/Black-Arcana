package dev.gustavopere.blackarcana.integration.neoforge;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Deterministic layout verification; physical world/chunk acceptance remains a separate QA gate. */
class MinecraftVeilAnchorConsecrationRuntimeTest {
    private static final BlockPos CENTER = new BlockPos(0, 70, 0);

    private static Map<BlockPos, Block> altar() {
        Map<BlockPos, Block> blocks = new HashMap<>();
        blocks.put(CENTER, Blocks.CRYING_OBSIDIAN);
        for (Direction side : Direction.Plane.HORIZONTAL) {
            blocks.put(CENTER.relative(side), Blocks.AMETHYST_BLOCK);
        }
        blocks.put(CENTER.offset(1, 0, 1), Blocks.SOUL_SAND);
        blocks.put(CENTER.offset(1, 0, -1), Blocks.SOUL_SAND);
        blocks.put(CENTER.offset(-1, 0, 1), Blocks.SOUL_SAND);
        blocks.put(CENTER.offset(-1, 0, -1), Blocks.SOUL_SAND);
        return blocks;
    }

    @Test
    void exactlyNineSurvivalObtainableBlocksDefineAValidVeilAnchor() {
        Map<BlockPos, Block> blocks = altar();
        assertTrue(MinecraftVeilAnchorConsecrationRuntime.matchesLayout(CENTER, blocks::get));
        assertTrue(blocks.size() == 9);
    }

    @Test
    void missingOrChangedBlockAndUnavailableCellFailClosed() {
        Map<BlockPos, Block> blocks = altar();
        BlockPos cardinal = CENTER.relative(Direction.NORTH);
        blocks.remove(cardinal);
        assertFalse(MinecraftVeilAnchorConsecrationRuntime.matchesLayout(CENTER, blocks::get));
        blocks.put(cardinal, Blocks.SOUL_SAND);
        assertFalse(MinecraftVeilAnchorConsecrationRuntime.matchesLayout(CENTER, blocks::get));
        blocks.put(cardinal, Blocks.AMETHYST_BLOCK);
        blocks.put(CENTER, Blocks.OBSIDIAN);
        assertFalse(MinecraftVeilAnchorConsecrationRuntime.matchesLayout(CENTER, blocks::get));
    }

    @Test
    void patternDoesNotReadOrScanAnyPositionOutsideTheNineBlocks() {
        Map<BlockPos, Block> blocks = altar();
        java.util.HashSet<BlockPos> visited = new java.util.HashSet<>();
        assertTrue(MinecraftVeilAnchorConsecrationRuntime.matchesLayout(CENTER, pos -> {
            visited.add(pos);
            return blocks.get(pos);
        }));
        assertTrue(visited.size() == 9);
        assertTrue(blocks.keySet().containsAll(visited));
    }
}
