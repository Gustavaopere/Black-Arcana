package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/** Immutable backlash inputs frozen when the root hazard session is opened. */
public record ArcaneBacklashSnapshot(
    ArcaneHazardSnapshot hazard,
    ArcaneResistanceSnapshot arcaneResistance,
    ArcaneBacklashPolicy policy
) {
    public ArcaneBacklashSnapshot {
        Objects.requireNonNull(hazard, "hazard");
        Objects.requireNonNull(arcaneResistance, "arcaneResistance");
        Objects.requireNonNull(policy, "policy");
    }
}
