package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

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
}
