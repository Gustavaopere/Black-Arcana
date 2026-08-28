package dev.gustavopere.blackarcana.core.progression;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DiminishingReturnsCurveTest {
    @Test void curveIsMonotonicAndNeverExceedsHardCap() {
        double previous = 1D;
        for (int raw = 0; raw <= 1_000_000; raw += 1000) {
            double current = DiminishingReturnsCurve.apply(1D, raw, 2D, 100D);
            assertTrue(current >= previous);
            assertTrue(current <= 2D);
            previous = current;
        }
    }

    @Test void extremeProgressionStillCannotBreakLocalEnvelope() {
        var envelope = new ProgressionScalingEnvelope(1D, 2.5D, 100D);
        double multiplier = envelope.multiplier(Long.MAX_VALUE, Integer.MAX_VALUE, 1_000_000D, 1_000_000D);
        assertTrue(Double.isFinite(multiplier));
        assertTrue(multiplier <= 2.5D);
        assertTrue(multiplier >= 1D);
    }
}
