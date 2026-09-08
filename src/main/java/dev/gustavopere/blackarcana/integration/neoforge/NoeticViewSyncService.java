package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;

import java.util.List;
import java.util.Objects;
import java.util.OptionalInt;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;

/** Stateless projection of bounded canonical Noetic sessions into client presentation transitions. */
final class NoeticViewSyncService {
    private NoeticViewSyncService() { }

    static List<NoeticViewTransitionTracker.Transition> reconcile(
            NoeticObservationRuntime runtime,
            NoeticViewTransitionTracker tracker,
            BiFunction<UUID, UUID, OptionalInt> loadedTargetIds
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(tracker, "tracker");
        Objects.requireNonNull(loadedTargetIds, "loadedTargetIds");
        return tracker.reconcileAll(NoeticViewSyncPlanner.project(runtime.activeSessions(), loadedTargetIds));
    }

    static int dispatch(
            NoeticObservationRuntime runtime,
            NoeticViewTransitionTracker tracker,
            BiFunction<UUID, UUID, OptionalInt> loadedTargetIds,
            BiConsumer<UUID, NoeticViewPayload> sender
    ) {
        Objects.requireNonNull(sender, "sender");
        List<NoeticViewTransitionTracker.Transition> transitions = reconcile(runtime, tracker, loadedTargetIds);
        for (NoeticViewTransitionTracker.Transition transition : transitions) {
            sender.accept(transition.viewerId(), transition.payload());
        }
        return transitions.size();
    }
}
