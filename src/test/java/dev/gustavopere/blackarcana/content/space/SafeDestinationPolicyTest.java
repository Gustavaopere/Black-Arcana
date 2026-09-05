package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SafeDestinationPolicyTest {
    private final SafeDestinationPolicy policy = new SafeDestinationPolicy();

    @Test
    void fullyValidLoadedDestinationIsAccepted() {
        assertTrue(policy.validate(valid()).allowed());
    }

    @Test
    void unloadedCollisionBorderFluidAndDimensionFailuresAreStructured() {
        assertEquals("destination_unloaded", policy.validate(new SafeDestinationPolicy.Facts(false, true, true, true, true, true, true, false)).code());
        assertEquals("world_border", policy.validate(new SafeDestinationPolicy.Facts(true, false, true, true, true, true, true, false)).code());
        assertEquals("collision_blocked", policy.validate(new SafeDestinationPolicy.Facts(true, true, false, true, true, true, true, false)).code());
        assertEquals("fluid_denied", policy.validate(new SafeDestinationPolicy.Facts(true, true, true, true, false, true, true, false)).code());
        assertEquals("dimension_denied", policy.validate(new SafeDestinationPolicy.Facts(true, true, true, true, true, false, true, false)).code());
    }

    static SafeDestinationPolicy.Facts valid() {
        return new SafeDestinationPolicy.Facts(true, true, true, true, true, true, true, false);
    }
}
