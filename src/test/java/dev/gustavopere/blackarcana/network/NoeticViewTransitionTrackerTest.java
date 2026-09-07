package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NoeticViewTransitionTrackerTest {
    @Test
    void beginIsDeduplicatedAndEndIsEmittedExactlyOnce() {
        NoeticViewTransitionTracker tracker = new NoeticViewTransitionTracker(2);
        UUID viewer = UUID.randomUUID();
        NoeticViewTransitionTracker.Desired desired = new NoeticViewTransitionTracker.Desired(
                NoeticObservationKind.BORROWED_SIGHT, 17);

        assertEquals(List.of(new NoeticViewPayload(
                        ArcanaProtocol.VERSION,
                        NoeticViewPayload.Action.BEGIN,
                        NoeticObservationKind.BORROWED_SIGHT,
                        17)),
                tracker.reconcile(viewer, Optional.of(desired)));
        assertTrue(tracker.reconcile(viewer, Optional.of(desired)).isEmpty());
        assertEquals(List.of(new NoeticViewPayload(
                        ArcanaProtocol.VERSION,
                        NoeticViewPayload.Action.END,
                        NoeticObservationKind.BORROWED_SIGHT,
                        17)),
                tracker.reconcile(viewer, Optional.empty()));
        assertTrue(tracker.reconcile(viewer, Optional.empty()).isEmpty());
        assertEquals(0, tracker.trackedCount());
    }

    @Test
    void changingCameraTargetEndsOldViewBeforeBeginningNewOne() {
        NoeticViewTransitionTracker tracker = new NoeticViewTransitionTracker(2);
        UUID viewer = UUID.randomUUID();
        tracker.reconcile(viewer, Optional.of(new NoeticViewTransitionTracker.Desired(
                NoeticObservationKind.BORROWED_SIGHT, 17)));

        assertEquals(List.of(
                        new NoeticViewPayload(
                                ArcanaProtocol.VERSION,
                                NoeticViewPayload.Action.END,
                                NoeticObservationKind.BORROWED_SIGHT,
                                17),
                        new NoeticViewPayload(
                                ArcanaProtocol.VERSION,
                                NoeticViewPayload.Action.BEGIN,
                                NoeticObservationKind.ASTRAL_SEVERANCE,
                                29)),
                tracker.reconcile(viewer, Optional.of(new NoeticViewTransitionTracker.Desired(
                        NoeticObservationKind.ASTRAL_SEVERANCE, 29))));
    }

    @Test
    void saturationAndMalformedDesiredStateFailClosed() {
        NoeticViewTransitionTracker tracker = new NoeticViewTransitionTracker(1);
        UUID first = UUID.randomUUID();
        UUID second = UUID.randomUUID();
        NoeticViewTransitionTracker.Desired desired = new NoeticViewTransitionTracker.Desired(
                NoeticObservationKind.BORROWED_SIGHT, 4);
        tracker.reconcile(first, Optional.of(desired));

        assertTrue(tracker.reconcile(second, Optional.of(desired)).isEmpty());
        assertEquals(1, tracker.trackedCount());
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewTransitionTracker.Desired(
                NoeticObservationKind.NAMESCRY, 4));
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewTransitionTracker.Desired(
                NoeticObservationKind.BORROWED_SIGHT, -1));
    }
}
