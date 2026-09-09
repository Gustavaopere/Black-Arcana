package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ScreenFocusNavigationTest {
    @Test
    void initialFocusPrefersVisibleCanonicalIndexAndFallsBackToFirst() {
        List<Integer> visible = List.of(8, 9, 10, 11);

        assertEquals(10, ScreenFocusNavigation.initialFocus(visible, 10));
        assertEquals(8, ScreenFocusNavigation.initialFocus(visible, 3));
        assertEquals(-1, ScreenFocusNavigation.initialFocus(List.of(), 3));
    }

    @Test
    void wrappedTraversalStaysOnCurrentPage() {
        List<Integer> visible = List.of(8, 9, 10);

        assertEquals(9, ScreenFocusNavigation.moveWrapped(visible, 8, 1));
        assertEquals(8, ScreenFocusNavigation.moveWrapped(visible, 10, 1));
        assertEquals(10, ScreenFocusNavigation.moveWrapped(visible, 8, -1));
        assertEquals(8, ScreenFocusNavigation.moveWrapped(List.of(8), 8, 1));
        assertEquals(-1, ScreenFocusNavigation.moveWrapped(List.of(), 8, 1));
    }

    @Test
    void clampedTraversalNeverWrapsOrChangesPage() {
        List<Integer> visible = List.of(16, 17, 18);

        assertEquals(16, ScreenFocusNavigation.moveClamped(visible, 16, -1));
        assertEquals(17, ScreenFocusNavigation.moveClamped(visible, 16, 1));
        assertEquals(18, ScreenFocusNavigation.moveClamped(visible, 18, 1));
        assertEquals(-1, ScreenFocusNavigation.moveClamped(List.of(), 18, 1));
    }

    @Test
    void pageTransitionPrefersDestinationSelectionOtherwisePreservesRelativePosition() {
        List<Integer> source = List.of(0, 1, 2, 3);
        List<Integer> destination = List.of(8, 9, 10);

        assertEquals(9, ScreenFocusNavigation.transitionFocus(source, destination, 1, -1));
        assertEquals(10, ScreenFocusNavigation.transitionFocus(source, destination, 3, -1));
        assertEquals(10, ScreenFocusNavigation.transitionFocus(source, destination, 1, 10));
        assertEquals(-1, ScreenFocusNavigation.transitionFocus(source, List.of(), 1, -1));
    }

    @Test
    void invalidCurrentFocusIsReconciledBeforeTraversal() {
        List<Integer> visible = List.of(4, 5, 6);

        assertEquals(5, ScreenFocusNavigation.moveWrapped(visible, 99, 1));
        assertEquals(4, ScreenFocusNavigation.moveClamped(visible, 99, -1));
    }
}
