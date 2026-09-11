package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.ArrayDeque;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralProjectionMovementRuntimeTest {
    @Test
    void projectionOwnsImmutableOriginAndServerUpdatedCurrentPose() {
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, () -> projectionId);
        UUID casterId = UUID.randomUUID();
        AstralProjectionPose origin = new AstralProjectionPose(12.5D, 70.0D, -4.5D, 0.0F, 0.0F);

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterId, 10L, 100, 8.0D, origin));

        var started = runtime.projection(casterId).orElseThrow();
        assertEquals(origin, started.originPose());
        assertEquals(origin, started.currentPose());

        assertEquals(AstralSeveranceRuntime.MoveResult.MOVED,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 1L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));

        var moved = runtime.projection(casterId).orElseThrow();
        assertEquals(origin, moved.originPose(), "movement must never rewrite the physical-body origin");
        assertNotEquals(origin, moved.currentPose(), "server must advance only the projection pose");
        assertEquals(1L, moved.lastAcceptedMovementSequence());
        assertEquals(NoeticSafetyCeilings.MAX_ASTRAL_STEP_BLOCKS_PER_INTENT,
                origin.distanceTo(moved.currentPose()), 1.0E-9D);
    }

    @Test
    void staleForeignInvalidAndPostCloseMovementIntentFailsClosed() {
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, () -> projectionId);
        UUID casterId = UUID.randomUUID();
        AstralProjectionPose origin = new AstralProjectionPose(0.0D, 64.0D, 0.0D, 0.0F, 0.0F);

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterId, 0L, 100, 8.0D, origin));

        assertEquals(AstralSeveranceRuntime.MoveResult.WRONG_PROJECTION,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        UUID.randomUUID(), 1L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));
        assertEquals(AstralSeveranceRuntime.MoveResult.INVALID_INTENT,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 1L, 0.0F, 1.1F, 0.0F, 0.0F, 0.0F)));

        assertEquals(AstralSeveranceRuntime.MoveResult.MOVED,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 1L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));
        AstralProjectionPose accepted = runtime.projection(casterId).orElseThrow().currentPose();

        assertEquals(AstralSeveranceRuntime.MoveResult.STALE_SEQUENCE,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 1L, 1.0F, 0.0F, 0.0F, 90.0F, 0.0F)));
        assertEquals(accepted, runtime.projection(casterId).orElseThrow().currentPose());

        assertEquals(AstralSeveranceRuntime.MoveResult.NO_ACTIVE_PROJECTION,
                runtime.move(UUID.randomUUID(), new AstralProjectionMovementIntent(
                        projectionId, 2L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));

        runtime.close(casterId, AstralSeveranceRuntime.CloseReason.EXPLICIT_RETURN);
        assertEquals(AstralSeveranceRuntime.MoveResult.NO_ACTIVE_PROJECTION,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 2L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));
    }

    @Test
    void hardRangeRejectsMovementWithoutAdvancingPoseOrSequence() {
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, () -> projectionId);
        UUID casterId = UUID.randomUUID();
        AstralProjectionPose origin = new AstralProjectionPose(0.0D, 64.0D, 0.0D, 0.0F, 0.0F);

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterId, 0L, 100, 1.25D, origin));
        assertEquals(AstralSeveranceRuntime.MoveResult.MOVED,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 1L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));

        var beforeRejectedMove = runtime.projection(casterId).orElseThrow();
        assertEquals(AstralSeveranceRuntime.MoveResult.OUT_OF_RANGE,
                runtime.move(casterId, new AstralProjectionMovementIntent(
                        projectionId, 2L, 0.0F, 1.0F, 0.0F, 0.0F, 0.0F)));
        var afterRejectedMove = runtime.projection(casterId).orElseThrow();

        assertEquals(beforeRejectedMove.currentPose(), afterRejectedMove.currentPose());
        assertEquals(1L, afterRejectedMove.lastAcceptedMovementSequence());
    }

    @Test
    void poseAndIntentRejectNonFiniteOrStructurallyInvalidValues() {
        assertThrows(IllegalArgumentException.class,
                () -> new AstralProjectionPose(Double.NaN, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class,
                () -> new AstralProjectionPose(0.0D, 0.0D, 0.0D, Float.POSITIVE_INFINITY, 0.0F));
        assertThrows(IllegalArgumentException.class,
                () -> new AstralProjectionPose(0.0D, 0.0D, 0.0D, 0.0F, 91.0F));
        assertThrows(IllegalArgumentException.class,
                () -> new AstralProjectionMovementIntent(
                        UUID.randomUUID(), 0L, 0.0F, 0.0F, 0.0F, 0.0F, 0.0F));
    }
}
