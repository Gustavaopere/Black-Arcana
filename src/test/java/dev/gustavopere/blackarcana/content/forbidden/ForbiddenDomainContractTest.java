package dev.gustavopere.blackarcana.content.forbidden;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ForbiddenDomainContractTest {
    @Test
    void localizedFieldSpecIsBoundedAndTemporaryDimensionsAreRejected() {
        ForbiddenDomainSpec spec = new ForbiddenDomainSpec(
                "black_arcana:forbidden_domain",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                16,
                600,
                32,
                256
        );
        assertEquals(16, spec.radius());
        assertEquals(600, spec.durationTicks());
        assertThrows(IllegalArgumentException.class, () -> new ForbiddenDomainSpec(
                "black_arcana:too_large",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                ForbiddenDomainSafetyCeilings.MAX_RADIUS + 1,
                600,
                32,
                256
        ));
        assertThrows(IllegalArgumentException.class, () -> new ForbiddenDomainSpec(
                "black_arcana:too_long",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                16,
                ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS + 1,
                32,
                256
        ));
        assertThrows(IllegalArgumentException.class, () -> new ForbiddenDomainSpec(
                "black_arcana:too_many_entities",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                16,
                600,
                ForbiddenDomainSafetyCeilings.MAX_TRACKED_ENTITIES + 1,
                256
        ));
        assertThrows(IllegalArgumentException.class, () -> new ForbiddenDomainSpec(
                "black_arcana:too_much_restoration",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                16,
                600,
                32,
                ForbiddenDomainSafetyCeilings.MAX_RESTORATION_POSITIONS + 1
        ));
        assertThrows(IllegalArgumentException.class, () -> new ForbiddenDomainSpec(
                "black_arcana:dynamic_dimension",
                ForbiddenDomainMode.TEMPORARY_DIMENSION,
                16,
                600,
                32,
                256
        ));
    }

    @Test
    void admissionFailsClosedOnAnyUnknownOrUnsafeWorldBoundary() {
        assertTrue(new ForbiddenDomainAdmission(true, true, true, true).admitted());
        assertFalse(new ForbiddenDomainAdmission(false, true, true, true).admitted());
        assertFalse(new ForbiddenDomainAdmission(true, false, true, true).admitted());
        assertFalse(new ForbiddenDomainAdmission(true, true, false, true).admitted());
        assertFalse(new ForbiddenDomainAdmission(true, true, true, false).admitted());
    }

    @Test
    void runtimeEnforcesOwnerGlobalParticipantAndExactlyOnceCloseContracts() {
        ForbiddenDomainSpec spec = new ForbiddenDomainSpec(
                "black_arcana:test_domain",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                8,
                40,
                2,
                32
        );
        ForbiddenDomainRuntime runtime = new ForbiddenDomainRuntime(2);
        UUID ownerA = UUID.randomUUID();
        UUID ownerB = UUID.randomUUID();
        UUID ownerC = UUID.randomUUID();
        UUID participantA = UUID.randomUUID();
        UUID participantB = UUID.randomUUID();
        UUID participantC = UUID.randomUUID();

        assertEquals(ForbiddenDomainRuntime.StartResult.STARTED, runtime.start(ownerA, spec, 100));
        assertEquals(ForbiddenDomainRuntime.StartResult.OWNER_ALREADY_ACTIVE, runtime.start(ownerA, spec, 100));
        assertEquals(ForbiddenDomainRuntime.StartResult.STARTED, runtime.start(ownerB, spec, 100));
        assertEquals(ForbiddenDomainRuntime.StartResult.GLOBAL_LIMIT, runtime.start(ownerC, spec, 100));

        assertTrue(runtime.trackParticipant(ownerA, participantA));
        assertTrue(runtime.trackParticipant(ownerA, participantA));
        assertTrue(runtime.trackParticipant(ownerA, participantB));
        assertFalse(runtime.trackParticipant(ownerA, participantC));
        assertEquals(2, runtime.session(ownerA).orElseThrow().participantCount());

        assertTrue(runtime.close(ownerA, ForbiddenDomainSession.CloseReason.EXPLICIT));
        assertFalse(runtime.close(ownerA, ForbiddenDomainSession.CloseReason.EXPLICIT));
        assertEquals(1, runtime.activeCount());
    }

    @Test
    void expiryAndServerStopCleanupCannotLeaveOrphanSessions() {
        ForbiddenDomainSpec spec = new ForbiddenDomainSpec(
                "black_arcana:test_domain",
                ForbiddenDomainMode.LOCALIZED_FIELD,
                8,
                20,
                8,
                32
        );
        ForbiddenDomainRuntime runtime = new ForbiddenDomainRuntime(ForbiddenDomainSafetyCeilings.MAX_ACTIVE_DOMAINS);
        UUID first = UUID.randomUUID();
        UUID second = UUID.randomUUID();
        assertEquals(ForbiddenDomainRuntime.StartResult.STARTED, runtime.start(first, spec, 100));
        assertEquals(ForbiddenDomainRuntime.StartResult.STARTED, runtime.start(second, spec, 100));

        assertEquals(1, runtime.expire(119));
        assertEquals(1, runtime.activeCount());
        assertEquals(1, runtime.expire(120));
        assertEquals(0, runtime.activeCount());

        runtime.start(first, spec, 200);
        runtime.start(second, spec, 200);
        assertEquals(2, runtime.clearForServerStop());
        assertEquals(0, runtime.activeCount());
    }
}
