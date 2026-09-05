package dev.gustavopere.blackarcana.content.space;

import java.util.Objects;

/** Pure server-fact validation shared by blink/gate/recall/transposition adapters. */
public final class SafeDestinationPolicy {
    public Decision validate(Facts facts) {
        Objects.requireNonNull(facts, "facts");
        if (!facts.sameAllowedDimension()) return Decision.deny("dimension_denied");
        if (!facts.loaded()) return Decision.deny("destination_unloaded");
        if (!facts.insideWorldBorder()) return Decision.deny("world_border");
        if (!facts.collisionFree()) return Decision.deny("collision_blocked");
        if (!facts.headroomSafe()) return Decision.deny("suffocation_risk");
        if (!facts.fluidAllowed()) return Decision.deny("fluid_denied");
        if (!facts.protectionAllowed()) return Decision.deny("protection_denied");
        if (facts.vehicleUnsafe()) return Decision.deny("vehicle_unsafe");
        return Decision.allow();
    }

    public record Facts(
        boolean loaded,
        boolean insideWorldBorder,
        boolean collisionFree,
        boolean headroomSafe,
        boolean fluidAllowed,
        boolean sameAllowedDimension,
        boolean protectionAllowed,
        boolean vehicleUnsafe
    ) { }

    public record Decision(boolean allowed, String code) {
        public Decision { Objects.requireNonNull(code, "code"); }
        static Decision allow() { return new Decision(true, ""); }
        static Decision deny(String code) { return new Decision(false, code); }
    }
}
