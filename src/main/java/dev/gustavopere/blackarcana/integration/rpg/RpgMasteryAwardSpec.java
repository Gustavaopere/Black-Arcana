package dev.gustavopere.blackarcana.integration.rpg;

import java.util.Objects;

/** Bounded mastery emission produced by one meaningful Black Arcana cast. */
public record RpgMasteryAwardSpec(String laneId, int experience, String sourceId) {
    public static final int MAX_EXPERIENCE_PER_CAST = 1000;

    public RpgMasteryAwardSpec {
        RpgProgressionSnapshot.validateKey(laneId, "mastery");
        Objects.requireNonNull(sourceId, "sourceId");
        if (sourceId.isBlank() || sourceId.length() > 96) {
            throw new IllegalArgumentException("sourceId must be 1..96 characters");
        }
        if (experience <= 0 || experience > MAX_EXPERIENCE_PER_CAST) {
            throw new IllegalArgumentException("mastery experience outside per-cast bounds");
        }
    }
}
