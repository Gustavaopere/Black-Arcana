package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PactSanctuaryContractTest {
    @Test
    void sanctuarySpecEnforcesAllHardCeilings() {
        PactSanctuarySpec spec = new PactSanctuarySpec(8, 200, 4);
        assertEquals(8, spec.radiusBlocks());
        assertEquals(200, spec.durationTicks());
        assertEquals(4, spec.memberBudget());

        assertThrows(IllegalArgumentException.class, () -> new PactSanctuarySpec(0, 200, 4));
        assertThrows(IllegalArgumentException.class,
                () -> new PactSanctuarySpec(NoeticSafetyCeilings.MAX_SANCTUARY_RADIUS + 1, 200, 4));
        assertThrows(IllegalArgumentException.class, () -> new PactSanctuarySpec(8, 0, 4));
        assertThrows(IllegalArgumentException.class,
                () -> new PactSanctuarySpec(8, NoeticSafetyCeilings.MAX_SANCTUARY_DURATION_TICKS + 1, 4));
        assertThrows(IllegalArgumentException.class, () -> new PactSanctuarySpec(8, 200, 0));
        assertThrows(IllegalArgumentException.class,
                () -> new PactSanctuarySpec(8, 200, NoeticSafetyCeilings.MAX_SANCTUARY_MEMBERS + 1));
    }

    @Test
    void sanctuaryServerWorkBudgetsAreBounded() {
        assertTrue(NoeticSafetyCeilings.MAX_ACTIVE_SANCTUARIES > 0);
        assertTrue(NoeticSafetyCeilings.MAX_SANCTUARY_MOBS_PER_TICK > 0);
        assertTrue(NoeticSafetyCeilings.MAX_SANCTUARY_MEMBERS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_SANCTUARY_RADIUS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_SANCTUARY_DURATION_TICKS > 0);
    }
}
