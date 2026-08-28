package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.Objects;
import java.util.Set;

/**
 * Read-only chunk admission gate. The injected probe can answer only whether a
 * chunk is already loaded; this contract intentionally exposes no loading/ticket API.
 */
public final class LoadedChunkGuard {
    private final int maxChunksPerEffect;
    private final LoadedChunkProbe probe;

    public LoadedChunkGuard(int maxChunksPerEffect, LoadedChunkProbe probe) {
        if (maxChunksPerEffect <= 0 || maxChunksPerEffect > 256) {
            throw new IllegalArgumentException("maxChunksPerEffect must be between 1 and 256");
        }
        this.maxChunksPerEffect = maxChunksPerEffect;
        this.probe = Objects.requireNonNull(probe, "probe");
    }

    public ArcanaDecision authorize(Collection<ChunkRef> requestedChunks) {
        Objects.requireNonNull(requestedChunks, "requestedChunks");
        Set<ChunkRef> unique = new LinkedHashSet<>(requestedChunks);
        if (unique.isEmpty()) return ArcanaDecision.deny("world_chunks_empty", "World effect requested no chunks");
        if (unique.size() > maxChunksPerEffect) {
            return ArcanaDecision.deny("world_chunk_budget", "World effect exceeds the loaded-chunk budget");
        }
        for (ChunkRef chunk : unique) {
            if (chunk == null) return ArcanaDecision.deny("world_chunk_invalid", "World effect contains a null chunk");
            if (!probe.isLoaded(chunk)) {
                return ArcanaDecision.deny("world_chunk_unloaded", "World effect would require an unloaded chunk");
            }
        }
        return ArcanaDecision.allow();
    }

    @FunctionalInterface
    public interface LoadedChunkProbe {
        boolean isLoaded(ChunkRef chunk);
    }
}
