package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneBacklashOffensiveCreditExclusionTest {
    private static final UUID CASTER = UUID.fromString("75000000-0000-0000-0000-000000000001");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("75000000-0000-0000-0000-000000000002");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:offensive_credit_probe");

    @Test
    void backlashCannotBecomeHazardEligibleOffensiveProvenance() {
        assertThrows(IllegalArgumentException.class, () -> provenance(
            "75000000-0000-0000-0000-000000000003",
            ArcaneDamageFamily.ARCANE_BACKLASH,
            true));

        ArcanaDamageProvenance terminal = provenance(
            "75000000-0000-0000-0000-000000000004",
            ArcaneDamageFamily.ARCANE_BACKLASH,
            false);
        assertFalse(terminal.hazardEligible());
        assertEquals(ArcaneDamageFamily.ARCANE_BACKLASH, terminal.family());
    }

    @Test
    void terminalBacklashIsRejectedBeforeClaimAndCannotCreateOffensiveCreditState() {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN,
            1.0D,
            0.0D,
            0.0D,
            200L,
            16);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            10L,
            profile);
        ArcaneHazardSession session = new ArcaneHazardSession(hazard);
        ArcaneBacklashLedger ledger = new ArcaneBacklashLedger(
            session,
            new ArcaneBacklashSnapshot(hazard, zeroResistance(), ArcaneBacklashPolicy.canonical()));

        ArcanaDamageProvenance offensive = provenance(
            "75000000-0000-0000-0000-000000000005",
            ArcaneDamageFamily.DIRECT,
            true);
        var normal = ledger.settle(new ArcaneConfirmedDamage(offensive, 4.0D, 20L));
        assertEquals(4.0D, normal.backlashDamage());
        assertEquals(1, session.seenDamageInstances());
        assertEquals(4.0D, ledger.confirmedEligibleDamage());
        assertEquals(4.0D, ledger.backlashSettled());

        ArcanaDamageProvenance terminal = provenance(
            "75000000-0000-0000-0000-000000000006",
            ArcaneDamageFamily.ARCANE_BACKLASH,
            false);
        var backlash = ledger.settle(new ArcaneConfirmedDamage(terminal, 4.0D, 20L));

        assertEquals("backlash_non_recursive", backlash.code());
        assertEquals(1, session.seenDamageInstances(), "terminal Backlash must be rejected before claiming an offensive damage id");
        assertEquals(4.0D, ledger.confirmedEligibleDamage(), "terminal Backlash must not create eligible offensive damage");
        assertEquals(4.0D, ledger.backlashSettled(), "terminal Backlash must not recursively settle more Backlash");
    }

    @Test
    void provenanceTrackerNeverInfersCreditForUnregisteredTerminalTokens() {
        ArcaneDamageProvenanceTracker<Object> tracker = new ArcaneDamageProvenanceTracker<>(4);
        Object attributedOffense = new Object();
        Object terminalBacklash = new Object();
        ArcanaDamageProvenance offensive = provenance(
            "75000000-0000-0000-0000-000000000007",
            ArcaneDamageFamily.DIRECT,
            true);

        assertTrue(tracker.register(attributedOffense, offensive));
        assertEquals(offensive, tracker.find(attributedOffense).orElseThrow());
        assertTrue(tracker.find(terminalBacklash).isEmpty(), "unregistered terminal damage must remain unattributed");
        assertEquals(1, tracker.size());
    }

    private static ArcanaDamageProvenance provenance(String id, ArcaneDamageFamily family, boolean eligible) {
        return new ArcanaDamageProvenance(
            CAST,
            ArcanaDamageInstanceId.parse(id),
            CASTER,
            SPELL,
            family,
            eligible);
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> byCategory = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            byCategory.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
            0.0D,
            1.0D,
            100.0D,
            1_000.0D,
            List.of(),
            byCategory,
            List.of());
    }
}
