package dev.gustavopere.blackarcana.core.hazard;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneResistanceCurveTest {
    @Test
    void canonicalCurveKeepsZeroResistanceAtFullBacklash() {
        ArcaneResistanceCurve curve = ArcaneResistanceCurve.canonical();

        assertEquals(1.0D, curve.residualMultiplier(0.0D), 0.0D);
        assertEquals(0.8D, curve.residualMultiplier(10.0D), 1.0E-12D);
        assertEquals(0.5D, curve.residualMultiplier(40.0D), 1.0E-12D);
        assertEquals(1.0D / 3.0D, curve.residualMultiplier(80.0D), 1.0E-12D);
        assertEquals(0.25D, curve.residualMultiplier(120.0D), 1.0E-12D);
        assertEquals(1.0D / 7.0D, curve.residualMultiplier(240.0D), 1.0E-12D);
        assertEquals(1.0D / 7.0D, curve.residualMultiplier(10_000.0D), 1.0E-12D);
    }

    @Test
    void residualIsMonotonicAndNeverHealing() {
        ArcaneResistanceCurve curve = ArcaneResistanceCurve.canonical();
        double previous = curve.residualMultiplier(0.0D);
        for (int resistance = 1; resistance <= 500; resistance++) {
            double current = curve.residualMultiplier(resistance);
            assertTrue(current >= 0.0D && current <= previous);
            previous = current;
        }
    }

    @Test
    void rejectsInvalidCurveInputs() {
        ArcaneResistanceCurve curve = ArcaneResistanceCurve.canonical();
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(Double.POSITIVE_INFINITY));
        assertThrows(IllegalArgumentException.class, () -> curve.residualMultiplier(-0.01D));
    }
}
