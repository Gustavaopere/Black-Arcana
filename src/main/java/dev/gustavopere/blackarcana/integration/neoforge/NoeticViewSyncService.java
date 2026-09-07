package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;

import java.util.List;
import java.util.Objects;
import java.util.OptionalInt;
import java.util.UUID;
import java.util.function.Function;

/** Stateless projection of bounded canonical Noetic sessions into client presentation transitions. */
final class NoeticViewSyncService {
    private NoeticViewSyncService() { }

    static List<NoeticViewTransitionTracker.Transition> reconcile(
            NoeticObservationRuntime runtime,
            NoeticViewTransitionTracker tracker,
            Function<UUID, OptionalInt> loadedTargetIds
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(tracker, "tracker");
        Objects.requireNonNull(loadedTargetIds, "loadedTargetIds");
        return tracker.reconcileAll(NoeticViewSyncPlanner.project(runtime.activeSessions(), loadedTargetIds));
    }
}
