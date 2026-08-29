package dev.gustavopere.blackarcana.content.projection;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProjectionBudgetTrackerTest {
    @Test
    void activeEchoesCannotExceedConfiguredOrHardVolleyBudget() {
        ProjectionBudgetTracker tracker = new ProjectionBudgetTracker(12);
        UUID owner = UUID.randomUUID();
        assertTrue(tracker.tryAcquireEchoes(owner, 8));
        assertFalse(tracker.tryAcquireEchoes(owner, 5));
        tracker.releaseEchoes(owner, 4);
        assertTrue(tracker.tryAcquireEchoes(owner, 5));
        assertEquals(9, tracker.activeEchoes(owner));
        assertThrows(IllegalArgumentException.class, () -> ProjectionBudgetTracker.validateVolleySize(65));
    }
}
