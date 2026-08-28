package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/** Pure translation of one NeoForge post-damage event after actual health loss is known. */
public record ArcaneConfirmedDamage(
    ArcanaDamageProvenance provenance,
    double healthDamage,
    long serverTick
) {
    public ArcaneConfirmedDamage {
        Objects.requireNonNull(provenance, "provenance");
        if (!Double.isFinite(healthDamage) || healthDamage < 0.0D) {
            throw new IllegalArgumentException("healthDamage must be finite and non-negative");
        }
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
    }
}
