package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;

import java.util.Comparator;
import java.util.List;
import java.util.Objects;

public final class BoundedTargeting {
    private BoundedTargeting() { }

    public static List<TargetCandidate> select(ArcanaTargetSpec spec, List<TargetCandidate> candidates) {
        Objects.requireNonNull(spec, "spec");
        Objects.requireNonNull(candidates, "candidates");

        double maxDistanceSquared = spec.maxRange() * spec.maxRange();
        return candidates.stream()
                .peek(candidate -> Objects.requireNonNull(candidate, "candidate"))
                .filter(TargetCandidate::loaded)
                .filter(TargetCandidate::alive)
                .filter(candidate -> candidate.distanceSquared() <= maxDistanceSquared)
                .filter(candidate -> !spec.requireLineOfSight() || candidate.lineOfSight())
                .filter(candidate -> spec.allowPlayers() || !candidate.player())
                .filter(candidate -> spec.allowFriendly() || !candidate.friendly())
                .sorted(Comparator.comparingDouble(TargetCandidate::distanceSquared)
                        .thenComparing(TargetCandidate::targetId))
                .limit(spec.maxTargets())
                .toList();
    }
}
