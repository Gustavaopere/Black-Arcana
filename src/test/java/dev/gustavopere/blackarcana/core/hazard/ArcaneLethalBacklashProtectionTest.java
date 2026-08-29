package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneLethalBacklashProtectionTest {
    private static final UUID CASTER = UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");

    @Test
    void armorReducedDamageThatIsCoveredByHealthAndAbsorptionDoesNotConsumeEmergencyResource() {
        ArcaneEmergencyProtectionStateService state = ArcaneEmergencyProtectionStateService.canonical(16);
        ArcaneEmergencyProtectionSnapshot frozen = snapshot(8.0D, 200L);
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of());

        var result = ArcaneLethalBacklashProtection.resolve(
            CASTER,
            ArcanaDamageInstanceId.random(),
            12.0D,
            10.0D,
            5.0D,
            true,
            frozen,
            state,
            100L,
            coordinator);

        assertFalse(result.consumed());
        assertEquals(12.0D, result.remainingDamage());
        assertEquals("not_lethal", result.code());
        assertEquals(0L, state.readyAtTick(CASTER, "black_arcana:test_seal"));
    }

    @Test
    void lethalFinalDamageConsumesFrozenCandidateAndStartsCooldownExactlyOnce() {
        ArcaneEmergencyProtectionStateService state = ArcaneEmergencyProtectionStateService.canonical(16);
        ArcaneEmergencyProtectionSnapshot frozen = snapshot(8.0D, 200L);
        ArcaneEmergencyProtectionCoordinator coordinator = new ArcaneEmergencyProtectionCoordinator(List.of());
        ArcanaDamageInstanceId damageId = ArcanaDamageInstanceId.random();

        var result = ArcaneLethalBacklashProtection.resolve(
            CASTER,
            damageId,
            20.0D,
            10.0D,
            5.0D,
            true,
            frozen,
            state,
            100L,
            coordinator);

        assertTrue(result.consumed());
        assertEquals(12.0D, result.remainingDamage());
        assertEquals(8.0D, result.absorbed());
        assertEquals("black_arcana:test_seal", result.code());
        assertEquals(300L, state.readyAtTick(CASTER, "black_arcana:test_seal"));

        var duplicate = ArcaneLethalBacklashProtection.resolve(
            CASTER,
            damageId,
            20.0D,
            10.0D,
            5.0D,
            true,
            frozen,
            state,
            100L,
            coordinator);
        assertFalse(duplicate.consumed());
        assertEquals(20.0D, duplicate.remainingDamage());
        assertEquals("already_processed", duplicate.code());
        assertEquals(300L, state.readyAtTick(CASTER, "black_arcana:test_seal"));
    }

    @Test
    void profileThatDisallowsEmergencyProtectionNeverConsumesCandidate() {
        ArcaneEmergencyProtectionStateService state = ArcaneEmergencyProtectionStateService.canonical(16);

        var result = ArcaneLethalBacklashProtection.resolve(
            CASTER,
            ArcanaDamageInstanceId.random(),
            20.0D,
            10.0D,
            0.0D,
            false,
            snapshot(20.0D, 200L),
            state,
            100L,
            new ArcaneEmergencyProtectionCoordinator(List.of()));

        assertFalse(result.consumed());
        assertEquals(20.0D, result.remainingDamage());
        assertEquals("protection_unavailable", result.code());
        assertEquals(0L, state.readyAtTick(CASTER, "black_arcana:test_seal"));
    }

    private static ArcaneEmergencyProtectionSnapshot snapshot(double absorption, long cooldownTicks) {
        return new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:test_seal",
                "black_arcana:test_seal",
                absorption,
                cooldownTicks)));
    }
}
