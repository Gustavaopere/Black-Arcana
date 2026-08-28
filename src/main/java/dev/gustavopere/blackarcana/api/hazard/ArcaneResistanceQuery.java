package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Immutable server query given to resistance providers at hazard snapshot time. */
public record ArcaneResistanceQuery(
    ArcanaCastId rootCastId,
    ArcanaSpellId spellId,
    UUID casterId,
    String dimensionId,
    long serverTick,
    ArcaneDangerProfile dangerProfile
) {
    public ArcaneResistanceQuery {
        Objects.requireNonNull(rootCastId, "rootCastId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(dangerProfile, "dangerProfile");
        if (dimensionId.isBlank() || dimensionId.length() > ArcaneHazardSnapshot.MAX_DIMENSION_ID_LENGTH) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
    }
}
