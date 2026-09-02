package dev.gustavopere.blackarcana.content.souls;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SoulAnchorLedgerTest {
    private static SoulAnchorLedger ledger() {
        return new SoulAnchorLedger(new SoulAnchorLedger.Policy(2, 10.0D, 100.0D, 600L, 16));
    }

    @Test
    void deathCreditIsWeightedDeduplicatedAndFormsBoundedAnchors() {
        SoulAnchorLedger ledger = ledger();
        UUID owner = UUID.randomUUID();
        UUID event = UUID.randomUUID();
        var credit = new SoulAnchorLedger.DeathCredit(event, 20.0D, 0.5D, true);
        assertEquals(10.0D, ledger.creditDeath(owner, credit).awarded(), 1.0E-9);
        assertFalse(ledger.creditDeath(owner, credit).credited(), "same death event must not credit twice");
        assertTrue(ledger.formAnchor(owner));
        assertFalse(ledger.formAnchor(owner));
        assertEquals(1, ledger.snapshot(owner).anchors());
    }

    @Test
    void oneDeathConsumesAtMostOneAnchorAndStartsRecoveryLockout() {
        SoulAnchorLedger ledger = ledger();
        UUID owner = UUID.randomUUID();
        ledger.creditDeath(owner, new SoulAnchorLedger.DeathCredit(UUID.randomUUID(), 20.0D, 1.0D, true));
        assertTrue(ledger.formAnchor(owner));
        assertTrue(ledger.formAnchor(owner));

        UUID deathEvent = UUID.randomUUID();
        var first = ledger.consumeForDeath(owner, deathEvent, 100L);
        assertTrue(first.consumed());
        assertEquals(1, first.anchorsRemaining());
        assertEquals(SoulAnchorLedger.AnchorConsumeResult.Status.RECOVERY_LOCKED,
            ledger.consumeForDeath(owner, UUID.randomUUID(), 101L).status());
        assertEquals(SoulAnchorLedger.AnchorConsumeResult.Status.DUPLICATE_EVENT,
            ledger.consumeForDeath(owner, deathEvent, first.recoveryUntilTick()).status());
        assertEquals(1, ledger.snapshot(owner).anchors(), "duplicate event must not consume another anchor");
    }

    @Test
    void snapshotRestorePreservesExactAnchorsCreditsAndLockout() {
        SoulAnchorLedger source = ledger();
        UUID owner = UUID.randomUUID();
        source.creditDeath(owner, new SoulAnchorLedger.DeathCredit(UUID.randomUUID(), 15.0D, 1.0D, true));
        source.formAnchor(owner);
        source.consumeForDeath(owner, UUID.randomUUID(), 40L);
        List<SoulAnchorLedger.Snapshot> snapshots = source.snapshotAll();

        SoulAnchorLedger restored = ledger();
        restored.restore(snapshots);
        assertEquals(source.snapshot(owner), restored.snapshot(owner));
    }

    @Test
    void snapshotRestorePreservesDeathTransactionIdempotency() {
        SoulAnchorLedger source = ledger();
        UUID owner = UUID.randomUUID();
        UUID creditedDeathEvent = UUID.randomUUID();
        UUID preventedDeathEvent = UUID.randomUUID();
        var credit = new SoulAnchorLedger.DeathCredit(creditedDeathEvent, 20.0D, 1.0D, true);

        assertTrue(source.creditDeath(owner, credit).credited());
        assertTrue(source.formAnchor(owner));
        assertTrue(source.formAnchor(owner));
        assertTrue(source.consumeForDeath(owner, preventedDeathEvent, 40L).consumed());

        SoulAnchorLedger restored = ledger();
        restored.restore(source.snapshotAll());

        assertFalse(restored.creditDeath(owner, credit).credited(),
            "restart must not allow the same credited death event to mint spirit twice");
        assertEquals(SoulAnchorLedger.AnchorConsumeResult.Status.DUPLICATE_EVENT,
            restored.consumeForDeath(owner, preventedDeathEvent, 1_000L).status(),
            "restart must preserve same-death-event anchor idempotency after lockout expires");
        assertEquals(1, restored.snapshot(owner).anchors(),
            "replayed prevented death must not consume the remaining anchor");
    }

    @Test
    void hardAnchorAndLockoutCeilingsCannotBeRelaxed() {
        assertThrows(IllegalArgumentException.class,
            () -> new SoulAnchorLedger.Policy(6, 10.0D, 100.0D, 600L, 16));
        assertThrows(IllegalArgumentException.class,
            () -> new SoulAnchorLedger.Policy(2, 10.0D, 100.0D, 199L, 16));
    }
}
