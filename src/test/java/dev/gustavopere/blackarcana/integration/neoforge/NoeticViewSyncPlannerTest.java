package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.OptionalInt;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NoeticViewSyncPlannerTest {
    @Test
    void projectsOnlyBorrowedSightWithViewerScopedLoadedTargets() {
        UUID borrowedViewer = UUID.randomUUID();
        UUID borrowedTarget = UUID.randomUUID();
        UUID namescryViewer = UUID.randomUUID();
        UUID namescryTarget = UUID.randomUUID();
        UUID astralViewer = UUID.randomUUID();
        UUID astralTarget = UUID.randomUUID();
        UUID missingViewer = UUID.randomUUID();
        UUID missingTarget = UUID.randomUUID();

        List<NoeticObservationRuntime.ActiveSession> sessions = List.of(
                new NoeticObservationRuntime.ActiveSession(
                        borrowedViewer, borrowedTarget, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L),
                new NoeticObservationRuntime.ActiveSession(
                        namescryViewer, namescryTarget, NoeticObservationKind.NAMESCRY, 10L, 30L),
                new NoeticObservationRuntime.ActiveSession(
                        astralViewer, astralTarget, NoeticObservationKind.ASTRAL_SEVERANCE, 10L, 30L),
                new NoeticObservationRuntime.ActiveSession(
                        missingViewer, missingTarget, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L));

        Map<UUID, NoeticViewTransitionTracker.Desired> desired = NoeticViewSyncPlanner.project(
                sessions,
                (viewerId, targetId) -> viewerId.equals(borrowedViewer) && targetId.equals(borrowedTarget)
                        ? OptionalInt.of(17)
                        : OptionalInt.empty());

        assertEquals(Map.of(
                borrowedViewer,
                new NoeticViewTransitionTracker.Desired(NoeticObservationKind.BORROWED_SIGHT, 17)), desired);
    }

    @Test
    void negativeResolvedEntityIdsFailClosedInsteadOfCreatingCameraAuthority() {
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        List<NoeticObservationRuntime.ActiveSession> sessions = List.of(
                new NoeticObservationRuntime.ActiveSession(
                        viewer, target, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L));

        assertEquals(Map.of(), NoeticViewSyncPlanner.project(
                sessions,
                (viewerId, targetId) -> OptionalInt.of(-1)));
    }
}
