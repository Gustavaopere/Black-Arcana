package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;

import java.util.Objects;

/** Spell-specific protection policy applied after the generic CONTROL admission gate. */
public final class NullifyingGazeTargetPolicy {
    private NullifyingGazeTargetPolicy() { }

    public static ArcanaDecision evaluate(EntityProtectionFacts facts) {
        Objects.requireNonNull(facts, "facts");
        if (facts.boss()) {
            return ArcanaDecision.deny(
                "nullifying_gaze_boss_resistant",
                "Boss targets require an explicit provider-specific nullification contract");
        }
        return ArcanaDecision.allow();
    }
}
