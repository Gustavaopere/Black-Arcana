package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneStrainProfileTest {
    @Test
    void unavoidableFloorSurvivesFullAvoidableMitigation() {
        ArcaneStrainProfile profile = new ArcaneStrainProfile(20.0D, 2.0D, 0.5D, 5.0D, 2.0D, 1.0D, 800.0D);
        assertEquals(5.0D, profile.appliedStrain(10.0D, 20L, 0.0D));
        assertEquals(50.0D, profile.appliedStrain(10.0D, 20L, 1.0D));
    }

    @Test
    void currentStrainOnlyAmplifiesWhenProfileDeclaresIt() {
        assertEquals(1.0D, ArcaneStrainProfile.none().backlashMultiplier(900.0D, 1_000.0D));
        assertEquals(1.0D, ArcaneStrainProfile.none().corruptionMultiplier(900.0D, 1_000.0D));
        assertFalse(ArcaneStrainProfile.none().hardGateActive(1_000.0D));

        ArcaneStrainProfile hazardous = new ArcaneStrainProfile(1.0D, 0.0D, 0.0D, 0.0D, 2.0D, 1.0D, 800.0D);
        assertEquals(2.8D, hazardous.backlashMultiplier(900.0D, 1_000.0D), 1.0E-9D);
        assertEquals(1.9D, hazardous.corruptionMultiplier(900.0D, 1_000.0D), 1.0E-9D);
        assertTrue(hazardous.hardGateActive(900.0D));
    }
}
