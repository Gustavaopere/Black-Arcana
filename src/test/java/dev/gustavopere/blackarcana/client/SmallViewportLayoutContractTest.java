package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertTrue;

class SmallViewportLayoutContractTest {
    @Test
    void loadoutLayoutFitsGuiScaleFourSmallWindow() throws Exception {
        Class<?> layoutClass = Class.forName("dev.gustavopere.blackarcana.client.LoadoutLayout");
        Method forViewport = layoutClass.getDeclaredMethod("forViewport", int.class, int.class);
        Object layout = forViewport.invoke(null, 214, 120);
        int left = (int) layout.getClass().getDeclaredMethod("left").invoke(layout);
        int top = (int) layout.getClass().getDeclaredMethod("top").invoke(layout);
        int panelWidth = (int) layout.getClass().getDeclaredMethod("panelWidth").invoke(layout);
        int rowsPerPage = (int) layout.getClass().getDeclaredMethod("rowsPerPage").invoke(layout);
        int rowHeight = (int) layout.getClass().getDeclaredMethod("rowHeight").invoke(layout);

        assertTrue(left - 8 >= 0);
        assertTrue(left + panelWidth + 8 <= 214);
        assertTrue(top - 24 >= 0);
        assertTrue(top + rowsPerPage * rowHeight + 48 <= 120);
    }

    @Test
    void radialRadiusShrinksToKeepSlotCardsInsideSmallViewport() throws Exception {
        Method method = RadialLayout.class.getDeclaredMethod(
                "radiusForViewport",
                int.class, int.class, int.class, int.class, double.class, int.class);
        double radius = (double) method.invoke(null, 214, 120, 45, 12, 78.0D, 4);

        assertTrue(radius <= 44.0D);
        assertTrue(radius > 0.0D);
    }

    @Test
    void hudExposesViewportBoundedTextWidth() throws Exception {
        Method method = HudLayout.class.getDeclaredMethod(
                "maxTextWidth", int.class, int.class, int.class);
        int maxTextWidth = (int) method.invoke(null, 214, 10, 6);

        assertTrue(maxTextWidth > 0);
        assertTrue(maxTextWidth + 2 * 6 + 2 * 10 <= 214);
    }
}
