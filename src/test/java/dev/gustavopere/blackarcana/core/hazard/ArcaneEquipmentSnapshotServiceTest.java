package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcaneEquipmentSnapshotServiceTest {
    @Test
    void snapshotIncludesOnlyExplicitProfilesAndFreezesSetComposition() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();
        registry.register("black_arcana:veil_hood", new ArcaneEquipmentProfile(
            "black_arcana:veil_hood", 12.0D, 5.0D, 8.0D, 0.1D,
            "black_arcana:veil", Set.of("black_arcana:containment")));
        registry.register("black_arcana:veil_robe", new ArcaneEquipmentProfile(
            "black_arcana:veil_robe", 18.0D, 9.0D, 12.0D, 0.2D,
            "black_arcana:veil", Set.of("black_arcana:containment")));

        ArcaneEquipmentSnapshotService.Snapshot snapshot = new ArcaneEquipmentSnapshotService(registry).capture(List.of(
            new ArcaneEquipmentSlotSnapshot("head", "black_arcana:veil_hood", 100),
            new ArcaneEquipmentSlotSnapshot("chest", "black_arcana:veil_robe", 250),
            new ArcaneEquipmentSlotSnapshot("legs", "minecraft:netherite_leggings", 400)));

        assertEquals(2, snapshot.items().size());
        assertEquals(2, snapshot.setPieces("black_arcana:veil"));
        assertEquals(30.0D, snapshot.arcaneResistance());
        assertEquals(14.0D, snapshot.corruptionResistance());
        assertEquals(20.0D, snapshot.strainCapacityBonus());
        assertEquals(0.3D, snapshot.strainRecoveryPerTick(), 1.0e-9D);
    }

    @Test
    void laterRegistryChangesDoNotMutateExistingSnapshot() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();
        registry.register("black_arcana:ward_mask", ArcaneEquipmentProfile.resistanceOnly(
            "black_arcana:ward_mask", 10.0D, 3.0D));
        ArcaneEquipmentSnapshotService service = new ArcaneEquipmentSnapshotService(registry);

        var snapshot = service.capture(List.of(
            new ArcaneEquipmentSlotSnapshot("head", "black_arcana:ward_mask", 50)));
        registry.register("black_arcana:ward_gloves", ArcaneEquipmentProfile.resistanceOnly(
            "black_arcana:ward_gloves", 99.0D, 99.0D));

        assertEquals(10.0D, snapshot.arcaneResistance());
        assertEquals(1, snapshot.items().size());
    }
}
