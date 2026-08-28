package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RadialLayoutTest {
    @Test
    void eightSlotsFitOnePageAndSixteenUseTwo() {
        assertEquals(1, RadialLayout.pageCount(8));
        assertEquals(2, RadialLayout.pageCount(16));
        assertEquals(List.of(8, 9, 10, 11, 12, 13, 14, 15), RadialLayout.visibleSlots(16, 1));
    }

    @Test
    void topDirectionSelectsFirstVisibleSlot() {
        int slot = RadialLayout.hoveredSlot(8, 0, 100.0D, 20.0D, 100.0D, 100.0D, 32.0D, 112.0D);
        assertEquals(0, slot);
    }

    @Test
    void centerDeadZoneNeverSelects() {
        assertEquals(-1, RadialLayout.hoveredSlot(8, 0, 100.0D, 100.0D, 100.0D, 100.0D, 32.0D, 112.0D));
    }

    @Test
    void secondPageReturnsGlobalSlotIndexes() {
        int slot = RadialLayout.hoveredSlot(16, 1, 100.0D, 20.0D, 100.0D, 100.0D, 32.0D, 112.0D);
        assertEquals(8, slot);
    }
}
