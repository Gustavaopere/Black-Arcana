package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEmergencyHazardSnapshotTest {
    @Test
    void hazardRuntimeRetainsFrozenEmergencyCandidatesUntilSettlementLifecycleEnds() {
        ArcanaCastId castId = ArcanaCastId.parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16, 0.0D, 0.0D, true);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            castId,
            ArcanaSpellId.parse("black_arcana:test_emergency"),
            UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            "minecraft:overworld",
            10L,
            profile);
        ArcaneEmergencyProtectionSnapshot emergency = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:containment_mask",
                "black_arcana:containment_mask",
                8.0D,
                200L)));

        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(8);
        var activated = runtime.activate(
            hazard,
            ArcaneResistanceSnapshot.zero(),
            ArcaneBacklashPolicy.canonical(),
            emergency);

        assertTrue(activated.activated());
        var stored = runtime.sessions().find(castId).orElseThrow().emergencyProtectionSnapshot();
        assertEquals(emergency, stored);
        assertEquals(1, stored.candidates().size());
    }

    @Test
    void legacyActivationDefaultsToNoEmergencyCandidates() {
        ArcanaCastId castId = ArcanaCastId.parse("cccccccc-cccc-cccc-cccc-cccccccccccc");
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            castId,
            ArcanaSpellId.parse("black_arcana:test_legacy"),
            UUID.fromString("dddddddd-dddd-dddd-dddd-dddddddddddd"),
            "minecraft:overworld",
            10L,
            new ArcaneDangerProfile(
                ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16, 0.0D, 0.0D, false));

        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(8);
        runtime.activate(hazard, ArcaneResistanceSnapshot.zero(), ArcaneBacklashPolicy.canonical());

        assertTrue(runtime.sessions().find(castId).orElseThrow()
            .emergencyProtectionSnapshot().candidates().isEmpty());
    }
}
