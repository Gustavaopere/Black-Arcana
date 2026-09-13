package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceControlRuntimeTest {
    @Test
    void serverOwnedPoseRejectsForeignReplayRangeAndUnavailableDestinations() {
        UUID caster = UUID.randomUUID();
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(1, () -> projectionId);
        AstralSeveranceRuntime.ProjectionPose origin =
                new AstralSeveranceRuntime.ProjectionPose(10.0D, 64.0D, 10.0D, 0.0F, 0.0F);

        assertEquals(
                AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(caster, 100L, 40, 3.0D, origin));

        var started = runtime.projection(caster).orElseThrow();
        assertEquals(origin, started.originPose());
        assertEquals(origin, started.pose());
        assertEquals(0L, started.lastProcessedControlSequence());
        assertEquals(caster, started.physicalBodyId());

        AstralSeveranceRuntime.ControlLimits limits =
                new AstralSeveranceRuntime.ControlLimits(2.0D, 45.0F);

        assertEquals(
                AstralSeveranceRuntime.ControlResult.SESSION_MISMATCH,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                UUID.randomUUID(), 1L, 0.0D, 0.0D, 1.0D, 0.0F, 0.0F),
                        limits,
                        pose -> true));
        assertEquals(origin, runtime.projection(caster).orElseThrow().pose());

        assertEquals(
                AstralSeveranceRuntime.ControlResult.APPLIED,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 1L, 0.0D, 0.0D, 1.0D, 0.0F, 0.0F),
                        limits,
                        pose -> true));
        var moved = runtime.projection(caster).orElseThrow();
        assertEquals(10.0D, moved.pose().x(), 1.0E-9D);
        assertEquals(64.0D, moved.pose().y(), 1.0E-9D);
        assertEquals(12.0D, moved.pose().z(), 1.0E-9D);
        assertEquals(1L, moved.lastProcessedControlSequence());

        assertEquals(
                AstralSeveranceRuntime.ControlResult.STALE_SEQUENCE,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 1L, 0.0D, 0.0D, 1.0D, 0.0F, 0.0F),
                        limits,
                        pose -> true));
        assertEquals(12.0D, runtime.projection(caster).orElseThrow().pose().z(), 1.0E-9D);

        assertEquals(
                AstralSeveranceRuntime.ControlResult.OUT_OF_RANGE,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 2L, 0.0D, 0.0D, 1.0D, 0.0F, 0.0F),
                        limits,
                        pose -> true));
        var rangeRefused = runtime.projection(caster).orElseThrow();
        assertEquals(12.0D, rangeRefused.pose().z(), 1.0E-9D);
        assertEquals(2L, rangeRefused.lastProcessedControlSequence());

        assertEquals(
                AstralSeveranceRuntime.ControlResult.DESTINATION_UNAVAILABLE,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 3L, 1.0D, 0.0D, 0.0D, 0.0F, 0.0F),
                        limits,
                        pose -> false));
        var unavailable = runtime.projection(caster).orElseThrow();
        assertEquals(12.0D, unavailable.pose().z(), 1.0E-9D);
        assertEquals(3L, unavailable.lastProcessedControlSequence());

        assertTrue(runtime.requestReturn(caster, projectionId));
        assertFalse(runtime.projection(caster).isPresent());
        assertEquals(
                AstralSeveranceRuntime.ControlResult.NO_ACTIVE_PROJECTION,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 4L, 0.0D, 0.0D, 1.0D, 0.0F, 0.0F),
                        limits,
                        pose -> true));
    }

    @Test
    void controlIntentIsAxesOnlyAndFailsClosedOnInvalidNumericInput() {
        UUID caster = UUID.randomUUID();
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(1, () -> projectionId);
        var origin = new AstralSeveranceRuntime.ProjectionPose(0.0D, 80.0D, 0.0D, 0.0F, 0.0F);
        assertEquals(
                AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(caster, 1L, 20, 8.0D, origin));

        assertEquals(
                AstralSeveranceRuntime.ControlResult.INVALID_INTENT,
                runtime.applyControl(
                        caster,
                        new AstralSeveranceRuntime.ControlIntent(
                                projectionId, 1L, Double.NaN, 0.0D, 0.0D, 0.0F, 0.0F),
                        new AstralSeveranceRuntime.ControlLimits(1.0D, 30.0F),
                        pose -> true));
        assertEquals(origin, runtime.projection(caster).orElseThrow().pose());
        assertEquals(0L, runtime.projection(caster).orElseThrow().lastProcessedControlSequence());
    }
}
