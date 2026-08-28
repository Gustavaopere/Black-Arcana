package dev.gustavopere.blackarcana.integration.ars;

/** Immutable server-side projection of Ars Nouveau mana for one player. */
public record ArsManaSnapshot(double current, double maximum) {
    public ArsManaSnapshot {
        if (!Double.isFinite(current) || current < 0.0D) {
            throw new IllegalArgumentException("current mana must be finite and non-negative");
        }
        if (!Double.isFinite(maximum) || maximum < 0.0D) {
            throw new IllegalArgumentException("maximum mana must be finite and non-negative");
        }
    }
}
