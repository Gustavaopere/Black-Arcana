package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneDangerProfileRegistryTest {
    private static final ArcanaSpellId DANGEROUS = ArcanaSpellId.parse("black_arcana:test_dangerous");

    @Test
    void replaceAllPublishesOneAtomicSnapshot() {
        ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS, 1.0D, 2.0D, 3.0D, 100L, 16);

        registry.replaceAll(Map.of(DANGEROUS, profile));

        assertEquals(profile, registry.resolve(DANGEROUS).orElseThrow());
        assertEquals(1, registry.snapshot().size());
    }

    @Test
    void requiredHazardProfileFailsClosedWhenMissingOrNormal() {
        ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
        assertThrows(IllegalStateException.class, () -> registry.requireHazardous(DANGEROUS));

        registry.replaceAll(Map.of(DANGEROUS, ArcaneDangerProfile.normal()));
        assertThrows(IllegalStateException.class, () -> registry.requireHazardous(DANGEROUS));
    }
}
