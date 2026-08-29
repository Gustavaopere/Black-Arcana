package dev.gustavopere.blackarcana.content.blood;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class LawOfRecurrenceTrackerTest {
    @Test
    void repeatedFamilyBuildsBoundedResistanceAndSwitchBuildsVulnerability() {
        var tracker = new LawOfRecurrenceTracker(8,
            new LawOfRecurrenceTracker.Policy(0.10D, 0.40D, 0.15D, 0.60D, 8, 4, 100L));
        UUID caster = UUID.randomUUID();

        var first = tracker.observe(caster, "minecraft:fire", 1L);
        var second = tracker.observe(caster, "minecraft:fire", 2L);
        var switched = tracker.observe(caster, "minecraft:magic", 3L);

        assertEquals(0.10D, first.resistance(), 1.0E-9);
        assertEquals(0.20D, second.resistance(), 1.0E-9);
        assertEquals(0.10D, switched.resistance(), 1.0E-9);
        assertEquals(0.15D, switched.vulnerability(), 1.0E-9);
    }

    @Test
    void resistanceCanNeverReachFullImmunity() {
        assertThrows(IllegalArgumentException.class, () -> new LawOfRecurrenceTracker.Policy(
            0.25D, 1.0D, 0.1D, 0.5D, 8, 4, 100L));
    }
}
