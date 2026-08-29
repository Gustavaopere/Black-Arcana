package dev.gustavopere.blackarcana.core.ritual;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RitualCompletionLedgerTest {
    private static final ArcanaRitualId RITUAL = ArcanaRitualId.parse("black_arcana:test_completion");

    @Test
    void completionIsIdempotentAndBounded() {
        RitualCompletionLedger ledger = new RitualCompletionLedger(1);
        RitualCompletionKey first = RitualCompletionKey.forCaster(
            RITUAL,
            UUID.fromString("11111111-1111-1111-1111-111111111111"));
        RitualCompletionKey second = RitualCompletionKey.forCaster(
            RITUAL,
            UUID.fromString("22222222-2222-2222-2222-222222222222"));

        assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, ledger.complete(first, 10L));
        assertEquals(RitualCompletionLedger.CompletionResult.ALREADY_COMPLETED, ledger.complete(first, 11L));
        assertEquals(RitualCompletionLedger.CompletionResult.CAPACITY_EXCEEDED, ledger.complete(second, 12L));
        assertEquals(1, ledger.size());
    }

    @Test
    void anchorIdentityIncludesDimensionAndPosition() {
        RitualCompletionKey overworld = RitualCompletionKey.forAnchor(
            RITUAL,
            new RitualAnchor("minecraft:overworld", 42L));
        RitualCompletionKey nether = RitualCompletionKey.forAnchor(
            RITUAL,
            new RitualAnchor("minecraft:the_nether", 42L));

        assertTrue(!overworld.equals(nether));
    }

    @Test
    void restoreRejectsDuplicateKeysWithoutDuplicatingRewardState() {
        RitualCompletionLedger ledger = new RitualCompletionLedger(4);
        RitualCompletionKey key = RitualCompletionKey.forCaster(
            RITUAL,
            UUID.fromString("33333333-3333-3333-3333-333333333333"));

        var result = ledger.restore(List.of(
            new RitualCompletionLedger.SnapshotEntry(key, 20L),
            new RitualCompletionLedger.SnapshotEntry(key, 21L)));

        assertEquals(1, result.restored());
        assertEquals(1, result.rejected());
        assertTrue(ledger.contains(key));
        assertEquals(20L, ledger.snapshot(4).getFirst().completedAtTick());
    }
}
