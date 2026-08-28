package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaTargetSpec(
        Kind kind,
        double maxRange,
        int maxTargets,
        boolean requireLineOfSight,
        boolean allowPlayers,
        boolean allowFriendly
) {
    public static final double ABSOLUTE_MAX_RANGE = 512.0;
    public static final int ABSOLUTE_MAX_TARGETS = 128;

    public ArcanaTargetSpec {
        Objects.requireNonNull(kind, "kind");
        if (!Double.isFinite(maxRange) || maxRange < 0.0 || maxRange > ABSOLUTE_MAX_RANGE) {
            throw new IllegalArgumentException("maxRange must be finite and between 0 and " + ABSOLUTE_MAX_RANGE);
        }
        if (maxTargets <= 0 || maxTargets > ABSOLUTE_MAX_TARGETS) {
            throw new IllegalArgumentException("maxTargets must be between 1 and " + ABSOLUTE_MAX_TARGETS);
        }
    }

    public enum Kind {
        SELF,
        ENTITY,
        RAY,
        BLOCK,
        CONE,
        SPHERE,
        CYLINDER,
        PROJECTILE,
        LINKED
    }
}
