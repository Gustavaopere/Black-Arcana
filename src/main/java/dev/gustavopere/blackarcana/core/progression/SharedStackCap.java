package dev.gustavopere.blackarcana.core.progression;

import java.util.Collection;
import java.util.Objects;

/** Shared cap for multiple bonuses affecting the same output dimension. */
public record SharedStackCap(double hardCap) {
    public SharedStackCap {
        if (!Double.isFinite(hardCap) || hardCap < 0D) throw new IllegalArgumentException("hardCap must be finite and non-negative");
    }

    public double combine(Collection<Double> sources) {
        Objects.requireNonNull(sources, "sources");
        double total = 0D;
        for (Double source : sources) {
            if (source == null || !Double.isFinite(source) || source < 0D) throw new IllegalArgumentException("stack sources must be finite and non-negative");
            if (total >= hardCap || source >= hardCap - total) return hardCap;
            total += source;
        }
        return Math.min(hardCap, total);
    }
}
