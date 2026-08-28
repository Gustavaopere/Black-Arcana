package dev.gustavopere.blackarcana.content.cinder;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class BlackPyreFrontierSchedulerTest {
    @Test void frontierIsBoundedDeduplicatedAndNeverNeedsUnloadedCells() {
        BlackPyreFrontierScheduler scheduler = new BlackPyreFrontierScheduler(1, 4, 2);
        UUID id = UUID.randomUUID();
        BlackPyreCell seed = new BlackPyreCell("minecraft:overworld", 0, 64, 0);
        assertTrue(scheduler.start(id, seed));
        assertFalse(scheduler.start(UUID.randomUUID(), seed));
        assertEquals(2, scheduler.offer(id, List.of(
            seed,
            new BlackPyreCell("minecraft:overworld", 1, 64, 0),
            new BlackPyreCell("minecraft:overworld", 2, 64, 0))));
        assertEquals(3, scheduler.seenCells(id));
        var first = scheduler.tick(id, cell -> cell.x() != 1);
        assertEquals(List.of(seed), first);
        var second = scheduler.tick(id, cell -> true);
        assertEquals(1, second.size());
        assertEquals(2, second.getFirst().x());
    }

    @Test void hardCeilingsCannotBeConfiguredPastSafetyBounds() {
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(9, 4, 2));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 257, 2));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 4, 17));
    }
}
