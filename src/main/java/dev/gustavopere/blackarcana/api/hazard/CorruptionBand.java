package dev.gustavopere.blackarcana.api.hazard;

/** Ordered corruption bands; exact thresholds remain configurable/balanceable. */
public enum CorruptionBand {
    CLEAR,
    TRACE,
    TAINTED,
    CORRUPTED,
    CRITICAL
}
