package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneResistanceNumericHardeningTest {
    private static final UUID CASTER = UUID.fromString("73000000-0000-0000-0000-000000000001");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("73000000-0000-0000-0000-000000000002");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:resistance_numeric_probe");

    @Test
    void curvesAndContributionBoundariesHandleExtremeFiniteAndNonFiniteInputs() {
        ArcaneResistanceCurve arcane = ArcaneResistanceCurve.canonical();
        assertEquals(1.0D, arcane.residualMultiplier(0.0D), 0.0D);
        assertEquals(
            arcane.residualMultiplier(ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE),
            arcane.residualMultiplier(Double.MAX_VALUE),
            0.0D);
        assertThrows(IllegalArgumentException.class, () -> arcane.residualMultiplier(Double.NEGATIVE_INFINITY));

        assertEquals(
            ArcaneResistanceContribution.ABSOLUTE_MAX_AMOUNT,
            new ArcaneResistanceContribution(
                "black_arcana:max_arcane",
                ArcaneResistanceSourceCategory.EXTERNAL,
                ArcaneResistanceContribution.ABSOLUTE_MAX_AMOUNT).amount(),
            0.0D);
        assertThrows(IllegalArgumentException.class, () -> arcaneContribution(Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> arcaneContribution(Double.POSITIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> arcaneContribution(Double.NEGATIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> arcaneContribution(-0.01D));
        assertThrows(IllegalArgumentException.class, () -> arcaneContribution(
            Math.nextUp(ArcaneResistanceContribution.ABSOLUTE_MAX_AMOUNT)));

        CorruptionResistanceCurve corruption = CorruptionResistanceCurve.canonical();
        assertEquals(1.0D, corruption.residualMultiplier(0.0D), 0.0D);
        assertEquals(
            corruption.residualMultiplier(CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE),
            corruption.residualMultiplier(Double.MAX_VALUE),
            0.0D);
        assertThrows(IllegalArgumentException.class, () -> corruption.residualMultiplier(Double.NEGATIVE_INFINITY));

        assertEquals(
            CorruptionResistanceContribution.ABSOLUTE_MAX_AMOUNT,
            new CorruptionResistanceContribution(
                "black_arcana:max_corruption",
                CorruptionResistanceSourceCategory.EXTERNAL,
                CorruptionResistanceContribution.ABSOLUTE_MAX_AMOUNT).amount(),
            0.0D);
        assertThrows(IllegalArgumentException.class, () -> corruptionContribution(Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> corruptionContribution(Double.POSITIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> corruptionContribution(Double.NEGATIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> corruptionContribution(-0.01D));
        assertThrows(IllegalArgumentException.class, () -> corruptionContribution(
            Math.nextUp(CorruptionResistanceContribution.ABSOLUTE_MAX_AMOUNT)));
    }

    @Test
    void nullProviderPayloadsFailClosedWithoutPoisoningValidContributions() {
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(8);
        arcane.register(new ArcaneResistanceProvider() {
            @Override public String providerId() { return "black_arcana:null_arcane"; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return null;
            }
        });
        arcane.register(new ArcaneResistanceProvider() {
            @Override public String providerId() { return "black_arcana:mixed_arcane"; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return Arrays.asList(
                    null,
                    new ArcaneResistanceContribution(
                        "black_arcana:valid_arcane",
                        ArcaneResistanceSourceCategory.EXTERNAL,
                        40.0D));
            }
        });

        var arcaneSnapshot = arcane.snapshot(arcaneQuery());
        assertEquals(40.0D, arcaneSnapshot.effectiveResistance(), 0.0D);
        assertEquals(0.5D, arcaneSnapshot.residualBacklashMultiplier(), 1.0E-12D);
        assertEquals(2, arcaneSnapshot.diagnostics().size());
        assertTrue(arcaneSnapshot.diagnostics().stream().anyMatch(message -> message.contains("null_arcane")));
        assertTrue(arcaneSnapshot.diagnostics().stream().anyMatch(message -> message.contains("null contribution")));

        CorruptionResistanceProviderRegistry corruption = CorruptionResistanceProviderRegistry.canonical(8);
        corruption.register(new CorruptionResistanceProvider() {
            @Override public String providerId() { return "black_arcana:null_corruption"; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return null;
            }
        });
        corruption.register(new CorruptionResistanceProvider() {
            @Override public String providerId() { return "black_arcana:mixed_corruption"; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return Arrays.asList(
                    null,
                    new CorruptionResistanceContribution(
                        "black_arcana:valid_corruption",
                        CorruptionResistanceSourceCategory.EXTERNAL,
                        60.0D));
            }
        });

        var corruptionSnapshot = corruption.snapshot(corruptionQuery());
        assertEquals(60.0D, corruptionSnapshot.effectiveResistance(), 0.0D);
        assertEquals(0.5D, corruptionSnapshot.baselineResidualMultiplier(), 1.0E-12D);
        assertEquals(2, corruptionSnapshot.diagnostics().size());
        assertTrue(corruptionSnapshot.diagnostics().stream().anyMatch(message -> message.contains("null_corruption")));
        assertTrue(corruptionSnapshot.diagnostics().stream().anyMatch(message -> message.contains("null contribution")));
    }

    @Test
    void canonicalRegistriesClampMaximumFiniteContributionsBeforeCurveEvaluation() {
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(8);
        arcane.register(arcaneProvider(
            "black_arcana:max_arcane_provider",
            "black_arcana:max_arcane_source",
            ArcaneResistanceSourceCategory.EXTERNAL,
            ArcaneResistanceContribution.ABSOLUTE_MAX_AMOUNT));

        var arcaneSnapshot = arcane.snapshot(arcaneQuery());
        assertEquals(ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE, arcaneSnapshot.effectiveResistance(), 0.0D);
        assertEquals(
            ArcaneResistanceCurve.canonical().residualMultiplier(ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE),
            arcaneSnapshot.residualBacklashMultiplier(),
            0.0D);

        CorruptionResistanceProviderRegistry corruption = CorruptionResistanceProviderRegistry.canonical(8);
        corruption.register(corruptionProvider(
            "black_arcana:max_corruption_provider",
            "black_arcana:max_corruption_source",
            CorruptionResistanceSourceCategory.EXTERNAL,
            CorruptionResistanceContribution.ABSOLUTE_MAX_AMOUNT));

        var corruptionSnapshot = corruption.snapshot(corruptionQuery());
        assertEquals(CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE, corruptionSnapshot.effectiveResistance(), 0.0D);
        assertEquals(
            CorruptionResistanceCurve.canonical().residualMultiplier(CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE),
            corruptionSnapshot.baselineResidualMultiplier(),
            0.0D);
    }

    @Test
    void canonicalZeroResistanceSnapshotProducesExactOneToOneBacklash() {
        ArcaneResistanceSnapshot zeroResistance = ArcaneResistanceProviderRegistry.canonical(8).snapshot(arcaneQuery());
        ArcaneBacklashLedger ledger = ledger(zeroResistance);

        ArcaneBacklashSettlement settlement = ledger.settle(confirmedDamage(7.5D));

        assertEquals(1.0D, zeroResistance.residualBacklashMultiplier(), 0.0D);
        assertEquals(ArcaneBacklashSettlement.Status.SETTLED, settlement.status());
        assertEquals(7.5D, settlement.deltaEligibleDamage(), 0.0D);
        assertEquals(7.5D, settlement.backlashDamage(), 0.0D);
    }

    @Test
    void canonicalResistanceCapFlowsIntoBacklashWithoutUnderflow() {
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        registry.register(arcaneProvider(
            "black_arcana:capped_backlash",
            "black_arcana:capped_backlash",
            ArcaneResistanceSourceCategory.EXTERNAL,
            ArcaneResistanceContribution.ABSOLUTE_MAX_AMOUNT));
        ArcaneResistanceSnapshot capped = registry.snapshot(arcaneQuery());
        ArcaneBacklashLedger ledger = ledger(capped);

        ArcaneBacklashSettlement settlement = ledger.settle(confirmedDamage(70.0D));

        assertEquals(ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE, capped.effectiveResistance(), 0.0D);
        assertEquals(1.0D / 7.0D, capped.residualBacklashMultiplier(), 1.0E-12D);
        assertEquals(10.0D, settlement.backlashDamage(), 1.0E-12D);
    }

    private static ArcaneResistanceContribution arcaneContribution(double amount) {
        return new ArcaneResistanceContribution(
            "black_arcana:arcane_boundary",
            ArcaneResistanceSourceCategory.EXTERNAL,
            amount);
    }

    private static CorruptionResistanceContribution corruptionContribution(double amount) {
        return new CorruptionResistanceContribution(
            "black_arcana:corruption_boundary",
            CorruptionResistanceSourceCategory.EXTERNAL,
            amount);
    }

    private static ArcaneResistanceProvider arcaneProvider(
        String providerId,
        String sourceId,
        ArcaneResistanceSourceCategory category,
        double amount
    ) {
        return new ArcaneResistanceProvider() {
            @Override public String providerId() { return providerId; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return List.of(new ArcaneResistanceContribution(sourceId, category, amount));
            }
        };
    }

    private static CorruptionResistanceProvider corruptionProvider(
        String providerId,
        String sourceId,
        CorruptionResistanceSourceCategory category,
        double amount
    ) {
        return new CorruptionResistanceProvider() {
            @Override public String providerId() { return providerId; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return List.of(new CorruptionResistanceContribution(sourceId, category, amount));
            }
        };
    }

    private static ArcaneBacklashLedger ledger(ArcaneResistanceSnapshot resistance) {
        ArcaneDangerProfile profile = forbiddenProfile();
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            10L,
            profile);
        return new ArcaneBacklashLedger(
            new ArcaneHazardSession(hazard),
            new ArcaneBacklashSnapshot(hazard, resistance, ArcaneBacklashPolicy.canonical()));
    }

    private static ArcaneConfirmedDamage confirmedDamage(double amount) {
        ArcanaDamageProvenance provenance = new ArcanaDamageProvenance(
            CAST,
            ArcanaDamageInstanceId.parse("73000000-0000-0000-0000-000000000003"),
            CASTER,
            SPELL,
            ArcaneDamageFamily.DIRECT,
            true);
        return new ArcaneConfirmedDamage(provenance, amount, 20L);
    }

    private static ArcaneResistanceQuery arcaneQuery() {
        return new ArcaneResistanceQuery(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            10L,
            forbiddenProfile());
    }

    private static CorruptionResistanceQuery corruptionQuery() {
        return new CorruptionResistanceQuery(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            10L,
            forbiddenProfile());
    }

    private static ArcaneDangerProfile forbiddenProfile() {
        return new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN,
            1.0D,
            0.5D,
            0.5D,
            200L,
            32);
    }
}
