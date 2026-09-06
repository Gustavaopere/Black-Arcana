package dev.gustavopere.blackarcana.content.cinder;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BlackPyreFrontierSchedulerTest {
    @Test
    void hardCeilingsCannotBeConfiguredPastSafetyBounds() {
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(9, 4, 2, 4, 100));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 257, 2, 4, 100));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 4, 17, 4, 100));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 4, 2, 13, 100));
        assertThrows(IllegalArgumentException.class, () -> new BlackPyreFrontierScheduler(1, 4, 2, 4, 1201));
    }

    @Test
    void frontierCapacityCellCapAndDeduplicationAreBounded() {
        var scheduler = new BlackPyreFrontierScheduler(1, 4, 2, 12, 1200);
        UUID first = UUID.randomUUID();
        var seed = cell(0, 64, 0);
        assertTrue(scheduler.start(first, seed, 100));
        assertFalse(scheduler.start(first, seed, 100));
        assertFalse(scheduler.start(UUID.randomUUID(), seed, 100));

        assertEquals(3, scheduler.offer(first, List.of(
            seed,
            cell(1, 64, 0),
            cell(2, 64, 0),
            cell(3, 64, 0),
            cell(4, 64, 0))));
        assertEquals(4, scheduler.seenCells(first));
    }

    @Test
    void offerRejectsDifferentDimensionAndCellsBeyondOriginRadius() {
        var scheduler = new BlackPyreFrontierScheduler(1, 16, 4, 12, 1200);
        UUID id = UUID.randomUUID();
        assertTrue(scheduler.start(id, cell(0, 64, 0), 0));

        assertEquals(1, scheduler.offer(id, List.of(
            cell(12, 64, 0),
            cell(13, 64, 0),
            new BlackPyreCell("minecraft:the_nether", 1, 64, 0))));
        assertEquals(2, scheduler.seenCells(id));
    }

    @Test
    void tickProcessesAtMostConfiguredWorkAndDropsUnloadedCellsPermanently() {
        var scheduler = new BlackPyreFrontierScheduler(1, 16, 2, 12, 1200);
        UUID id = UUID.randomUUID();
        var seed = cell(0, 64, 0);
        var unloaded = cell(1, 64, 0);
        var loaded = cell(2, 64, 0);
        assertTrue(scheduler.start(id, seed, 0));
        assertEquals(List.of(seed), scheduler.tick(id, 0, ignored -> true));
        assertEquals(2, scheduler.offer(id, List.of(unloaded, loaded)));

        assertEquals(List.of(loaded), scheduler.tick(id, 1, candidate -> !candidate.equals(unloaded)));
        assertEquals(List.of(), scheduler.tick(id, 2, ignored -> true),
            "unloaded candidates must be dropped rather than retained for a later chunk load");
    }

    @Test
    void lifetimeExpiryAndExplicitFinishRemoveFrontierState() {
        var scheduler = new BlackPyreFrontierScheduler(2, 16, 4, 12, 1200);
        UUID expiring = UUID.randomUUID();
        assertTrue(scheduler.start(expiring, cell(0, 64, 0), 100));
        scheduler.tick(expiring, 1299, ignored -> true);
        assertEquals(1, scheduler.activeFrontiers());
        assertEquals(List.of(), scheduler.tick(expiring, 1300, ignored -> true));
        assertEquals(0, scheduler.activeFrontiers());

        UUID explicit = UUID.randomUUID();
        assertTrue(scheduler.start(explicit, cell(0, 64, 0), 2000));
        scheduler.finish(explicit);
        assertEquals(0, scheduler.activeFrontiers());
    }

    @Test
    void maximumLegalFrontiersRemainIndividuallyBoundedUnderStress() {
        var scheduler = new BlackPyreFrontierScheduler(8, 256, 16, 12, 1200);
        List<UUID> ids = new ArrayList<>();
        for (int frontier = 0; frontier < 8; frontier++) {
            UUID id = UUID.randomUUID();
            ids.add(id);
            assertTrue(scheduler.start(id, cell(0, 64, frontier), 0));
            List<BlackPyreCell> candidates = new ArrayList<>();
            for (int x = -12; x <= 12; x++) {
                for (int z = -12; z <= 12 && candidates.size() < 255; z++) {
                    candidates.add(cell(x, 64, z + frontier));
                }
            }
            scheduler.offer(id, candidates);
            assertTrue(scheduler.seenCells(id) <= 256);
            assertTrue(scheduler.tick(id, 1, ignored -> true).size() <= 16);
        }
        assertEquals(8, scheduler.activeFrontiers());
    }

    private static BlackPyreCell cell(int x, int y, int z) {
        return new BlackPyreCell("minecraft:overworld", x, y, z);
    }
}
