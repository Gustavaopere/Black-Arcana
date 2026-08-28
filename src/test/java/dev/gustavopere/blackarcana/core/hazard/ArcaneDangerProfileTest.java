package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneDangerProfileTest {
    @Test
    void normalProfileBypassesSevereHazardSession() {
        ArcaneDangerProfile profile = ArcaneDangerProfile.normal();

        assertFalse(profile.requiresHazardSession());
    }

    @Test
    void dangerousProfileRequiresHazardSession() {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            1.0D,
            0.25D,
            0.5D,
            200L,
            32);

        assertTrue(profile.requiresHazardSession());
    }

    @Test
    void rejectsNonFiniteAndOutOfBoundsProfileNumbers() {
        assertThrows(IllegalArgumentException.class, () -> new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            Double.NaN,
            0.0D,
            0.0D,
            20L,
            8));
        assertThrows(IllegalArgumentException.class, () -> new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN,
            Double.POSITIVE_INFINITY,
            0.0D,
            0.0D,
            20L,
            8));
        assertThrows(IllegalArgumentException.class, () -> new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            ArcaneDangerProfile.ABSOLUTE_MAX_BACKLASH_MULTIPLIER + 0.01D,
            0.0D,
            0.0D,
            20L,
            8));
        assertThrows(IllegalArgumentException.class, () -> new ArcaneDangerProfile(
            ArcaneDangerTier.UNSTABLE,
            0.0D,
            0.0D,
            1.0D,
            ArcaneDangerProfile.ABSOLUTE_MAX_DAMAGE_LEASE_TICKS + 1L,
            8));
        assertThrows(IllegalArgumentException.class, () -> new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            1.0D,
            0.0D,
            0.0D,
            20L,
            ArcaneDangerProfile.ABSOLUTE_MAX_DAMAGE_INSTANCES + 1));
    }
}
