package dev.gustavopere.blackarcana.integration.irons;

/** Immutable server-side projection of Iron's mana for one player. */
public record IronsManaSnapshot(float current, float maximum) {
    public IronsManaSnapshot {
        if (!Float.isFinite(current) || current < 0.0F) {
            throw new IllegalArgumentException("current mana must be finite and non-negative");
        }
        if (!Float.isFinite(maximum) || maximum < 0.0F) {
            throw new IllegalArgumentException("maximum mana must be finite and non-negative");
        }
    }
}
