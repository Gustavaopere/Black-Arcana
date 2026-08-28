package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CorruptionResistanceCurveTest {
    @Test
    void resistanceReducesResidualMonotonicallyWithoutGoingNegative() {
        CorruptionResistanceCurve curve = CorruptionResistanceCurve.canonical();
        double zero = curve.residualMultiplier(0.0D);
        double low = curve.residualMultiplier(30.0D);
        double high = curve.residualMultiplier(180.0D);

        assertEquals(1.0D, zero, 1.0E-9D);
        assertTrue(zero > low);
        assertTrue(low > high);
        assertTrue(high >= 0.0D);
    }
}
