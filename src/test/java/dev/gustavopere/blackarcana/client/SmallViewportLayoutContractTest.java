package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SmallViewportLayoutContractTest {
    @Test
    void loadoutLayoutFitsGuiScaleFourSmallWindow() {
        LoadoutLayout layout = LoadoutLayout.forViewport(214, 120);

        assertTrue(layout.left() - 8 >= 0);
        assertTrue(layout.left() + layout.panelWidth() + 8 <= 214);
        assertTrue(layout.top() - 24 >= 0);
        assertTrue(layout.top() + layout.rowsPerPage() * layout.rowHeight() + 48 <= 120);
    }

    @Test
    void radialRadiusShrinksToKeepSlotCardsInsideSmallViewport() {
        RadialLayout.CardMetrics card = RadialLayout.cardMetricsForViewport(214, 120);
        double radius = RadialLayout.radiusForViewport(
                214, 120, card.halfWidth(), card.halfHeight(), 78.0D, 4);

        assertTrue(radius <= 49.0D);
        assertTrue(radius > 0.0D);
        assertTrue(card.compact());
    }

    @Test
    void eightRadialCardsDoNotOverlapAtGuiScaleFourSmallWindow() {
        int width = 214;
        int height = 120;
        RadialLayout.CardMetrics card = RadialLayout.cardMetricsForViewport(width, height);
        double radius = RadialLayout.radiusForViewport(
                width, height, card.halfWidth(), card.halfHeight(), 78.0D, 4);
        List<Rect> cards = new ArrayList<>();

        for (int index = 0; index < 8; index++) {
            RadialLayout.Point center = RadialLayout.slotCenter(
                    index, 8, width / 2.0D, height / 2.0D, radius);
            cards.add(new Rect(
                    center.x() - card.halfWidth(),
                    center.y() - card.halfHeight(),
                    center.x() + card.halfWidth(),
                    center.y() + card.halfHeight()));
        }

        for (int left = 0; left < cards.size(); left++) {
            for (int right = left + 1; right < cards.size(); right++) {
                assertFalse(cards.get(left).overlaps(cards.get(right)),
                        "radial cards overlap: " + left + " and " + right);
            }
        }
    }

    @Test
    void hudExposesViewportBoundedTextWidth() {
        int maxTextWidth = HudLayout.maxTextWidth(214, 10, 6);

        assertTrue(maxTextWidth > 0);
        assertTrue(maxTextWidth + 2 * 6 + 2 * 10 <= 214);
    }

    @Test
    void scaledFourLineHudCanReduceMarginInsteadOfOverflowingVertically() {
        int logicalWidth = 107;
        int logicalHeight = 60;
        int panelWidth = 87;
        int panelHeight = 54;
        int margin = HudLayout.boundedMargin(
                logicalWidth, logicalHeight, panelWidth, panelHeight, 10, 1);
        HudLayout.Point origin = HudLayout.origin(
                HudLayout.Anchor.BOTTOM_CENTER,
                logicalWidth, logicalHeight, panelWidth, panelHeight, margin);

        assertTrue(margin < 10);
        assertTrue(origin.x() - 1 >= 0);
        assertTrue(origin.y() - 1 >= 0);
        assertTrue(origin.x() + panelWidth + 1 <= logicalWidth);
        assertTrue(origin.y() + panelHeight + 1 <= logicalHeight);
    }

    private record Rect(double left, double top, double right, double bottom) {
        boolean overlaps(Rect other) {
            return left < other.right && right > other.left
                    && top < other.bottom && bottom > other.top;
        }
    }
}
