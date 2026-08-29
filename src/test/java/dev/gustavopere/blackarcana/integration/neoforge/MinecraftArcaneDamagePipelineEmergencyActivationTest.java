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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftArcaneDamagePipelineEmergencyActivationTest {
    @Test
    void pipelineActivationBridgePassesEmergencySnapshotToHazardRuntime() {
        ArcanaCastId castId = ArcanaCastId.parse("f1111111-2222-3333-4444-555555555555");
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            castId,
            ArcanaSpellId.parse("black_arcana:pipeline_emergency_probe"),
            UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
            "minecraft:overworld",
            100L,
            new ArcaneDangerProfile(
                ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16, 0.0D, 0.0D, true));
        ArcaneEmergencyProtectionSnapshot emergency = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:test_mask", "black_arcana:test_mask", 8.0D, 200L)));
        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(8);

        var result = MinecraftArcaneDamagePipeline.activateHazardRuntime(
            runtime,
            hazard,
            zeroResistance(),
            ArcaneBacklashPolicy.canonical(),
            emergency);

        assertTrue(result.activated());
        assertEquals(
            emergency,
            runtime.sessions().find(castId).orElseThrow().emergencyProtectionSnapshot());
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
