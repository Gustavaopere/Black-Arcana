package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCost(String resourceId, double amount) {
    public ArcanaCost {
        Objects.requireNonNull(resourceId, "resourceId");
        if (resourceId.isBlank()) {
            throw new IllegalArgumentException("resourceId cannot be blank");
        }
        if (!Double.isFinite(amount) || amount < 0.0) {
            throw new IllegalArgumentException("amount must be finite and non-negative");
        }
    }

    public static ArcanaCost none() {
        return new ArcanaCost("black_arcana:none", 0.0);
    }
}
