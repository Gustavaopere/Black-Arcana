package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralViewTransitionTrackerTest {
    @Test
    void beginIsDeduplicatedAndEndIsEmittedExactlyOnce() {
        AstralViewTransitionTracker tracker = new AstralViewTransitionTracker(2);
        UUID viewer = UUID.randomUUID();
        UUID projection = UUID.randomUUID();
        AstralViewTransitionTracker.Desired desired = new AstralViewTransitionTracker.Desired(projection, 17);

        assertEquals(List.of(new AstralViewPayload(
                        ArcanaProtocol.VERSION,
                        AstralViewPayload.Action.BEGIN,
                        projection,
                        17)),
                tracker.reconcile(viewer, Optional.of(desired)));
        assertTrue(tracker.reconcile(viewer, Optional.of(desired)).isEmpty());
        assertEquals(List.of(new AstralViewPayload(
                        ArcanaProtocol.VERSION,
                        AstralViewPayload.Action.END,
                        projection,
                        17)),
                tracker.reconcile(viewer, Optional.empty()));
        assertTrue(tracker.reconcile(viewer, Optional.empty()).isEmpty());
        assertEquals(0, tracker.trackedCount());
    }

    @Test
    void changingProjectionEndsOldIdentityBeforeBeginningNewOne() {
        AstralViewTransitionTracker tracker = new AstralViewTransitionTracker(2);
        UUID viewer = UUID.randomUUID();
        UUID firstProjection = UUID.randomUUID();
        UUID secondProjection = UUID.randomUUID();
        tracker.reconcile(viewer, Optional.of(new AstralViewTransitionTracker.Desired(firstProjection, 17)));

        assertEquals(List.of(
                        new AstralViewPayload(
                                ArcanaProtocol.VERSION,
                                AstralViewPayload.Action.END,
                                firstProjection,
                                17),
                        new AstralViewPayload(
                                ArcanaProtocol.VERSION,
                                AstralViewPayload.Action.BEGIN,
                                secondProjection,
                                29)),
                tracker.reconcile(viewer, Optional.of(new AstralViewTransitionTracker.Desired(secondProjection, 29))));
    }

    @Test
    void canonicalBatchReconciliationClosesMissingViewers() {
        AstralViewTransitionTracker tracker = new AstralViewTransitionTracker(2);
        UUID first = UUID.randomUUID();
        UUID second = UUID.randomUUID();
        AstralViewTransitionTracker.Desired firstView =
                new AstralViewTransitionTracker.Desired(UUID.randomUUID(), 17);
        AstralViewTransitionTracker.Desired secondView =
                new AstralViewTransitionTracker.Desired(UUID.randomUUID(), 29);
        Map<UUID, AstralViewTransitionTracker.Desired> desired = new LinkedHashMap<>();
        desired.put(first, firstView);
        desired.put(second, secondView);

        assertEquals(2, tracker.reconcileAll(desired).size());
        assertTrue(tracker.reconcileAll(desired).isEmpty());
        List<AstralViewTransitionTracker.Transition> closed = tracker.reconcileAll(Map.of(second, secondView));
        assertEquals(1, closed.size());
        assertEquals(first, closed.getFirst().viewerId());
        assertEquals(AstralViewPayload.Action.END, closed.getFirst().payload().action());
        assertEquals(firstView.projectionId(), closed.getFirst().payload().projectionId());
    }

    @Test
    void capacityAndMalformedEntityIdsFailClosed() {
        AstralViewTransitionTracker tracker = new AstralViewTransitionTracker(1);
        Map<UUID, AstralViewTransitionTracker.Desired> oversized = new LinkedHashMap<>();
        oversized.put(UUID.randomUUID(), new AstralViewTransitionTracker.Desired(UUID.randomUUID(), 1));
        oversized.put(UUID.randomUUID(), new AstralViewTransitionTracker.Desired(UUID.randomUUID(), 2));

        assertThrows(IllegalArgumentException.class, () -> tracker.reconcileAll(oversized));
        assertEquals(0, tracker.trackedCount());
        assertThrows(IllegalArgumentException.class,
                () -> new AstralViewTransitionTracker.Desired(UUID.randomUUID(), -1));
    }
}
