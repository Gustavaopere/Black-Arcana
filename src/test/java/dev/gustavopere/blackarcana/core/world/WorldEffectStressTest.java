package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.core.runtime.BoundedWorkScheduler;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WorldEffectStressTest {
    @Test
    void maximumLoadedChunkSetIsBounded() {
        LoadedChunkGuard guard = new LoadedChunkGuard(64, chunk -> true);
        List<ChunkRef> chunks = new ArrayList<>();
        for (int i = 0; i < 64; i++) {
            chunks.add(new ChunkRef("minecraft:overworld", i, 0));
        }
        assertTrue(guard.authorize(chunks).allowed());

        chunks.add(new ChunkRef("minecraft:overworld", 64, 0));
        assertFalse(guard.authorize(chunks).allowed());
        assertEquals("world_chunk_budget", guard.authorize(chunks).code());
    }

    @Test
    void cumulativeCastWorkStopsExactlyAtConfiguredHardBudget() {
        WorldEffectBudgetLedger ledger = new WorldEffectBudgetLedger(8, 4096, 200L);
        ArcanaCastId castId = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");

        for (int i = 0; i < 64; i++) {
            assertTrue(ledger.tryConsume(castId, 64, i).allowed());
        }
        assertEquals(4096, ledger.usedUnits(castId));
        var denied = ledger.tryConsume(castId, 1, 64L);
        assertFalse(denied.allowed());
        assertEquals("world_budget_exhausted", denied.code());
        assertEquals(4096, ledger.usedUnits(castId));
    }

    @Test
    void worstCaseQueueNeverProcessesMoreThanPerTickBudget() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(2048, 128);
        for (int i = 0; i < 2048; i++) {
            assertTrue(scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.complete(1)));
        }
        assertFalse(scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.complete(1)));

        BoundedWorkScheduler.TickResult first = scheduler.tick();
        assertEquals(128, first.consumedUnits());
        assertEquals(128, first.completedItems());
        assertEquals(1920, first.queuedItems());

        BoundedWorkScheduler.TickResult second = scheduler.tick();
        assertEquals(128, second.consumedUnits());
        assertEquals(1792, second.queuedItems());
    }
}
