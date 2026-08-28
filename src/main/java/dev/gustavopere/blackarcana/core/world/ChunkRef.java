package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;

public record ChunkRef(String dimensionId, int chunkX, int chunkZ) {
    public ChunkRef {
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (dimensionId.isBlank() || dimensionId.length() > 128) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
    }
}
