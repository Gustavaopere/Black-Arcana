package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;

import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Fail-closed policy for mutually exclusive client camera presentations. */
final class NoeticCameraConflictPolicy {
    private NoeticCameraConflictPolicy() { }

    static Set<UUID> conflictedViewers(
            List<NoeticObservationRuntime.ActiveSession> observations,
            List<AstralSeveranceRuntime.ActiveProjection> projections
    ) {
        Objects.requireNonNull(observations, "observations");
        Objects.requireNonNull(projections, "projections");

        Set<UUID> borrowedSightViewers = new LinkedHashSet<>();
        for (NoeticObservationRuntime.ActiveSession observation : observations) {
            Objects.requireNonNull(observation, "observation");
            if (observation.kind() == NoeticObservationKind.BORROWED_SIGHT) {
                borrowedSightViewers.add(observation.viewerId());
            }
        }

        Set<UUID> conflicted = new LinkedHashSet<>();
        for (AstralSeveranceRuntime.ActiveProjection projection : projections) {
            Objects.requireNonNull(projection, "projection");
            if (borrowedSightViewers.contains(projection.casterId())) {
                conflicted.add(projection.casterId());
            }
        }
        return Collections.unmodifiableSet(conflicted);
    }
}
