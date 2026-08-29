package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class PendingBacklashContextTest {
    private static final UUID PLAYER = UUID.fromString("61000000-0000-0000-0000-000000000001");
    private static final ArcanaDamageInstanceId DAMAGE_A = new ArcanaDamageInstanceId(
        UUID.fromString("61000000-0000-0000-0000-000000000011"));
    private static final ArcanaDamageInstanceId DAMAGE_B = new ArcanaDamageInstanceId(
        UUID.fromString("61000000-0000-0000-0000-000000000012"));

    @Test
    void contextualDebtsRemainDistinctAndDrainInInsertionOrder() {
        PendingBacklashRegistry registry = new PendingBacklashRegistry(4, 100.0D);
        PendingBacklashDebt first = contextual(12.0D, DAMAGE_A, "veil_a");
        PendingBacklashDebt second = contextual(7.5D, DAMAGE_B, "veil_b");

        assertTrue(registry.accrue(PLAYER, first));
        assertTrue(registry.accrue(PLAYER, second));
        assertEquals(19.5D, registry.pending(PLAYER), 0.0D);

        List<PendingBacklashDebt> drained = registry.drainDebts(PLAYER);
        assertEquals(List.of(first, second), drained);
        assertEquals(0.0D, registry.pending(PLAYER), 0.0D);
        assertTrue(registry.drainDebts(PLAYER).isEmpty());
    }

    @Test
    void legacyNumericDebtNeverInventsEmergencyContext() {
        PendingBacklashRegistry registry = new PendingBacklashRegistry(4, 100.0D);
        assertTrue(registry.accrue(PLAYER, 9.0D));

        PendingBacklashDebt debt = assertSingle(registry.drainDebts(PLAYER));
        assertEquals(9.0D, debt.amount(), 0.0D);
        assertTrue(debt.damageInstanceId().isEmpty());
        assertFalse(debt.protectionAllowed());
        assertTrue(debt.emergencyProtectionSnapshot().candidates().isEmpty());
    }

    @Test
    void contextualPersistenceRoundTripPreservesFrozenIdentityAndSnapshot() {
        PendingBacklashRegistry source = new PendingBacklashRegistry(4, 100.0D);
        PendingBacklashDebt debt = contextual(20.0D, DAMAGE_A, "sealed_hood");
        assertTrue(source.accrue(PLAYER, debt));

        Map<UUID, List<PendingBacklashDebt>> snapshot = source.persistentDebtsSnapshot();
        PendingBacklashRegistry restored = new PendingBacklashRegistry(4, 100.0D);
        restored.restoreDebtsSnapshot(snapshot);

        assertEquals(List.of(debt), restored.drainDebts(PLAYER));
        assertThrows(UnsupportedOperationException.class,
            () -> snapshot.put(UUID.randomUUID(), List.of(PendingBacklashDebt.legacy(1.0D))));
    }

    @Test
    void debtCountAndAmountAreBothBoundedWithoutAggregatingDifferentContexts() {
        PendingBacklashRegistry registry = new PendingBacklashRegistry(1, 10.0D);
        assertTrue(registry.accrue(PLAYER, contextual(6.0D, DAMAGE_A, "veil_a")));
        assertFalse(registry.accrue(PLAYER, contextual(8.0D, DAMAGE_B, "veil_b")));

        List<PendingBacklashDebt> debts = registry.drainDebts(PLAYER);
        assertEquals(2, debts.size());
        assertEquals(6.0D, debts.get(0).amount(), 0.0D);
        assertEquals(4.0D, debts.get(1).amount(), 0.0D);
        assertEquals(DAMAGE_A, debts.get(0).damageInstanceId().orElseThrow());
        assertEquals(DAMAGE_B, debts.get(1).damageInstanceId().orElseThrow());
    }

    private static PendingBacklashDebt contextual(
        double amount,
        ArcanaDamageInstanceId damageInstanceId,
        String resourceId
    ) {
        ArcaneEmergencyProtectionSnapshot frozen = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(resourceId, resourceId, 5.0D, 40L)));
        return PendingBacklashDebt.contextual(amount, damageInstanceId, true, frozen);
    }

    private static <T> T assertSingle(List<T> values) {
        assertEquals(1, values.size());
        return values.getFirst();
    }
}
