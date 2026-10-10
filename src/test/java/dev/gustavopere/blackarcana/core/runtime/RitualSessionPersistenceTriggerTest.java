package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.core.ritual.RitualEngine;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Persistence capture is mandatory after any authoritative ritual transition. */
class RitualSessionPersistenceTriggerTest {
    @Test
    void quietTickDoesNotForceAnExtraSnapshotCapture() {
        assertFalse(ArcanaServerRuntimeManager.ritualStateChanged(
                new RitualEngine.TickSummary(0, 0, 0)));
    }

    @Test
    void successfulCommitRequiresSnapshotBeforeNextPeriodicSave() {
        assertTrue(ArcanaServerRuntimeManager.ritualStateChanged(
                new RitualEngine.TickSummary(1, 0, 0)));
    }

    @Test
    void outcomeCompletionRequiresSnapshotBeforeNextPeriodicSave() {
        assertTrue(ArcanaServerRuntimeManager.ritualStateChanged(
                new RitualEngine.TickSummary(0, 1, 0)));
    }

    @Test
    void failureCancellationRequiresSnapshotBeforeNextPeriodicSave() {
        assertTrue(ArcanaServerRuntimeManager.ritualStateChanged(
                new RitualEngine.TickSummary(0, 0, 1)));
    }

    @Test
    void multipleTransitionsStillRequireOnlyOneCaptureForTheTick() {
        assertTrue(ArcanaServerRuntimeManager.ritualStateChanged(
                new RitualEngine.TickSummary(12, 7, 3)));
    }
}
