package dev.gustavopere.blackarcana.content.cinder;

import java.util.Objects;

public record BlackPyreCell(String dimensionId, int x, int y, int z) {
    public BlackPyreCell {
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (dimensionId.isBlank() || dimensionId.length() > 128) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
    }
}
