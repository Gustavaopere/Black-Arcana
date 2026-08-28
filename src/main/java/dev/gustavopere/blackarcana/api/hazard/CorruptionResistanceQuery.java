package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Immutable server query for the long-term corruption resistance channel. */
public record CorruptionResistanceQuery(
    ArcanaCastId rootCastId,
    ArcanaSpellId spellId,
    UUID subjectId,
    String dimensionId,
    long serverTick,
    ArcaneDangerProfile dangerProfile
) {
    public CorruptionResistanceQuery {
        Objects.requireNonNull(rootCastId, "rootCastId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(subjectId, "subjectId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(dangerProfile, "dangerProfile");
        if (dimensionId.isBlank() || dimensionId.length() > ArcaneHazardSnapshot.MAX_DIMENSION_ID_LENGTH) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
    }
}
