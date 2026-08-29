package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentProfileRegistryTest {
    @Test
    void ordinaryArmorHasNoImplicitArcaneProfile() {
        ArcaneEquipmentProfileRegistry registry = new ArcaneEquipmentProfileRegistry();

        assertTrue(registry.resolve("minecraft:diamond_chestplate").isEmpty());
        assertTrue(registry.resolve("minecraft:netherite_chestplate").isEmpty());
    }
}
