package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
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

    @Test
    void canonicalCurveSaturatesAtConfiguredResistanceCap() {
        CorruptionResistanceCurve curve = CorruptionResistanceCurve.canonical();
        double atCap = curve.residualMultiplier(CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE);
        assertEquals(atCap, curve.residualMultiplier(Double.MAX_VALUE), 0.0D);
        assertTrue(atCap > 0.0D && atCap < 1.0D);
    }

    @Test
    void rejectsNonFiniteNegativeAndInvalidCurveParameters() {
        CorruptionResistanceCurve curve = CorruptionResistanceCurve.canonical();
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(Double.POSITIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(-0.01D));
        assertThrows(IllegalArgumentException.class, () -> new CorruptionResistanceCurve(0.0D, 100.0D));
        assertThrows(IllegalArgumentException.class, () -> new CorruptionResistanceCurve(Double.NaN, 100.0D));
        assertThrows(IllegalArgumentException.class, () -> new CorruptionResistanceCurve(60.0D, Double.POSITIVE_INFINITY));
    }
}
