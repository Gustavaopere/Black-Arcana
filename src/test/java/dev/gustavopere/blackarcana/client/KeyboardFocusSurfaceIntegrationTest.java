package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;
import org.lwjgl.glfw.GLFW;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class KeyboardFocusSurfaceIntegrationTest {
    @Test
    void boundedPageIndicesUseCanonicalAbsoluteIndices() {
        assertEquals(List.of(0, 1, 2), ScreenFocusNavigation.pageIndices(7, 0, 3));
        assertEquals(List.of(3, 4, 5), ScreenFocusNavigation.pageIndices(7, 1, 3));
        assertEquals(List.of(6), ScreenFocusNavigation.pageIndices(7, 2, 3));
        assertEquals(List.of(), ScreenFocusNavigation.pageIndices(0, 0, 3));
    }

    @Test
    void presentationTargetFollowsActiveModalityWithoutDestroyingFallback() {
        assertEquals(5, ScreenFocusNavigation.presentationFocus(
                ScreenFocusNavigation.InputModality.KEYBOARD, 2, 5, 1));
        assertEquals(2, ScreenFocusNavigation.presentationFocus(
                ScreenFocusNavigation.InputModality.POINTER, 2, 5, 1));
        assertEquals(1, ScreenFocusNavigation.presentationFocus(
                ScreenFocusNavigation.InputModality.POINTER, -1, 5, 1));
        assertEquals(1, ScreenFocusNavigation.presentationFocus(
                ScreenFocusNavigation.InputModality.KEYBOARD, 2, -1, 1));
    }

    @Test
    void radialKeyboardFocusHasASeparateNonColorCue() {
        assertEquals("[F] ", BlackArcanaRadialScreen.keyboardFocusPrefix(true, false));
        assertEquals("F", BlackArcanaRadialScreen.keyboardFocusPrefix(true, true));
        assertEquals("", BlackArcanaRadialScreen.keyboardFocusPrefix(false, false));
        assertEquals("", BlackArcanaRadialScreen.keyboardFocusPrefix(false, true));
    }

    @Test
    void loadoutKeyboardFocusDoesNotReuseMembershipMeaning() {
        assertEquals("[F] ", BlackArcanaLoadoutScreen.keyboardFocusPrefix(true));
        assertEquals("", BlackArcanaLoadoutScreen.keyboardFocusPrefix(false));
        assertEquals("[x] ", BlackArcanaLoadoutScreen.membershipPrefix(CastingUxSemantics.LoadoutMembership.ACCEPTED));
    }

    @Test
    void radialActivationIsEnterOrSpaceOnly() {
        assertTrue(BlackArcanaRadialScreen.isKeyboardActivationKey(GLFW.GLFW_KEY_ENTER));
        assertTrue(BlackArcanaRadialScreen.isKeyboardActivationKey(GLFW.GLFW_KEY_KP_ENTER));
        assertTrue(BlackArcanaRadialScreen.isKeyboardActivationKey(GLFW.GLFW_KEY_SPACE));
        assertFalse(BlackArcanaRadialScreen.isKeyboardActivationKey(GLFW.GLFW_KEY_TAB));
        assertFalse(BlackArcanaRadialScreen.isKeyboardActivationKey(GLFW.GLFW_KEY_RIGHT));
    }

    @Test
    void loadoutSpaceTogglesRowButEnterRemainsApply() {
        assertTrue(BlackArcanaLoadoutScreen.isDraftToggleKey(GLFW.GLFW_KEY_SPACE));
        assertFalse(BlackArcanaLoadoutScreen.isDraftToggleKey(GLFW.GLFW_KEY_ENTER));
        assertFalse(BlackArcanaLoadoutScreen.isDraftToggleKey(GLFW.GLFW_KEY_DELETE));
    }
}
