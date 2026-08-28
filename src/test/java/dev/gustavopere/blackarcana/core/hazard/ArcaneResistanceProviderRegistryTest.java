package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneResistanceProviderRegistryTest {
    @Test
    void providerOrderingCannotChangeSnapshotTotalsOrBreakdown() {
        ArcaneResistanceProvider a = provider("armor", "robe", ArcaneResistanceSourceCategory.EQUIPMENT, 60.0D);
        ArcaneResistanceProvider b = provider("rpg", "mastery", ArcaneResistanceSourceCategory.RPG, 40.0D);

        ArcaneResistanceProviderRegistry first = ArcaneResistanceProviderRegistry.canonical(8);
        first.register(a);
        first.register(b);
        ArcaneResistanceProviderRegistry second = ArcaneResistanceProviderRegistry.canonical(8);
        second.register(b);
        second.register(a);

        var firstSnapshot = first.snapshot(query());
        var secondSnapshot = second.snapshot(query());
        assertEquals(100.0D, firstSnapshot.effectiveResistance(), 1.0E-12D);
        assertEquals(firstSnapshot.effectiveResistance(), secondSnapshot.effectiveResistance(), 0.0D);
        assertEquals(firstSnapshot.residualBacklashMultiplier(), secondSnapshot.residualBacklashMultiplier(), 0.0D);
        assertEquals(firstSnapshot.contributions(), secondSnapshot.contributions());
    }

    @Test
    void bucketAndGlobalCapsPreventAbsurdStacking() {
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        registry.register(provider("armor_a", "robe", ArcaneResistanceSourceCategory.EQUIPMENT, 200.0D));
        registry.register(provider("armor_b", "mask", ArcaneResistanceSourceCategory.EQUIPMENT, 200.0D));
        registry.register(provider("rpg", "mastery", ArcaneResistanceSourceCategory.RPG, 200.0D));

        var snapshot = registry.snapshot(query());
        assertEquals(ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE, snapshot.effectiveResistance(), 0.0D);
        assertEquals(ArcaneResistanceCurve.canonical().residualMultiplier(240.0D), snapshot.residualBacklashMultiplier(), 0.0D);
        assertTrue(snapshot.effectiveByCategory().get(ArcaneResistanceSourceCategory.EQUIPMENT)
            <= ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE);
    }

    @Test
    void failingProviderIsIsolatedAndDiagnosed() {
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        registry.register(provider("good", "robe", ArcaneResistanceSourceCategory.EQUIPMENT, 40.0D));
        registry.register(new ArcaneResistanceProvider() {
            @Override public String providerId() { return "broken"; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                throw new IllegalStateException("synthetic failure");
            }
        });

        var snapshot = registry.snapshot(query());
        assertEquals(40.0D, snapshot.effectiveResistance(), 0.0D);
        assertEquals(1, snapshot.diagnostics().size());
        assertTrue(snapshot.diagnostics().getFirst().contains("broken"));
    }

    @Test
    void snapshotDoesNotChangeAfterProviderStateMutates() {
        AtomicReference<Double> amount = new AtomicReference<>(80.0D);
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        registry.register(new ArcaneResistanceProvider() {
            @Override public String providerId() { return "mutable_test"; }
            @Override public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return List.of(new ArcaneResistanceContribution(
                    "source", ArcaneResistanceSourceCategory.EXTERNAL, amount.get()));
            }
        });

        var first = registry.snapshot(query());
        amount.set(0.0D);
        var second = registry.snapshot(query());

        assertEquals(80.0D, first.effectiveResistance(), 0.0D);
        assertEquals(0.0D, second.effectiveResistance(), 0.0D);
    }

    @Test
    void invalidContributionsAndDuplicateProviderIdsFailAtBoundary() {
        assertThrows(IllegalArgumentException.class, () -> new ArcaneResistanceContribution(
            "bad", ArcaneResistanceSourceCategory.EXTERNAL, Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> new ArcaneResistanceContribution(
            "bad", ArcaneResistanceSourceCategory.EXTERNAL, -1.0D));

        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(2);
        registry.register(provider("same", "a", ArcaneResistanceSourceCategory.NATIVE, 1.0D));
        assertThrows(IllegalArgumentException.class, () ->
            registry.register(provider("same", "b", ArcaneResistanceSourceCategory.NATIVE, 1.0D)));
    }

    private static ArcaneResistanceProvider provider(
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

    private static ArcaneResistanceQuery query() {
        return new ArcaneResistanceQuery(
            ArcanaCastId.parse("99999999-9999-9999-9999-999999999999"),
            ArcanaSpellId.parse("black_arcana:resistance_probe"),
            UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            "minecraft:overworld",
            100L,
            new ArcaneDangerProfile(ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16));
    }
}
