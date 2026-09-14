package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.OptionalInt;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NoeticViewSuppressionTest {
    @Test
    void conflictedBorrowedSightViewerProducesNoDesiredCameraState() {
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        List<NoeticObservationRuntime.ActiveSession> sessions = List.of(
                new NoeticObservationRuntime.ActiveSession(
                        viewer, target, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L));

        assertEquals(java.util.Map.of(), NoeticViewSyncPlanner.project(
                sessions,
                Set.of(viewer),
                (viewerId, targetId) -> OptionalInt.of(17)));
    }
}
