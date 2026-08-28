package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCost(String resourceId, double amount, Unit unit) {
    public ArcanaCost {
        Objects.requireNonNull(resourceId, "resourceId");
        Objects.requireNonNull(unit, "unit");
        if (resourceId.isBlank()) throw new IllegalArgumentException("resourceId cannot be blank");
        if (!Double.isFinite(amount) || amount < 0.0) throw new IllegalArgumentException("amount must be finite and non-negative");
        if (unit == Unit.PERCENT_OF_MAX && amount > 1.0) {
            throw new IllegalArgumentException("percent-of-max amount cannot exceed 1.0");
        }
    }

    public ArcanaCost(String resourceId, double amount) {
        this(resourceId, amount, Unit.FLAT);
    }

    public static ArcanaCost percentOfMax(String resourceId, double fraction) {
        return new ArcanaCost(resourceId, fraction, Unit.PERCENT_OF_MAX);
    }

    public static ArcanaCost none() {
        return new ArcanaCost("black_arcana:none", 0.0, Unit.FLAT);
    }

    public enum Unit {
        FLAT,
        PERCENT_OF_MAX
    }
}
