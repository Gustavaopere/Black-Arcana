package dev.gustavopere.blackarcana.api;

import java.util.Objects;
import java.util.UUID;

public record ArcanaCastContext(UUID casterId, long serverTick, String dimensionId, ArcanaCasterMode casterMode) {
    public ArcanaCastContext {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(casterMode, "casterMode");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        if (dimensionId.isBlank()) throw new IllegalArgumentException("dimensionId cannot be blank");
    }

    public ArcanaCastContext(UUID casterId, long serverTick, String dimensionId) {
        this(casterId, serverTick, dimensionId, ArcanaCasterMode.SURVIVAL);
    }
}
