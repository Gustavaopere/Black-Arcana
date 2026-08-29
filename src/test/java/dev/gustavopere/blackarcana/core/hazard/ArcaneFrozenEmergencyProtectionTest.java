package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtection;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneFrozenEmergencyProtectionTest {
    private static final UUID CASTER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");

    @Test
    void frozenCandidateCommitsCooldownWithoutRequeryingEquipment() {
        ArcaneEmergencyProtectionStateService state = ArcaneEmergencyProtectionStateService.canonical(16);
        ArcaneEmergencyProtectionSnapshot snapshot = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:containment_mask",
                "black_arcana:containment_mask",
                8.0D,
                200L)));
        List<ArcaneEmergencyProtection> providers =
            ArcaneFrozenEmergencyProtection.providers(snapshot, state, 100L);
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of());
        ArcanaDamageInstanceId damageId = ArcanaDamageInstanceId.random();

        var result = coordinator.protect(
            new ArcaneEmergencyProtection.Query(CASTER, damageId, 20.0D, 5.0D, true),
            providers);

        assertTrue(result.consumed());
        assertEquals(8.0D, result.absorbed());
        assertEquals(12.0D, result.remainingBacklash());
        assertEquals("black_arcana:containment_mask", result.sourceId());
        assertEquals(300L, state.readyAtTick(CASTER, "black_arcana:containment_mask"));

        var duplicate = coordinator.protect(
            new ArcaneEmergencyProtection.Query(CASTER, damageId, 20.0D, 5.0D, true),
            providers);
        assertFalse(duplicate.consumed());
        assertEquals("already_processed", duplicate.sourceId());
        assertEquals(300L, state.readyAtTick(CASTER, "black_arcana:containment_mask"));
    }

    @Test
    void cooldownCandidateIsSkippedAndNextFrozenCandidateCanProtect() {
        ArcaneEmergencyProtectionStateService state = ArcaneEmergencyProtectionStateService.canonical(16);
        state.reserve(CASTER, "black_arcana:first", 10L, 500L).commit();
        ArcaneEmergencyProtectionSnapshot snapshot = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:first_source", "black_arcana:first", 20.0D, 500L),
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:second_source", "black_arcana:second", 6.0D, 100L)));

        var result = new ArcaneEmergencyProtectionCoordinator(List.of()).protect(
            new ArcaneEmergencyProtection.Query(
                CASTER, ArcanaDamageInstanceId.random(), 15.0D, 0.0D, true),
            ArcaneFrozenEmergencyProtection.providers(snapshot, state, 100L));

        assertTrue(result.consumed());
        assertEquals(6.0D, result.absorbed());
        assertEquals(9.0D, result.remainingBacklash());
        assertEquals("black_arcana:second_source", result.sourceId());
        assertEquals(510L, state.readyAtTick(CASTER, "black_arcana:first"));
        assertEquals(200L, state.readyAtTick(CASTER, "black_arcana:second"));
    }

    @Test
    void emptyFrozenSnapshotAddsNoProviderAndLeavesBacklashUntouched() {
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of());
        var result = coordinator.protect(
            new ArcaneEmergencyProtection.Query(
                CASTER, ArcanaDamageInstanceId.random(), 10.0D, 0.0D, true),
            ArcaneFrozenEmergencyProtection.providers(
                ArcaneEmergencyProtectionSnapshot.empty(),
                ArcaneEmergencyProtectionStateService.canonical(16),
                100L));

        assertFalse(result.consumed());
        assertEquals(10.0D, result.remainingBacklash());
        assertEquals("no_reservation", result.sourceId());
    }
}
