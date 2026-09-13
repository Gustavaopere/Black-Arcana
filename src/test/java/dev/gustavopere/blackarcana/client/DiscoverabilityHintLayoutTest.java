package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DiscoverabilityHintLayoutTest {
    @Test
    void standardViewportUsesBoundedPreferredWidth() {
        var layout = DiscoverabilityHintLayout.forViewport(854, 480);

        assertEquals(360, layout.width());
        assertEquals(8, layout.x());
        assertEquals(8, layout.y());
        assertTrue(layout.x() + layout.width() <= 854);
        assertTrue(layout.maxHeight() <= 480);
    }

    @Test
    void narrowViewportNeverEscapesHorizontalBounds() {
        var layout = DiscoverabilityHintLayout.forViewport(160, 100);

        assertTrue(layout.x() >= 0);
        assertTrue(layout.width() > 0);
        assertTrue(layout.x() + layout.width() <= 160);
        assertTrue(layout.y() >= 0);
        assertTrue(layout.maxHeight() > 0);
        assertTrue(layout.y() + layout.maxHeight() <= 100);
    }

    @Test
    void tinyViewportStillReturnsPositiveContainedGeometry() {
        var layout = DiscoverabilityHintLayout.forViewport(12, 12);

        assertTrue(layout.x() >= 0);
        assertTrue(layout.y() >= 0);
        assertTrue(layout.width() >= 1);
        assertTrue(layout.maxHeight() >= 1);
        assertTrue(layout.x() + layout.width() <= 12);
        assertTrue(layout.y() + layout.maxHeight() <= 12);
    }
}
