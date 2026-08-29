package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentProfileRegistryTest {
    @Test
    void ordinaryArmorHasNoImplicitArcaneProfile() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();

        assertTrue(registry.resolve("minecraft:diamond_chestplate").isEmpty());
        assertTrue(registry.resolve("minecraft:netherite_chestplate").isEmpty());
    }

    @Test
    void replaceAllPublishesOneValidatedSnapshotAtomically() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();
        registry.register("minecraft:diamond_helmet",
            ArcaneEquipmentProfile.resistanceOnly("black_arcana:old", 1.0D, 1.0D));

        registry.replaceAll(Map.of(
            "minecraft:golden_helmet",
            ArcaneEquipmentProfile.resistanceOnly("black_arcana:new", 20.0D, 15.0D)));

        assertTrue(registry.resolve("minecraft:diamond_helmet").isEmpty());
        assertEquals(20.0D, registry.resolve("minecraft:golden_helmet").orElseThrow().arcaneResistance());
        assertEquals(1, registry.size());
    }
}
