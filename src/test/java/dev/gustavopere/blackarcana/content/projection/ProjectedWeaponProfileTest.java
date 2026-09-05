package dev.gustavopere.blackarcana.content.projection;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ProjectedWeaponProfileTest {
    @Test
    void sanitizerClampsObservedDamageAndCarriesNoArbitraryPersistenceData() {
        var profile = ProjectedWeaponProfile.sanitized(
            "black_arcana:test_blade", "modded:absurd_sword", ProjectedWeaponProfile.Archetype.MELEE,
            9999.0D, 2.0D, 0.0D);
        assertEquals(ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE, profile.attackDamageContribution());
        assertEquals("modded:absurd_sword", profile.sourceItemId());
        assertEquals(6, ProjectedWeaponProfile.class.getRecordComponents().length,
            "profile schema must remain an explicit value object rather than arbitrary NBT/components");
    }

    @Test
    void directConstructionCannotExceedHardDamageCeiling() {
        assertThrows(IllegalArgumentException.class, () -> new ProjectedWeaponProfile(
            "black_arcana:bad", "minecraft:diamond_sword", ProjectedWeaponProfile.Archetype.MELEE,
            101.0D, 2.0D, 0.0D));
    }
}
