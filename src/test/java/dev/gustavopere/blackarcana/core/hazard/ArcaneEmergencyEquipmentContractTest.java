package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEmergencyEquipmentContractTest {
    @Test
    void explicitEmergencyProfileProducesFrozenCandidate() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();
        registry.register("black_arcana:containment_mask", new ArcaneEquipmentProfile(
            "black_arcana:containment_mask",
            12.0D,
            5.0D,
            0.0D,
            0.0D,
            null,
            Set.of("black_arcana:containment"),
            8.0D,
            200L));

        ArcaneEquipmentSnapshotService.Snapshot snapshot = new ArcaneEquipmentSnapshotService(registry).capture(List.of(
            new ArcaneEquipmentSlotSnapshot("head", "black_arcana:containment_mask", 73)));

        assertEquals(1, snapshot.emergencyProtectionCandidates().size());
        var candidate = snapshot.emergencyProtectionCandidates().getFirst();
        assertEquals("black_arcana:containment_mask", candidate.sourceId());
        assertEquals("black_arcana:containment_mask", candidate.resourceId());
        assertEquals(8.0D, candidate.absorption());
        assertEquals(200L, candidate.cooldownTicks());
    }

    @Test
    void brokenOrUnprofiledEquipmentCannotBecomeEmergencyProtection() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();
        registry.register("black_arcana:broken_charm", new ArcaneEquipmentProfile(
            "black_arcana:broken_charm",
            0.0D,
            0.0D,
            0.0D,
            0.0D,
            null,
            Set.of(),
            50.0D,
            100L));

        ArcaneEquipmentSnapshotService.Snapshot snapshot = new ArcaneEquipmentSnapshotService(registry).capture(List.of(
            new ArcaneEquipmentSlotSnapshot("offhand", "black_arcana:broken_charm", 0),
            new ArcaneEquipmentSlotSnapshot("chest", "minecraft:netherite_chestplate", 400)));

        assertTrue(snapshot.emergencyProtectionCandidates().isEmpty());
    }
}
