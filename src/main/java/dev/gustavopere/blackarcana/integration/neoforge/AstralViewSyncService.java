package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import dev.gustavopere.blackarcana.network.AstralViewTransitionTracker;

import java.util.List;
import java.util.Objects;
import java.util.OptionalInt;
import java.util.Set;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;

/** Stateless projection of bounded canonical Astral sessions into client presentation transitions. */
final class AstralViewSyncService {
    private AstralViewSyncService() { }

    static List<AstralViewTransitionTracker.Transition> reconcile(
            AstralSeveranceRuntime runtime,
            AstralViewTransitionTracker tracker,
            Set<UUID> suppressedViewers,
            BiFunction<UUID, UUID, OptionalInt> loadedEntityIds
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(tracker, "tracker");
        Objects.requireNonNull(suppressedViewers, "suppressedViewers");
        Objects.requireNonNull(loadedEntityIds, "loadedEntityIds");
        return tracker.reconcileAll(AstralViewSyncPlanner.project(
                runtime.activeProjections(), suppressedViewers, loadedEntityIds));
    }

    static int dispatch(
            AstralSeveranceRuntime runtime,
            AstralViewTransitionTracker tracker,
            Set<UUID> suppressedViewers,
            BiFunction<UUID, UUID, OptionalInt> loadedEntityIds,
            BiConsumer<UUID, AstralViewPayload> sender
    ) {
        Objects.requireNonNull(sender, "sender");
        List<AstralViewTransitionTracker.Transition> transitions =
                reconcile(runtime, tracker, suppressedViewers, loadedEntityIds);
        for (AstralViewTransitionTracker.Transition transition : transitions) {
            sender.accept(transition.viewerId(), transition.payload());
        }
        return transitions.size();
    }
}
