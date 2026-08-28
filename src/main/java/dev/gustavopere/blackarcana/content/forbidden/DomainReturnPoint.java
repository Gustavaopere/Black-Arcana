package dev.gustavopere.blackarcana.content.forbidden;

import java.util.Objects;

public record DomainReturnPoint(String dimensionId, double x, double y, double z) {
    public DomainReturnPoint {
        Objects.requireNonNull(dimensionId, "dimensionId");
        if (dimensionId.isBlank() || dimensionId.length() > 128) throw new IllegalArgumentException("invalid dimensionId");
        if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) throw new IllegalArgumentException("coordinates must be finite");
    }
}
