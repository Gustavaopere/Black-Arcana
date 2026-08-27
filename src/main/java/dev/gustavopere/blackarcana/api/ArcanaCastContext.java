package dev.gustavopere.blackarcana.api;

import java.util.Objects;
import java.util.UUID;

public record ArcanaCastContext(UUID casterId, long serverTick, String dimensionId) {
    public ArcanaCastContext {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (serverTick < 0L) {
            throw new IllegalArgumentException("serverTick cannot be negative");
        }
        if (dimensionId.isBlank()) {
            throw new IllegalArgumentException("dimensionId cannot be blank");
        }
    }
}
