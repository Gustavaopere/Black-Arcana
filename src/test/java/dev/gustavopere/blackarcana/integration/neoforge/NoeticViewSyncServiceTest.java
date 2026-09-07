package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationSession;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.OptionalInt;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NoeticViewSyncServiceTest {
    @Test
    void emitsBeginOnceThenEndWhenCanonicalSessionCloses() {
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        NoeticObservationRuntime runtime = new NoeticObservationRuntime(2);
        NoeticViewTransitionTracker tracker = new NoeticViewTransitionTracker(2);
        assertEquals(
                NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewer, target, NoeticObservationKind.BORROWED_SIGHT, 10L, 40));

        List<NoeticViewTransitionTracker.Transition> begin = NoeticViewSyncService.reconcile(
                runtime,
                tracker,
                id -> id.equals(target) ? OptionalInt.of(27) : OptionalInt.empty());
        assertEquals(List.of(new NoeticViewTransitionTracker.Transition(
                viewer,
                new NoeticViewPayload(
                        ArcanaProtocol.VERSION,
                        NoeticViewPayload.Action.BEGIN,
                        NoeticObservationKind.BORROWED_SIGHT,
                        27))), begin);

        assertEquals(List.of(), NoeticViewSyncService.reconcile(
                runtime,
                tracker,
                id -> id.equals(target) ? OptionalInt.of(27) : OptionalInt.empty()));

        runtime.close(viewer, NoeticObservationSession.CloseReason.EXPLICIT);
        assertEquals(List.of(new NoeticViewTransitionTracker.Transition(
                viewer,
                new NoeticViewPayload(
                        ArcanaProtocol.VERSION,
                        NoeticViewPayload.Action.END,
                        NoeticObservationKind.BORROWED_SIGHT,
                        27))), NoeticViewSyncService.reconcile(runtime, tracker, id -> OptionalInt.empty()));
        assertEquals(0, tracker.trackedCount());
    }

    @Test
    void loadedTargetLossEndsTrackedViewWithoutScanningPlayers() {
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        NoeticObservationRuntime runtime = new NoeticObservationRuntime(1);
        NoeticViewTransitionTracker tracker = new NoeticViewTransitionTracker(1);
        runtime.start(viewer, target, NoeticObservationKind.BORROWED_SIGHT, 0L, 20);

        NoeticViewSyncService.reconcile(runtime, tracker, id -> OptionalInt.of(9));

        assertEquals(List.of(new NoeticViewTransitionTracker.Transition(
                viewer,
                new NoeticViewPayload(
                        ArcanaProtocol.VERSION,
                        NoeticViewPayload.Action.END,
                        NoeticObservationKind.BORROWED_SIGHT,
                        9))), NoeticViewSyncService.reconcile(runtime, tracker, id -> OptionalInt.empty()));
        assertEquals(0, tracker.trackedCount());
    }
}
