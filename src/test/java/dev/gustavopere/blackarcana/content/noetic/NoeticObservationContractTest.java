package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NoeticObservationContractTest {
    @Test
    void safetyCeilingsBoundRangeDurationAndConcurrentSessions() {
        assertTrue(NoeticSafetyCeilings.MAX_RANGE_BLOCKS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_DURATION_TICKS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS > 0);
        assertThrows(IllegalArgumentException.class,
                () -> new NoeticObservationRuntime(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS + 1));

        NoeticObservationRuntime runtime = new NoeticObservationRuntime(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);
        UUID viewer = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        assertEquals(NoeticObservationRuntime.StartResult.INVALID_DURATION,
                runtime.start(viewer, target, NoeticObservationKind.NAMESCRY, 10L, 0));
        assertEquals(NoeticObservationRuntime.StartResult.INVALID_DURATION,
                runtime.start(viewer, target, NoeticObservationKind.NAMESCRY, 10L,
                        NoeticSafetyCeilings.MAX_DURATION_TICKS + 1));
    }

    @Test
    void namescryPlayerPrivacyAndBorrowedSightOwnershipFailClosed() {
        NoeticObservationFacts safeNpc = new NoeticObservationFacts(
                true, true, true, true, true, false, false, false);
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.NAMESCRY, safeNpc).allowed());

        NoeticObservationFacts privatePlayer = new NoeticObservationFacts(
                true, true, true, true, true, true, false, false);
        assertFalse(NoeticObservationPolicy.authorize(NoeticObservationKind.NAMESCRY, privatePlayer).allowed());

        NoeticObservationFacts consentingPlayer = new NoeticObservationFacts(
                true, true, true, true, true, true, true, false);
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.NAMESCRY, consentingPlayer).allowed());

        NoeticObservationFacts ownedFamiliar = new NoeticObservationFacts(
                true, true, true, false, true, false, false, true);
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.BORROWED_SIGHT, ownedFamiliar).allowed());

        NoeticObservationFacts foreignFamiliar = new NoeticObservationFacts(
                true, true, true, false, true, false, false, false);
        assertFalse(NoeticObservationPolicy.authorize(NoeticObservationKind.BORROWED_SIGHT, foreignFamiliar).allowed());

        NoeticObservationFacts consentingBondedTarget = new NoeticObservationFacts(
                true, true, true, false, true, false, true, false);
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.BORROWED_SIGHT, consentingBondedTarget).allowed());
    }

    @Test
    void allObservationKindsRejectUnloadedWrongDimensionOutOfRangeOrDeadTargets() {
        NoeticObservationFacts unloaded = new NoeticObservationFacts(
                false, true, true, true, true, false, true, true);
        NoeticObservationFacts wrongDimension = new NoeticObservationFacts(
                true, false, true, true, true, false, true, true);
        NoeticObservationFacts outOfRange = new NoeticObservationFacts(
                true, true, false, true, true, false, true, true);
        NoeticObservationFacts dead = new NoeticObservationFacts(
                true, true, true, true, false, false, true, true);

        for (NoeticObservationKind kind : NoeticObservationKind.values()) {
            assertFalse(NoeticObservationPolicy.authorize(kind, unloaded).allowed(), kind + " must reject unloaded targets");
            assertFalse(NoeticObservationPolicy.authorize(kind, wrongDimension).allowed(), kind + " must reject cross-dimension targets");
            assertFalse(NoeticObservationPolicy.authorize(kind, outOfRange).allowed(), kind + " must reject out-of-range targets");
            assertFalse(NoeticObservationPolicy.authorize(kind, dead).allowed(), kind + " must reject dead targets");
        }
    }

    @Test
    void occultAppraisalRequiresLineOfSightButRemoteModesDoNotInventThatRequirement() {
        NoeticObservationFacts noLineOfSight = new NoeticObservationFacts(
                true, true, true, false, true, false, true, true);
        assertFalse(NoeticObservationPolicy.authorize(NoeticObservationKind.OCCULT_APPRAISAL, noLineOfSight).allowed());
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.NAMESCRY, noLineOfSight).allowed());
        assertTrue(NoeticObservationPolicy.authorize(NoeticObservationKind.BORROWED_SIGHT, noLineOfSight).allowed());
    }

    @Test
    void runtimeEnforcesOneSessionPerViewerGlobalLimitExpiryAndExactlyOnceClose() {
        NoeticObservationRuntime runtime = new NoeticObservationRuntime(2);
        UUID viewerA = UUID.randomUUID();
        UUID viewerB = UUID.randomUUID();
        UUID viewerC = UUID.randomUUID();
        UUID targetA = UUID.randomUUID();
        UUID targetB = UUID.randomUUID();
        UUID targetC = UUID.randomUUID();

        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerA, targetA, NoeticObservationKind.NAMESCRY, 100L, 20));
        assertEquals(NoeticObservationRuntime.StartResult.VIEWER_ALREADY_ACTIVE,
                runtime.start(viewerA, targetB, NoeticObservationKind.BORROWED_SIGHT, 100L, 20));
        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerB, targetB, NoeticObservationKind.OCCULT_APPRAISAL, 101L, 20));
        assertEquals(NoeticObservationRuntime.StartResult.GLOBAL_LIMIT,
                runtime.start(viewerC, targetC, NoeticObservationKind.NAMESCRY, 101L, 20));
        assertEquals(2, runtime.activeCount());

        assertTrue(runtime.close(viewerA, NoeticObservationSession.CloseReason.EXPLICIT));
        assertFalse(runtime.close(viewerA, NoeticObservationSession.CloseReason.EXPLICIT));
        assertEquals(1, runtime.activeCount());

        assertEquals(0, runtime.expire(120L));
        assertEquals(1, runtime.expire(121L));
        assertEquals(0, runtime.activeCount());
    }

    @Test
    void viewerAndTargetLifecycleCleanupCannotLeaveOrphanSessions() {
        NoeticObservationRuntime runtime = new NoeticObservationRuntime(3);
        UUID viewerA = UUID.randomUUID();
        UUID viewerB = UUID.randomUUID();
        UUID target = UUID.randomUUID();

        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerA, target, NoeticObservationKind.NAMESCRY, 1L, 40));
        assertEquals(NoeticObservationRuntime.StartResult.STARTED,
                runtime.start(viewerB, target, NoeticObservationKind.BORROWED_SIGHT, 1L, 40));

        assertTrue(runtime.clearViewer(viewerA, NoeticObservationSession.CloseReason.VIEWER_LOGOUT));
        assertFalse(runtime.clearViewer(viewerA, NoeticObservationSession.CloseReason.VIEWER_LOGOUT));
        assertEquals(1, runtime.clearTarget(target));
        assertEquals(0, runtime.activeCount());

        runtime.start(viewerA, UUID.randomUUID(), NoeticObservationKind.OCCULT_APPRAISAL, 50L, 20);
        runtime.start(viewerB, UUID.randomUUID(), NoeticObservationKind.NAMESCRY, 50L, 20);
        assertEquals(2, runtime.clearForServerStop());
        assertEquals(0, runtime.activeCount());
    }
}
