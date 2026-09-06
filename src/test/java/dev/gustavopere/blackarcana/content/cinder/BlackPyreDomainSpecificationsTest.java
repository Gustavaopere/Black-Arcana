package dev.gustavopere.blackarcana.content.cinder;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BlackPyreDomainSpecificationsTest {
    @Test
    void blackPyreIdentityAndDefaultSafetyContractAreFrozen() {
        var specs = BlackPyreDomainSpecifications.all();
        assertEquals(1, specs.size());
        var spec = specs.getFirst();
        assertEquals("black_arcana:black_pyre", spec.spellId().canonical());
        assertEquals(ArcanaDomain.BLACK_FLAME, spec.domain());
        assertEquals(WorldEffectMode.TEMPORARY, spec.worldEffectMode());
        assertEquals(300L, spec.cooldownTicks());
        assertEquals("T3 Cinder", spec.progressionGate());
        assertTrue(spec.hostIntegration().contains("Iron's"));
        assertTrue(spec.hostIntegration().contains("Malum"));
        assertTrue(spec.configSurface().contains("radius"));
        assertTrue(spec.configSurface().contains("concurrent frontiers"));
    }

    @Test
    void technicalCeilingsMatchTheApprovedBlackFlameContract() {
        assertEquals(12, BlackPyreSafetyCeilings.MAX_RADIUS_BLOCKS);
        assertEquals(256, BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER);
        assertEquals(16, BlackPyreSafetyCeilings.MAX_SPREAD_PER_TICK);
        assertEquals(8, BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS);
        assertEquals(1200L, BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS);
    }
}
