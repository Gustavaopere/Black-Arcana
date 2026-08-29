package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtection;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEmergencyProtectionCoordinatorTest {
    @Test
    void commitsExactlyOnceAndPreservesUnavoidableFloor() {
        AtomicInteger commits = new AtomicInteger();
        AtomicInteger refunds = new AtomicInteger();
        ArcaneEmergencyProtection provider = provider("black_arcana:test_charm", 100.0D, commits, refunds);
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of(provider));
        ArcanaDamageInstanceId id = ArcanaDamageInstanceId.random();
        var query = new ArcaneEmergencyProtection.Query(UUID.randomUUID(), id, 20.0D, 7.0D, true);

        var first = coordinator.protect(query);
        assertTrue(first.consumed());
        assertEquals(13.0D, first.absorbed());
        assertEquals(7.0D, first.remainingBacklash());
        assertEquals(1, commits.get());
        assertEquals(0, refunds.get());

        var duplicate = coordinator.protect(query);
        assertFalse(duplicate.consumed());
        assertEquals("already_processed", duplicate.sourceId());
        assertEquals(1, commits.get());
    }

    @Test
    void invalidOrDepletedReservationDoesNotConsumeIdentity() {
        AtomicInteger commits = new AtomicInteger();
        AtomicInteger refunds = new AtomicInteger();
        ArcaneEmergencyProtection depleted = provider("black_arcana:depleted", 0.0D, commits, refunds);
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of(depleted));
        ArcanaDamageInstanceId id = ArcanaDamageInstanceId.random();

        var result = coordinator.protect(new ArcaneEmergencyProtection.Query(
            UUID.randomUUID(), id, 10.0D, 2.0D, true));

        assertFalse(result.consumed());
        assertEquals(10.0D, result.remainingBacklash());
        assertEquals(0, commits.get());
        assertEquals(1, refunds.get());
        assertFalse(coordinator.wasCommitted(id));
    }

    @Test
    void profileCanDisableEmergencyProtectionEntirely() {
        AtomicInteger commits = new AtomicInteger();
        AtomicInteger refunds = new AtomicInteger();
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of(
            provider("black_arcana:unused", 5.0D, commits, refunds)));

        var result = coordinator.protect(new ArcaneEmergencyProtection.Query(
            UUID.randomUUID(), ArcanaDamageInstanceId.random(), 10.0D, 0.0D, false));

        assertFalse(result.consumed());
        assertEquals(0, commits.get());
        assertEquals(0, refunds.get());
    }

    private static ArcaneEmergencyProtection provider(
        String id,
        double absorption,
        AtomicInteger commits,
        AtomicInteger refunds
    ) {
        return new ArcaneEmergencyProtection() {
            @Override public String providerId() { return id; }
            @Override public Reservation reserve(Query query) {
                return new Reservation() {
                    private boolean terminal;
                    @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    @Override public double absorption() { return absorption; }
                    @Override public void commit() { if (!terminal) { terminal = true; commits.incrementAndGet(); } }
                    @Override public void refund() { if (!terminal) { terminal = true; refunds.incrementAndGet(); } }
                };
            }
        };
    }
}
