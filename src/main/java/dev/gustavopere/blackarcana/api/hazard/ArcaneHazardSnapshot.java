package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Immutable root facts captured when a hazard session is activated. */
public record ArcaneHazardSnapshot(
    ArcanaCastId rootCastId,
    ArcanaSpellId spellId,
    UUID casterId,
    String dimensionId,
    long activatedAtTick,
    ArcaneDangerProfile profile
) {
    public static final int MAX_DIMENSION_ID_LENGTH = 192;

    public ArcaneHazardSnapshot {
        Objects.requireNonNull(rootCastId, "rootCastId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(profile, "profile");
        if (dimensionId.isBlank() || dimensionId.length() > MAX_DIMENSION_ID_LENGTH) {
            throw new IllegalArgumentException("dimensionId must be non-blank and bounded");
        }
        if (activatedAtTick < 0L) {
            throw new IllegalArgumentException("activatedAtTick cannot be negative");
        }
    }
}
