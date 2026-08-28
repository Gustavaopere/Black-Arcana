package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneBacklashLedgerTest {
    private static final UUID CASTER = UUID.fromString("b73d98b6-3e35-4747-82b2-d0c648aecc06");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("10000000-0000-0000-0000-000000000001");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:forbidden_probe");

    @Test
    void zeroResistanceCanonicalProfileIsExactOneToOne() {
        ArcaneBacklashLedger ledger = ledger(1.0D, zeroResistance(), ArcaneBacklashPolicy.canonical());
        var result = ledger.settle(damage("20000000-0000-0000-0000-000000000001", ArcaneDamageFamily.DIRECT, 7.5D, true));

        assertEquals(ArcaneBacklashSettlement.Status.SETTLED, result.status());
        assertEquals(7.5D, result.deltaEligibleDamage());
        assertEquals(7.5D, result.backlashDamage());
    }

    @Test
    void resistanceSnapshotIsFrozenAndAppliedExactlyOnce() {
        ArcaneResistanceSnapshot resistance = resistance(0.25D);
        ArcaneBacklashLedger ledger = ledger(1.0D, resistance, ArcaneBacklashPolicy.canonical());

        assertEquals(2.0D, ledger.settle(damage("20000000-0000-0000-0000-000000000002", ArcaneDamageFamily.PROJECTILE, 8.0D, true)).backlashDamage());
        assertEquals(1.0D, ledger.settle(damage("20000000-0000-0000-0000-000000000003", ArcaneDamageFamily.CHAIN, 4.0D, true)).backlashDamage());
        assertEquals(resistance, ledger.snapshot().arcaneResistance());
    }

    @Test
    void duplicateDamageInstanceCannotSettleTwice() {
        ArcaneBacklashLedger ledger = ledger(1.0D, zeroResistance(), ArcaneBacklashPolicy.canonical());
        ArcaneConfirmedDamage damage = damage("20000000-0000-0000-0000-000000000004", ArcaneDamageFamily.DIRECT, 3.0D, true);

        assertEquals(3.0D, ledger.settle(damage).backlashDamage());
        var duplicate = ledger.settle(damage);
        assertEquals(ArcaneBacklashSettlement.Status.DENIED, duplicate.status());
        assertEquals("hazard_claim_duplicate", duplicate.code());
        assertEquals(3.0D, ledger.backlashSettled());
    }

    @Test
    void backlashAndIneligibleDamageAreTerminallyExcluded() {
        ArcaneBacklashLedger ledger = ledger(1.0D, zeroResistance(), ArcaneBacklashPolicy.canonical());

        var backlash = ledger.settle(damage("20000000-0000-0000-0000-000000000005", ArcaneDamageFamily.ARCANE_BACKLASH, 10.0D, false));
        var external = ledger.settle(damage("20000000-0000-0000-0000-000000000006", ArcaneDamageFamily.OTHER, 10.0D, false));

        assertEquals("backlash_non_recursive", backlash.code());
        assertEquals("hazard_ineligible", external.code());
        assertEquals(0.0D, ledger.confirmedEligibleDamage());
    }

    @Test
    void ownedSummonRequiresExplicitOptIn() {
        ArcaneBacklashLedger defaultLedger = ledger(1.0D, zeroResistance(), ArcaneBacklashPolicy.canonical());
        assertEquals("summon_not_opted_in", defaultLedger.settle(
            damage("20000000-0000-0000-0000-000000000007", ArcaneDamageFamily.OWNED_SUMMON, 5.0D, true)).code());

        ArcaneBacklashLedger optedIn = ledger(1.0D, zeroResistance(),
            new ArcaneBacklashPolicy(true, 0.0D, 1_000.0D, 10_000.0D));
        assertEquals(5.0D, optedIn.settle(
            damage("20000000-0000-0000-0000-000000000008", ArcaneDamageFamily.OWNED_SUMMON, 5.0D, true)).backlashDamage());
    }

    @Test
    void totalAndPerSettlementCeilingsAreSaturating() {
        ArcaneBacklashLedger ledger = ledger(16.0D, zeroResistance(),
            new ArcaneBacklashPolicy(false, 0.0D, 20.0D, 10.0D));

        var first = ledger.settle(damage("20000000-0000-0000-0000-000000000009", ArcaneDamageFamily.DIRECT, 8.0D, true));
        var second = ledger.settle(damage("20000000-0000-0000-0000-000000000010", ArcaneDamageFamily.DIRECT, 8.0D, true));

        assertEquals(20.0D, first.backlashDamage());
        assertEquals(2.0D, second.deltaEligibleDamage());
        assertEquals(20.0D, second.backlashDamage());
        assertEquals(10.0D, ledger.confirmedEligibleDamage());
    }

    @Test
    void nonFiniteConfirmedDamageIsRejectedAtBoundary() {
        assertThrows(IllegalArgumentException.class, () -> new ArcaneConfirmedDamage(
            provenance("20000000-0000-0000-0000-000000000011", ArcaneDamageFamily.DIRECT, true),
            Double.NaN,
            10L));
    }

    private static ArcaneBacklashLedger ledger(
        double multiplier,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy policy
    ) {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, multiplier, 0.5D, 0.5D, 200L, 32);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(CAST, SPELL, CASTER, "minecraft:overworld", 10L, profile);
        ArcaneHazardSession session = new ArcaneHazardSession(hazard);
        return new ArcaneBacklashLedger(session, new ArcaneBacklashSnapshot(hazard, resistance, policy));
    }

    private static ArcaneConfirmedDamage damage(String id, ArcaneDamageFamily family, double health, boolean eligible) {
        return new ArcaneConfirmedDamage(provenance(id, family, eligible), health, 20L);
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
        return resistance(1.0D);
    }

    private static ArcaneResistanceSnapshot resistance(double residual) {
        Map<ArcaneResistanceSourceCategory, Double> byCategory = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            byCategory.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
            0.0D,
            residual,
            100.0D,
            1_000.0D,
            List.of(),
            byCategory,
            List.of());
    }
}
