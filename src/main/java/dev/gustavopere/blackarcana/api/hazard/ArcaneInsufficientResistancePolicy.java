package dev.gustavopere.blackarcana.api.hazard;

/**
 * Server-owned policy applied when effective Arcane Resistance is below a profile's declared minimum.
 * The minimum remains descriptive data; this enum decides whether that threshold is a hard cast gate.
 */
public enum ArcaneInsufficientResistancePolicy {
    DENY_CAST(true),
    ALLOW_WITH_RISK(false);

    private final boolean blocksCast;

    ArcaneInsufficientResistancePolicy(boolean blocksCast) {
        this.blocksCast = blocksCast;
    }

    public boolean blocksCast() {
        return blocksCast;
    }
}
