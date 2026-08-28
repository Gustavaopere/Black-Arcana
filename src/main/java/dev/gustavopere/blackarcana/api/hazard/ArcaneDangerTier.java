package dev.gustavopere.blackarcana.api.hazard;

/** Coarse semantic tier; exact numbers remain explicit in the profile. */
public enum ArcaneDangerTier {
    NORMAL,
    UNSTABLE,
    DANGEROUS,
    FORBIDDEN,
    CATASTROPHIC;

    public boolean requiresHazardSession() {
        return this != NORMAL;
    }

    public boolean requiresBacklashRisk() {
        return ordinal() >= DANGEROUS.ordinal();
    }
}
