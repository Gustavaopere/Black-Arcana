package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class PendingBacklashRegistryTest {
    @Test
    void debtIsBoundedAndDrainedExactlyOnce() {
        PendingBacklashRegistry registry = new PendingBacklashRegistry(1, 10.0D);
        UUID player = UUID.fromString("60000000-0000-0000-0000-000000000001");

        assertTrue(registry.accrue(player, 4.0D));
        assertFalse(registry.accrue(player, 9.0D));
        assertEquals(10.0D, registry.pending(player));
        assertEquals(10.0D, registry.drain(player));
        assertEquals(0.0D, registry.drain(player));
    }

    @Test
    void newCasterFailsClosedWhenRegistryCapacityIsFull() {
        PendingBacklashRegistry registry = new PendingBacklashRegistry(1, 10.0D);
        UUID first = UUID.fromString("60000000-0000-0000-0000-000000000002");
        UUID second = UUID.fromString("60000000-0000-0000-0000-000000000003");
        assertTrue(registry.accrue(first, 1.0D));
        assertFalse(registry.accrue(second, 1.0D));
        assertEquals(0.0D, registry.pending(second));
    }

    @Test
    void persistenceSnapshotRestoresDebtWithoutDoubleApplication() {
        UUID player = UUID.fromString("60000000-0000-0000-0000-000000000004");
        PendingBacklashRegistry source = new PendingBacklashRegistry(4, 100.0D);
        assertTrue(source.accrue(player, 12.5D));

        Map<UUID, Double> snapshot = source.persistentSnapshot();
        PendingBacklashRegistry restored = new PendingBacklashRegistry(4, 100.0D);
        restored.restoreSnapshot(snapshot);

        assertEquals(12.5D, restored.pending(player), 0.0D);
        assertEquals(12.5D, restored.drain(player), 0.0D);
        assertEquals(0.0D, restored.drain(player), 0.0D);
        assertThrows(UnsupportedOperationException.class,
            () -> snapshot.put(UUID.randomUUID(), 1.0D));
    }

    @Test
    void restoreSnapshotSanitizesMalformedDebtAndHonorsCapacity() {
        UUID invalidFinite = UUID.fromString("60000000-0000-0000-0000-000000000005");
        UUID negative = UUID.fromString("60000000-0000-0000-0000-000000000006");
        UUID oversized = UUID.fromString("60000000-0000-0000-0000-000000000007");
        UUID overflow = UUID.fromString("60000000-0000-0000-0000-000000000008");
        Map<UUID, Double> persisted = new LinkedHashMap<>();
        persisted.put(invalidFinite, Double.POSITIVE_INFINITY);
        persisted.put(negative, -1.0D);
        persisted.put(oversized, 1_000.0D);
        persisted.put(overflow, 5.0D);

        PendingBacklashRegistry restored = new PendingBacklashRegistry(1, 10.0D);
        restored.restoreSnapshot(persisted);

        assertEquals(1, restored.size());
        assertEquals(0.0D, restored.pending(invalidFinite), 0.0D);
        assertEquals(0.0D, restored.pending(negative), 0.0D);
        assertEquals(10.0D, restored.pending(oversized), 0.0D);
        assertEquals(0.0D, restored.pending(overflow), 0.0D);
    }
}
