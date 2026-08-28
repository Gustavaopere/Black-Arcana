package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Immutable server-authored attribution for one subordinate damage attempt. */
public record ArcanaDamageProvenance(
    ArcanaCastId rootCastId,
    ArcanaDamageInstanceId damageInstanceId,
    UUID casterId,
    ArcanaSpellId spellId,
    ArcaneDamageFamily family,
    boolean hazardEligible
) {
    public ArcanaDamageProvenance {
        Objects.requireNonNull(rootCastId, "rootCastId");
        Objects.requireNonNull(damageInstanceId, "damageInstanceId");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(family, "family");
        if (family == ArcaneDamageFamily.ARCANE_BACKLASH && hazardEligible) {
            throw new IllegalArgumentException("Arcane Backlash cannot be hazard-eligible recursively");
        }
    }
}
