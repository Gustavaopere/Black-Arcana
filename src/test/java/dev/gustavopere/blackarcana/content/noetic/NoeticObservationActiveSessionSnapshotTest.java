package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NoeticObservationActiveSessionSnapshotTest {
    @Test
    void snapshotIsImmutableBoundedDataAndTracksCanonicalLifecycle() {
        NoeticObservationRuntime runtime = new NoeticObservationRuntime(2);
        UUID viewerA = UUID.randomUUID();
        UUID targetA = UUID.randomUUID();
        UUID viewerB = UUID.randomUUID();
        UUID targetB = UUID.randomUUID();

        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerA, targetA, NoeticObservationKind.BORROWED_SIGHT, 10L, 20));
        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerB, targetB, NoeticObservationKind.NAMESCRY, 11L, 20));

        List<NoeticObservationRuntime.ActiveSession> snapshot = runtime.activeSessions();
        assertEquals(List.of(
                new NoeticObservationRuntime.ActiveSession(
                        viewerA, targetA, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L),
                new NoeticObservationRuntime.ActiveSession(
                        viewerB, targetB, NoeticObservationKind.NAMESCRY, 11L, 31L)),
                snapshot);
        assertThrows(UnsupportedOperationException.class, () -> snapshot.clear());

        runtime.close(viewerA, NoeticObservationSession.CloseReason.EXPLICIT);
        assertEquals(1, runtime.activeSessions().size());
        assertEquals(viewerB, runtime.activeSessions().getFirst().viewerId());

        runtime.expire(31L);
        assertEquals(List.of(), runtime.activeSessions());

        // Prior snapshots are immutable value copies, not handles to mutable session state.
        assertEquals(2, snapshot.size());
    }
}
