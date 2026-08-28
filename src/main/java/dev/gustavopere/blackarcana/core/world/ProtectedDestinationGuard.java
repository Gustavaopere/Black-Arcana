package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.List;
import java.util.Objects;

/**
 * Fail-closed destination gate for displacement/control effects.
 * A destination must already be loaded and must be accepted by every installed
 * protection adapter. This class has no chunk-loading or teleport API.
 */
public final class ProtectedDestinationGuard {
    private final LoadedChunkGuard loadedChunks;
    private final ProtectionAdapterRegistry protectionAdapters;

    public ProtectedDestinationGuard(
        LoadedChunkGuard loadedChunks,
        ProtectionAdapterRegistry protectionAdapters
    ) {
        this.loadedChunks = Objects.requireNonNull(loadedChunks, "loadedChunks");
        this.protectionAdapters = Objects.requireNonNull(protectionAdapters, "protectionAdapters");
    }

    public ArcanaDecision authorize(ChunkRef destinationChunk, ProtectionQuery query) {
        Objects.requireNonNull(destinationChunk, "destinationChunk");
        Objects.requireNonNull(query, "query");
        if (!destinationChunk.dimensionId().equals(query.dimensionId())) {
            return ArcanaDecision.deny(
                "destination_dimension_mismatch",
                "Destination chunk and protection query refer to different dimensions");
        }

        ArcanaDecision loaded = loadedChunks.authorize(List.of(destinationChunk));
        if (!loaded.allowed()) return loaded;
        return protectionAdapters.authorize(query);
    }
}
