package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WorldEffectBudgetLedgerTest {
    @Test
    void totalPerCastCannotGrowPastBound() {
        var ledger = new WorldEffectBudgetLedger(4, 10, 100);
        var cast = new ArcanaCastId(UUID.randomUUID());

        assertTrue(ledger.tryConsume(cast, 6, 1).allowed());
        assertTrue(ledger.tryConsume(cast, 4, 2).allowed());
        assertFalse(ledger.tryConsume(cast, 1, 3).allowed());
        assertEquals(10, ledger.usedUnits(cast));
    }

    @Test
    void activeCastCardinalityIsBoundedAndIdleEntriesExpire() {
        var ledger = new WorldEffectBudgetLedger(1, 10, 5);
        var first = new ArcanaCastId(UUID.randomUUID());
        var second = new ArcanaCastId(UUID.randomUUID());

        assertTrue(ledger.tryConsume(first, 1, 0).allowed());
        assertFalse(ledger.tryConsume(second, 1, 1).allowed());
        assertEquals(1, ledger.pruneIdle(6));
        assertTrue(ledger.tryConsume(second, 1, 6).allowed());
    }
}
