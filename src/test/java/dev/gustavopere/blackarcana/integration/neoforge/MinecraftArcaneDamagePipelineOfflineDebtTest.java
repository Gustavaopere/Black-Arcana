package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneBacklashProtectionAttemptTracker;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashDebt;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftArcaneDamagePipelineOfflineDebtTest {
    private static final ArcanaCastId CAST = ArcanaCastId.parse("62000000-0000-0000-0000-000000000001");
    private static final ArcanaDamageInstanceId DAMAGE = new ArcanaDamageInstanceId(
        UUID.fromString("62000000-0000-0000-0000-000000000002"));
    private static final UUID CASTER = UUID.fromString("62000000-0000-0000-0000-000000000003");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:offline_debt_probe");

    @Test
    void contextualOfflineDebtRecreatesOnlyItsFrozenProtectionAttempt() {
        ArcaneEmergencyProtectionSnapshot frozen = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:frozen_seal", "black_arcana:frozen_seal", 6.0D, 120L)));
        ArcaneBacklashProtectionAttemptTracker.Attempt original =
            new ArcaneBacklashProtectionAttemptTracker.Attempt(CAST, DAMAGE, CASTER, true, frozen);
        ArcanaDamageProvenance provenance = provenance();

        PendingBacklashDebt debt = MinecraftArcaneDamagePipeline.pendingDebt(
            provenance, 13.0D, Optional.of(original));
        var restored = MinecraftArcaneDamagePipeline.protectionAttempt(CASTER, debt).orElseThrow();

        assertEquals(13.0D, debt.amount(), 0.0D);
        assertEquals(CAST, debt.rootCastId().orElseThrow());
        assertEquals(DAMAGE, debt.damageInstanceId().orElseThrow());
        assertEquals(original, restored);
    }

    @Test
    void missingLiveSessionStillKeepsCausalIdentityButCannotInventProtection() {
        PendingBacklashDebt debt = MinecraftArcaneDamagePipeline.pendingDebt(
            provenance(), 9.0D, Optional.empty());
        var restored = MinecraftArcaneDamagePipeline.protectionAttempt(CASTER, debt).orElseThrow();

        assertTrue(debt.hasCausalContext());
        assertFalse(debt.protectionAllowed());
        assertTrue(debt.emergencyProtectionSnapshot().candidates().isEmpty());
        assertEquals(CAST, restored.rootCastId());
        assertEquals(DAMAGE, restored.damageInstanceId());
        assertFalse(restored.protectionAllowed());
        assertTrue(restored.emergencyProtectionSnapshot().candidates().isEmpty());
    }

    @Test
    void legacySavedDebtCanNeverBecomeAnEmergencyProtectionAttempt() {
        PendingBacklashDebt legacy = PendingBacklashDebt.legacy(4.0D);

        assertTrue(MinecraftArcaneDamagePipeline.protectionAttempt(CASTER, legacy).isEmpty());
    }

    @Test
    void mismatchedAttemptFailsClosedInsteadOfBorrowingAnotherFrozenSnapshot() {
        ArcaneEmergencyProtectionSnapshot foreignSnapshot = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:foreign_seal", "black_arcana:foreign_seal", 20.0D, 400L)));
        ArcaneBacklashProtectionAttemptTracker.Attempt foreign =
            new ArcaneBacklashProtectionAttemptTracker.Attempt(
                ArcanaCastId.parse("62000000-0000-0000-0000-000000000099"),
                DAMAGE,
                CASTER,
                true,
                foreignSnapshot);

        PendingBacklashDebt debt = MinecraftArcaneDamagePipeline.pendingDebt(
            provenance(), 7.0D, Optional.of(foreign));

        assertEquals(CAST, debt.rootCastId().orElseThrow());
        assertEquals(DAMAGE, debt.damageInstanceId().orElseThrow());
        assertFalse(debt.protectionAllowed());
        assertTrue(debt.emergencyProtectionSnapshot().candidates().isEmpty());
    }

    private static ArcanaDamageProvenance provenance() {
        return new ArcanaDamageProvenance(
            CAST,
            DAMAGE,
            CASTER,
            SPELL,
            ArcaneDamageFamily.DIRECT,
            true);
    }
}
