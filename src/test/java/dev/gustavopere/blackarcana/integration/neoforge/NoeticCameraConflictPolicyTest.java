package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NoeticCameraConflictPolicyTest {
    @Test
    void simultaneousBorrowedSightAndAstralForSameViewerSuppressBothPresentations() {
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        UUID projection = UUID.randomUUID();

        assertEquals(Set.of(viewer), NoeticCameraConflictPolicy.conflictedViewers(
                List.of(new NoeticObservationRuntime.ActiveSession(
                        viewer, target, NoeticObservationKind.BORROWED_SIGHT, 10L, 30L)),
                List.of(projection(viewer, projection))));
    }

    @Test
    void otherObservationKindsAndDifferentViewersDoNotCreateCameraPriority() {
        UUID viewer = UUID.randomUUID();
        UUID other = UUID.randomUUID();

        assertEquals(Set.of(), NoeticCameraConflictPolicy.conflictedViewers(
                List.of(
                        new NoeticObservationRuntime.ActiveSession(
                                viewer, UUID.randomUUID(), NoeticObservationKind.NAMESCRY, 10L, 30L),
                        new NoeticObservationRuntime.ActiveSession(
                                other, UUID.randomUUID(), NoeticObservationKind.BORROWED_SIGHT, 10L, 30L)),
                List.of(projection(viewer, UUID.randomUUID()))));
    }

    private static AstralSeveranceRuntime.ActiveProjection projection(UUID caster, UUID projection) {
        AstralSeveranceRuntime.ProjectionPose pose =
                new AstralSeveranceRuntime.ProjectionPose(1.0D, 2.0D, 3.0D, 0.0F, 0.0F);
        return new AstralSeveranceRuntime.ActiveProjection(
                projection, caster, caster, 10L, 30L, 16.0D, pose, pose, 0L);
    }
}
