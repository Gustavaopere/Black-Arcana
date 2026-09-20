package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CorruptionResistanceProviderRegistryTest {
    private static final UUID PLAYER = UUID.fromString("11111111-1111-1111-1111-111111111111");

    @Test
    void providerAbsenceContributesZeroAndDoesNotDisableChannel() {
        CorruptionResistanceProviderRegistry registry = CorruptionResistanceProviderRegistry.canonical(8);
        var snapshot = registry.snapshot(query());

        assertEquals(0.0D, snapshot.effectiveResistance(), 1.0E-9D);
        assertEquals(1.0D, snapshot.baselineResidualMultiplier(), 1.0E-9D);
        assertTrue(snapshot.contributions().isEmpty());
    }

    @Test
    void providerFailuresFailClosedToZeroContribution() {
        CorruptionResistanceProviderRegistry registry = CorruptionResistanceProviderRegistry.canonical(8);
        registry.register(new CorruptionResistanceProvider() {
            @Override public String providerId() { return "black_arcana:broken"; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                throw new IllegalStateException("synthetic failure");
            }
        });

        var snapshot = registry.snapshot(query());
        assertEquals(0.0D, snapshot.effectiveResistance(), 1.0E-9D);
        assertEquals(1, snapshot.diagnostics().size());
    }

    @Test
    void corruptionResistanceUsesItsOwnProviderChannel() {
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(8);
        CorruptionResistanceProviderRegistry corruption = CorruptionResistanceProviderRegistry.canonical(8);

        arcane.register(new ArcaneResistanceProvider() {
            @Override public String providerId() { return "black_arcana:arcane_only"; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return List.of(new ArcaneResistanceContribution(
                    "black_arcana:arcane_ward",
                    ArcaneResistanceSourceCategory.EQUIPMENT,
                    240.0D));
            }
        });

        assertEquals(240.0D, arcane.snapshot(arcaneQuery()).effectiveResistance(), 1.0E-9D);
        assertEquals(0.0D, corruption.snapshot(query()).effectiveResistance(), 1.0E-9D);

        corruption.register(provider(
            "black_arcana:corruption_only",
            "black_arcana:corruption_ward",
            CorruptionResistanceSourceCategory.RPG,
            75.0D));

        assertEquals(75.0D, corruption.snapshot(query()).effectiveResistance(), 1.0E-9D);
        assertEquals(240.0D, arcane.snapshot(arcaneQuery()).effectiveResistance(), 1.0E-9D);
    }

    @Test
    void providerOrderingAndGlobalCapAreDeterministic() {
        CorruptionResistanceProvider firstProvider = provider(
            "black_arcana:z_provider",
            "black_arcana:ritual",
            CorruptionResistanceSourceCategory.RITUAL,
            200.0D);
        CorruptionResistanceProvider secondProvider = provider(
            "black_arcana:a_provider",
            "black_arcana:rpg",
            CorruptionResistanceSourceCategory.RPG,
            200.0D);

        CorruptionResistanceProviderRegistry first = CorruptionResistanceProviderRegistry.canonical(8);
        first.register(firstProvider);
        first.register(secondProvider);
        CorruptionResistanceProviderRegistry second = CorruptionResistanceProviderRegistry.canonical(8);
        second.register(secondProvider);
        second.register(firstProvider);

        var firstSnapshot = first.snapshot(query());
        var secondSnapshot = second.snapshot(query());

        assertEquals(CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE, firstSnapshot.effectiveResistance(), 0.0D);
        assertEquals(firstSnapshot.effectiveResistance(), secondSnapshot.effectiveResistance(), 0.0D);
        assertEquals(firstSnapshot.baselineResidualMultiplier(), secondSnapshot.baselineResidualMultiplier(), 0.0D);
        assertEquals(firstSnapshot.contributions(), secondSnapshot.contributions());
    }

    private static CorruptionResistanceProvider provider(
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

    private static ArcaneResistanceQuery arcaneQuery() {
        return new ArcaneResistanceQuery(
            ArcanaCastId.random(),
            ArcanaSpellId.parse("black_arcana:corruption_probe"),
            PLAYER,
            "minecraft:overworld",
            100L,
            ArcaneDangerProfile.normal());
    }

    private static CorruptionResistanceQuery query() {
        return new CorruptionResistanceQuery(
            ArcanaCastId.random(),
            ArcanaSpellId.parse("black_arcana:corruption_probe"),
            PLAYER,
            "minecraft:overworld",
            100L,
            ArcaneDangerProfile.normal());
    }
}
