package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;

public record RitualAnchor(String dimensionId, long packedBlockPos) {
    public RitualAnchor {
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (dimensionId.isBlank() || dimensionId.length() > 192) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
    }
}
