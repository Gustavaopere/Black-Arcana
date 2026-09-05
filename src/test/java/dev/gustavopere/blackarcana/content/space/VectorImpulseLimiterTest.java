package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class VectorImpulseLimiterTest {
    @Test
    void excessiveImpulseIsNormalizedToConfiguredSpeed() {
        var vector = VectorImpulseLimiter.clamp(10.0D, 0.0D, 0.0D, 1.5D);
        assertEquals(1.5D, vector.speed(), 1.0E-9);
        assertThrows(IllegalArgumentException.class, () -> VectorImpulseLimiter.clamp(1, 0, 0, 2.6D));
    }
}
