package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class HudLayoutTest {
    @Test
    void anchorsRemainInsideCommonGuiSizes() {
        int[][] sizes = {{427, 240}, {960, 540}, {1720, 720}};
        for (int[] size : sizes) {
            for (HudLayout.Anchor anchor : HudLayout.Anchor.values()) {
                HudLayout.Point point = HudLayout.origin(anchor, size[0], size[1], 140, 34, 10);
                assertTrue(point.x() >= 0 && point.x() + 140 <= size[0]);
                assertTrue(point.y() >= 0 && point.y() + 34 <= size[1]);
            }
        }
    }

    @Test
    void bottomCenterIsStable() {
        assertEquals(new HudLayout.Point(130, 196),
                HudLayout.origin(HudLayout.Anchor.BOTTOM_CENTER, 400, 240, 140, 34, 10));
    }

    @Test
    void recencyIsBoundedAndRejectsClockRegression() {
        assertTrue(HudLayout.isRecent(100, 90, 10));
        assertFalse(HudLayout.isRecent(101, 90, 10));
        assertFalse(HudLayout.isRecent(89, 90, 10));
        assertFalse(HudLayout.isRecent(100, Long.MIN_VALUE, 10));
        assertFalse(HudLayout.isRecent(100, 90, 0));
    }
}
