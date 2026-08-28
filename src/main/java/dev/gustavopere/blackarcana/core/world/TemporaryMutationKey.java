package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;

/** Opaque dimension + packed block-position identity, independent of Minecraft world objects. */
public record TemporaryMutationKey(String dimensionId, long packedBlockPos) {
    public TemporaryMutationKey {
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (dimensionId.isBlank() || dimensionId.length() > 128) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
    }
}
