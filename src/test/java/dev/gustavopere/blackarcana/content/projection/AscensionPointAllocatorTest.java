package dev.gustavopere.blackarcana.content.projection;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AscensionPointAllocatorTest {
    @Test
    void curveHasDiminishingReturnsAndHardPointCap() {
        var policy = new AscensionPointAllocator.Policy(10.0D, 0.5D, 20);
        int low = AscensionPointAllocator.allocate(new AscensionPointAllocator.Sacrifice(40.0D, false), policy).points();
        int high = AscensionPointAllocator.allocate(new AscensionPointAllocator.Sacrifice(160.0D, false), policy).points();
        int huge = AscensionPointAllocator.allocate(new AscensionPointAllocator.Sacrifice(1_000_000.0D, false), policy).points();
        assertEquals(2, low);
        assertEquals(4, high);
        assertEquals(20, huge);
        assertTrue((high - low) < (160.0D - 40.0D), "point growth must be sublinear");
    }

    @Test
    void recursiveAugmentedInputIsRejected() {
        var allocation = AscensionPointAllocator.allocate(
            new AscensionPointAllocator.Sacrifice(1000.0D, true),
            new AscensionPointAllocator.Policy(10.0D, 0.5D, 20));
        assertFalse(allocation.accepted());
        assertEquals("recursive_input", allocation.denialCode());
    }
}
