package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

class ArcaneStrainProfileRegistryTest {
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:strain_profile_test");

    @Test
    void missingProfileFallsBackToLegacyCommittedCastCoefficient() {
        ArcaneStrainProfileRegistry registry = new ArcaneStrainProfileRegistry();
        ArcaneStrainProfile resolved = registry.resolveOrCommittedCast(SPELL, 12.0D);

        assertEquals(12.0D, resolved.baseStrainPerCommittedCast(), 0.0D);
        assertEquals(0.0D, resolved.maxBacklashBonusMultiplier(), 0.0D);
        assertEquals(0.0D, resolved.maxCorruptionBonusMultiplier(), 0.0D);
        assertEquals(0.0D, resolved.hardGateThresholdUnits(), 0.0D);
    }

    @Test
    void explicitProfileOverridesFallbackWithoutInventingBalance() {
        ArcaneStrainProfileRegistry registry = new ArcaneStrainProfileRegistry();
        ArcaneStrainProfile explicit = new ArcaneStrainProfile(
            20.0D, 1.0D, 0.5D, 4.0D, 2.0D, 1.0D, 800.0D);
        registry.replaceAll(Map.of(SPELL, explicit));

        assertSame(explicit, registry.resolveOrCommittedCast(SPELL, 999.0D));
        assertEquals(1, registry.size());
    }
}
