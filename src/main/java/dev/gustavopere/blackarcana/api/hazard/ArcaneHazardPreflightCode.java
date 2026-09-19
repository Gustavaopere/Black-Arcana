package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/** Stable server-authored decision codes emitted by the Arcane Danger preflight lifecycle. */
public enum ArcaneHazardPreflightCode {
    MINIMUM_RESISTANCE_REQUIRED("hazard_minimum_resistance"),
    STATE_CAPACITY("hazard_state_capacity"),
    STRAIN_GATE("hazard_strain_gate"),
    STATE_BUSY("hazard_state_busy"),
    PREPARATION_CANCELLED("hazard_preparation_cancelled");

    private final String code;

    ArcaneHazardPreflightCode(String code) {
        this.code = Objects.requireNonNull(code, "code");
    }

    public String code() {
        return code;
    }
}
