package dev.gustavopere.blackarcana.content.projection;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ProjectedWeaponProfileRegistryTest {
    @Test
    void registryIsBoundedPerOwnerAndReplacementDoesNotConsumeAnotherSlot() {
        var registry = new ProjectedWeaponProfileRegistry(2, 2);
        UUID owner = UUID.randomUUID();
        registry.remember(owner, profile("one", 4.0D));
        registry.remember(owner, profile("two", 5.0D));
        registry.remember(owner, profile("one", 6.0D));
        assertEquals(2, registry.snapshot(owner).size());
        assertEquals(6.0D, registry.find(owner, "black_arcana:one").orElseThrow().attackDamageContribution());
        assertThrows(IllegalStateException.class, () -> registry.remember(owner, profile("three", 6.0D)));
    }

    private static ProjectedWeaponProfile profile(String id, double damage) {
        return new ProjectedWeaponProfile("black_arcana:" + id, "minecraft:iron_sword",
            ProjectedWeaponProfile.Archetype.MELEE, damage, 1.6D, 0.0D);
    }
}
