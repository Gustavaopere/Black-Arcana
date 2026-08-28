package dev.gustavopere.blackarcana.core.world;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoadedChunkGuardTest {
    @Test
    void admitsOnlyAlreadyLoadedChunks() {
        var loaded = new ChunkRef("minecraft:overworld", 0, 0);
        var unloaded = new ChunkRef("minecraft:overworld", 1, 0);
        var guard = new LoadedChunkGuard(4, chunk -> chunk.equals(loaded));

        assertTrue(guard.authorize(List.of(loaded)).allowed());
        assertEquals("world_chunk_unloaded", guard.authorize(List.of(loaded, unloaded)).code());
    }

    @Test
    void uniqueChunkCardinalityIsBounded() {
        var one = new ChunkRef("minecraft:overworld", 0, 0);
        var two = new ChunkRef("minecraft:overworld", 1, 0);
        var guard = new LoadedChunkGuard(1, chunk -> true);

        assertTrue(guard.authorize(List.of(one, one)).allowed());
        assertFalse(guard.authorize(List.of(one, two)).allowed());
    }
}
