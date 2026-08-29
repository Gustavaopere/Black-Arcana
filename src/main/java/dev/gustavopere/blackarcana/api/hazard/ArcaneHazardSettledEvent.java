package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/**
 * Final server-owned hazard settlement emitted after a spell cast's hazard math is complete.
 */
public record ArcaneHazardSettledEvent(
    ArcanaCastId castId,
    ArcanaSpellId spellId,
    UUID casterId,
    ArcaneHazardSnapshot snapshot
) {
    public ArcaneHazardSettledEvent {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(snapshot, "snapshot");
    }
}
