package dev.gustavopere.blackarcana.core.targeting;

import java.util.Objects;

public record TargetCandidate(
        String targetId,
        double distanceSquared,
        boolean loaded,
        boolean alive,
        boolean lineOfSight,
        boolean player,
        boolean friendly
) {
    public TargetCandidate {
        Objects.requireNonNull(targetId, "targetId");
        if (targetId.isBlank()) throw new IllegalArgumentException("targetId cannot be blank");
        if (!Double.isFinite(distanceSquared) || distanceSquared < 0.0) {
            throw new IllegalArgumentException("distanceSquared must be finite and non-negative");
        }
    }
}
