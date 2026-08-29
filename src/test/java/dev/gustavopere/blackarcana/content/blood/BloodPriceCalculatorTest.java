package dev.gustavopere.blackarcana.content.blood;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BloodPriceCalculatorTest {
    @Test
    void substitutesOnlyConfiguredBoundedFraction() {
        var quote = BloodPriceCalculator.quote(100.0D, 0.35D, 0.10D, 20.0D, 4.0D);
        assertEquals(65.0D, quote.resourceCost(), 1.0E-9);
        assertEquals(3.5D, quote.healthCost(), 1.0E-9);
        assertTrue(quote.affordable());
    }

    @Test
    void refusesQuoteThatWouldCrossHealthFloor() {
        var quote = BloodPriceCalculator.quote(100.0D, 0.50D, 0.20D, 10.0D, 4.0D);
        assertFalse(quote.affordable());
    }

    @Test
    void hardFractionAndHealthFloorCannotBeRelaxed() {
        assertThrows(IllegalArgumentException.class,
            () -> BloodPriceCalculator.quote(10.0D, 0.51D, 1.0D, 20.0D, 4.0D));
        assertThrows(IllegalArgumentException.class,
            () -> BloodPriceCalculator.quote(10.0D, 0.25D, 1.0D, 20.0D, 0.5D));
    }
}
