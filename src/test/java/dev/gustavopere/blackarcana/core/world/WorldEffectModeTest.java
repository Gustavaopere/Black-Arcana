package dev.gustavopere.blackarcana.core.world;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WorldEffectModeTest {
    @Test
    void modesFormStrictSafetyCeiling() {
        assertFalse(WorldEffectMode.OFF.allows(WorldMutationClass.COSMETIC));
        assertTrue(WorldEffectMode.COSMETIC.allows(WorldMutationClass.COSMETIC));
        assertFalse(WorldEffectMode.COSMETIC.allows(WorldMutationClass.TEMPORARY));
        assertTrue(WorldEffectMode.TEMPORARY.allows(WorldMutationClass.TEMPORARY));
        assertFalse(WorldEffectMode.TEMPORARY.allows(WorldMutationClass.LIMITED));
        assertTrue(WorldEffectMode.LIMITED.allows(WorldMutationClass.LIMITED));
        assertFalse(WorldEffectMode.LIMITED.allows(WorldMutationClass.PERMANENT));
        assertTrue(WorldEffectMode.FULL.allows(WorldMutationClass.PERMANENT));
    }

    @Test
    void perSpellModeCannotElevateGlobalMode() {
        assertTrue(WorldEffectMode.mostRestrictive(WorldEffectMode.TEMPORARY, WorldEffectMode.FULL)
            == WorldEffectMode.TEMPORARY);
        assertTrue(WorldEffectMode.mostRestrictive(WorldEffectMode.FULL, WorldEffectMode.COSMETIC)
            == WorldEffectMode.COSMETIC);
    }
}
