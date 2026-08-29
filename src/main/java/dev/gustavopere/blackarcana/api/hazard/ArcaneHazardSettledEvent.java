package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Immutable post-settlement notification; observers cannot mutate the originating cast. */
public record ArcaneHazardSettledEvent(
    ArcanaCastId rootCastId,
    ArcanaDamageInstanceId damageInstanceId,
    ArcanaSpellId spellId,
    UUID casterId,
    ArcaneDangerTier tier,
    double confirmedHealthDamage,
    double eligibleDamage,
    double settledBacklash,
    double corruptionDelta,
    double strainDelta
) {
    public ArcaneHazardSettledEvent {
        Objects.requireNonNull(rootCastId, "rootCastId");
        Objects.requireNonNull(damageInstanceId, "damageInstanceId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(tier, "tier");
        validate("confirmedHealthDamage", confirmedHealthDamage);
        validate("eligibleDamage", eligibleDamage);
        validate("settledBacklash", settledBacklash);
        validate("corruptionDelta", corruptionDelta);
        validate("strainDelta", strainDelta);
    }

    private static void validate(String name, double value) {
        if (!Double.isFinite(value) || value < 0.0D || value > 100_000_000.0D) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }
}
