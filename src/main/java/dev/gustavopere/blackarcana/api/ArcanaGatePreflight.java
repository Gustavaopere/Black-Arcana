package dev.gustavopere.blackarcana.api;

import java.util.Objects;

/**
 * Result of the deliberately partial, read-only selected-spell gate projection.
 *
 * <p>Only gates whose established service contract is query-only participate here.
 * CLEAR therefore means "no predictable read-only gate currently blocks" rather
 * than "the cast is guaranteed to succeed". Replay admission, target resolution,
 * world policy and hazard preparation remain authoritative cast-time stages.</p>
 */
public record ArcanaGatePreflight(Gate gate, ArcanaDecision decision) {
    public enum Gate {
        CLEAR,
        IDENTITY,
        PROGRESSION,
        COOLDOWN,
        COST
    }

    public ArcanaGatePreflight {
        Objects.requireNonNull(gate, "gate");
        Objects.requireNonNull(decision, "decision");
        if ((gate == Gate.CLEAR) != decision.allowed()) {
            throw new IllegalArgumentException("clear gate and decision must agree");
        }
    }

    public boolean allowed() {
        return gate == Gate.CLEAR;
    }

    public static ArcanaGatePreflight clear() {
        return new ArcanaGatePreflight(Gate.CLEAR, ArcanaDecision.allow());
    }

    public static ArcanaGatePreflight blocked(Gate gate, ArcanaDecision decision) {
        Objects.requireNonNull(gate, "gate");
        Objects.requireNonNull(decision, "decision");
        if (gate == Gate.CLEAR) throw new IllegalArgumentException("blocked gate cannot be CLEAR");
        if (decision.allowed()) throw new IllegalArgumentException("blocked gate requires a denial decision");
        return new ArcanaGatePreflight(gate, decision);
    }
}
