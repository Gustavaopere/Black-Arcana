package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ArcaneDamageProvenanceTrackerTest {
    @Test
    void trackerUsesIdentityNotEqualsAndIsBounded() {
        ArcaneDamageProvenanceTracker<Object> tracker = new ArcaneDamageProvenanceTracker<>(1);
        Object first = new String("same");
        Object equalButDifferent = new String("same");
        ArcanaDamageProvenance provenance = provenance();

        assertTrue(tracker.register(first, provenance));
        assertEquals(provenance, tracker.find(first).orElseThrow());
        assertTrue(tracker.find(equalButDifferent).isEmpty());
        assertFalse(tracker.register(equalButDifferent, provenance));
        assertEquals(provenance, tracker.release(first).orElseThrow());
        assertTrue(tracker.register(equalButDifferent, provenance));
    }

    private static ArcanaDamageProvenance provenance() {
        return new ArcanaDamageProvenance(
            ArcanaCastId.parse("40000000-0000-0000-0000-000000000001"),
            ArcanaDamageInstanceId.parse("40000000-0000-0000-0000-000000000002"),
            UUID.fromString("40000000-0000-0000-0000-000000000003"),
            ArcanaSpellId.parse("black_arcana:tracker_probe"),
            ArcaneDamageFamily.DIRECT,
            true);
    }
}
