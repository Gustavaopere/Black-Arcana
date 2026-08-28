package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.CorruptionBand;

/** Ordered, bounded corruption thresholds. Stage 08 may tune values without changing semantics. */
public record CorruptionThresholds(
    double trace,
    double tainted,
    double corrupted,
    double critical
) {
    public static final double ABSOLUTE_MAX_THRESHOLD = 1_000_000.0D;

    public CorruptionThresholds {
        finitePositive("trace", trace);
        finitePositive("tainted", tainted);
        finitePositive("corrupted", corrupted);
        finitePositive("critical", critical);
        if (!(trace < tainted && tainted < corrupted && corrupted < critical)) {
            throw new IllegalArgumentException("corruption thresholds must be strictly increasing");
        }
    }

    public static CorruptionThresholds canonical() {
        return new CorruptionThresholds(100.0D, 300.0D, 600.0D, 900.0D);
    }

    public CorruptionBand bandFor(double units) {
        if (!Double.isFinite(units) || units < 0.0D) {
            throw new IllegalArgumentException("corruption units must be finite and non-negative");
        }
        if (units >= critical) return CorruptionBand.CRITICAL;
        if (units >= corrupted) return CorruptionBand.CORRUPTED;
        if (units >= tainted) return CorruptionBand.TAINTED;
        if (units >= trace) return CorruptionBand.TRACE;
        return CorruptionBand.CLEAR;
    }

    private static void finitePositive(String name, double value) {
        if (!Double.isFinite(value) || value <= 0.0D || value > ABSOLUTE_MAX_THRESHOLD) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }
}
