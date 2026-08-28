package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
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

        // Registering nothing in the corruption registry must stay zero regardless of the separate Arcane registry.
        assertEquals(0, arcane.size());
        assertEquals(0.0D, corruption.snapshot(query()).effectiveResistance(), 1.0E-9D);

        corruption.register(new CorruptionResistanceProvider() {
            @Override public String providerId() { return "black_arcana:corruption_only"; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return List.of(new CorruptionResistanceContribution(
                    "black_arcana:test",
                    CorruptionResistanceSourceCategory.RPG,
                    75.0D));
            }
        });
        assertEquals(75.0D, corruption.snapshot(query()).effectiveResistance(), 1.0E-9D);
        assertEquals(0, arcane.size());
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
