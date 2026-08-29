package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneBacklashProtectionAttemptTrackerTest {
    @Test
    void exactTokenIdentityCarriesFrozenAttemptAndReleasesDeterministically() {
        ArcaneBacklashProtectionAttemptTracker<Object> tracker =
            new ArcaneBacklashProtectionAttemptTracker<>(2);
        Object token = new Object();
        var attempt = attempt("11111111-1111-1111-1111-111111111111");

        assertTrue(tracker.register(token, attempt));
        assertEquals(attempt, tracker.find(token).orElseThrow());
        assertEquals(1, tracker.size());
        assertEquals(attempt, tracker.release(token).orElseThrow());
        assertTrue(tracker.find(token).isEmpty());
        assertEquals(0, tracker.size());
    }

    @Test
    void duplicateTokenAndCapacityAreRejectedWithoutReplacingExistingAttempt() {
        ArcaneBacklashProtectionAttemptTracker<Object> tracker =
            new ArcaneBacklashProtectionAttemptTracker<>(1);
        Object first = new Object();
        Object second = new Object();
        var original = attempt("22222222-2222-2222-2222-222222222222");

        assertTrue(tracker.register(first, original));
        assertFalse(tracker.register(first, attempt("33333333-3333-3333-3333-333333333333")));
        assertFalse(tracker.register(second, attempt("44444444-4444-4444-4444-444444444444")));
        assertEquals(original, tracker.find(first).orElseThrow());
        assertEquals(1, tracker.size());
    }

    private static ArcaneBacklashProtectionAttemptTracker.Attempt attempt(String castId) {
        return new ArcaneBacklashProtectionAttemptTracker.Attempt(
            ArcanaCastId.parse(castId),
            ArcanaDamageInstanceId.random(),
            UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            true,
            new ArcaneEmergencyProtectionSnapshot(List.of(
                new ArcaneEmergencyProtectionSnapshot.Candidate(
                    "black_arcana:test_seal", "black_arcana:test_seal", 8.0D, 200L))));
    }
}
