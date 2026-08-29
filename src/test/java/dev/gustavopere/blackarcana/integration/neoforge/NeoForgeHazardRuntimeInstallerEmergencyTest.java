package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardRuntime;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NeoForgeHazardRuntimeInstallerEmergencyTest {
    @Test
    void installerActivatorForwardsFrozenEmergencySnapshotWithoutDroppingIt() {
        ArcanaCastId castId = ArcanaCastId.parse("22222222-3333-4444-5555-666666666666");
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            castId,
            ArcanaSpellId.parse("black_arcana:installer_emergency_probe"),
            UUID.fromString("bbbbbbbb-cccc-dddd-eeee-ffffffffffff"),
            "minecraft:overworld",
            100L,
            new ArcaneDangerProfile(
                ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16, 0.0D, 0.0D, true));
        ArcaneEmergencyProtectionSnapshot emergency = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:test_seal", "black_arcana:test_seal", 6.0D, 120L)));
        AtomicReference<ArcaneEmergencyProtectionSnapshot> forwarded = new AtomicReference<>();

        var activator = NeoForgeHazardRuntimeInstaller.createActivator(
            (snapshot, resistance, policy, emergencySnapshot) -> {
                forwarded.set(emergencySnapshot);
                return ArcaneHazardRuntime.ActivationResult.success(true);
            },
            ignored -> true);

        var result = activator.activate(
            hazard,
            zeroResistance(),
            ArcaneBacklashPolicy.canonical(),
            emergency);

        assertTrue(result.activated());
        assertEquals(emergency, forwarded.get());
        assertTrue(activator.close(castId));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        EnumMap<ArcaneResistanceSourceCategory, Double> byCategory =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            byCategory.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
            0.0D,
            1.0D,
            40.0D,
            240.0D,
            List.of(),
            byCategory,
            List.of());
    }
}
