package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEmergencyProtectionStateServiceTest {
    private static final UUID PLAYER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static final String RESOURCE = "black_arcana:containment_mask";

    @Test
    void reservationIsExclusiveAndRefundMakesResourceImmediatelyAvailableAgain() {
        ArcaneEmergencyProtectionStateService service = ArcaneEmergencyProtectionStateService.canonical(32);

        var first = service.reserve(PLAYER, RESOURCE, 100L, 200L);
        assertTrue(first.decision().allowed());

        var overlapping = service.reserve(PLAYER, RESOURCE, 100L, 200L);
        assertFalse(overlapping.decision().allowed());
        assertEquals("emergency_resource_busy", overlapping.decision().code());

        first.refund();
        var retried = service.reserve(PLAYER, RESOURCE, 100L, 200L);
        assertTrue(retried.decision().allowed());
        retried.refund();
    }

    @Test
    void commitStartsPersistentCooldownExactlyOnce() {
        ArcaneEmergencyProtectionStateService service = ArcaneEmergencyProtectionStateService.canonical(32);

        var lease = service.reserve(PLAYER, RESOURCE, 100L, 200L);
        assertTrue(lease.decision().allowed());
        lease.commit();
        lease.commit();

        assertEquals(300L, service.readyAtTick(PLAYER, RESOURCE));
        var beforeReady = service.reserve(PLAYER, RESOURCE, 299L, 200L);
        assertFalse(beforeReady.decision().allowed());
        assertEquals("emergency_resource_cooldown", beforeReady.decision().code());

        var ready = service.reserve(PLAYER, RESOURCE, 300L, 200L);
        assertTrue(ready.decision().allowed());
        ready.refund();
    }

    @Test
    void cooldownSurvivesSnapshotAndRestore() {
        ArcaneEmergencyProtectionStateService source = ArcaneEmergencyProtectionStateService.canonical(32);
        var lease = source.reserve(PLAYER, RESOURCE, 25L, 400L);
        lease.commit();

        ArcaneEmergencyProtectionStateService restored = ArcaneEmergencyProtectionStateService.canonical(32);
        restored.restoreSnapshot(source.persistentSnapshot());

        assertEquals(425L, restored.readyAtTick(PLAYER, RESOURCE));
        assertFalse(restored.reserve(PLAYER, RESOURCE, 424L, 400L).decision().allowed());
    }
}
