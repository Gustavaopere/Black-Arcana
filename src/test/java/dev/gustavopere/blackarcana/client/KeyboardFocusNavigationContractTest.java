package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class KeyboardFocusNavigationContractTest {
    private static final String CLASS_NAME = "dev.gustavopere.blackarcana.client.KeyboardFocusNavigation";

    @Test
    void exposesClientLocalPointerAndKeyboardModalities() {
        Class<?> navigation = navigationClass();
        Class<?> modality = Set.of(navigation.getDeclaredClasses()).stream()
                .filter(type -> type.getSimpleName().equals("InputModality"))
                .findFirst()
                .orElseGet(() -> fail("KeyboardFocusNavigation.InputModality is missing"));

        Set<String> values = Set.of(modality.getEnumConstants()).stream()
                .map(Object::toString)
                .collect(java.util.stream.Collectors.toSet());
        assertEquals(Set.of("POINTER", "KEYBOARD"), values);
    }

    @Test
    void radialInitialFocusPrefersSelectedVisibleSlotAndHandlesEmptyState() {
        assertEquals(5, invokeInt("radialInitialFocus", 8, 0, 5));
        assertEquals(0, invokeInt("radialInitialFocus", 8, 0, 12));
        assertEquals(8, invokeInt("radialInitialFocus", 16, 1, 8));
        assertEquals(-1, invokeInt("radialInitialFocus", 0, 0, 0));
    }

    @Test
    void radialTabTraversalWrapsWithinCurrentPageOnly() {
        assertEquals(1, invokeInt("radialTraverse", 16, 0, 0, 1));
        assertEquals(0, invokeInt("radialTraverse", 16, 0, 7, 1));
        assertEquals(7, invokeInt("radialTraverse", 16, 0, 0, -1));
        assertEquals(8, invokeInt("radialTraverse", 9, 1, 8, 1));
        assertEquals(8, invokeInt("radialTraverse", 9, 1, 8, -1));
        assertEquals(-1, invokeInt("radialTraverse", 0, 0, -1, 1));
    }

    @Test
    void radialPageChangePrefersSelectedThenPreservesOrClampsRelativePosition() {
        assertEquals(9, invokeInt("radialFocusAfterPageChange", 16, 0, 1, 9, 6));
        assertEquals(14, invokeInt("radialFocusAfterPageChange", 16, 0, 1, 0, 6));
        assertEquals(9, invokeInt("radialFocusAfterPageChange", 10, 0, 1, 0, 7));
        assertEquals(2, invokeInt("radialFocusAfterPageChange", 16, 1, 0, 12, 10));
    }

    @Test
    void loadoutInitialFocusUsesPreferredVisibleEntryOtherwiseFirstVisible() {
        assertEquals(4, invokeInt("loadoutInitialFocus", 12, 0, 8, 4));
        assertEquals(0, invokeInt("loadoutInitialFocus", 12, 0, 8, 10));
        assertEquals(10, invokeInt("loadoutInitialFocus", 12, 1, 8, 10));
        assertEquals(-1, invokeInt("loadoutInitialFocus", 0, 0, 8, -1));
    }

    @Test
    void loadoutUpDownClampWithinPageAndNeverCrossPageBoundary() {
        assertEquals(0, invokeInt("loadoutMoveRow", 16, 0, 8, 0, -1));
        assertEquals(1, invokeInt("loadoutMoveRow", 16, 0, 8, 0, 1));
        assertEquals(7, invokeInt("loadoutMoveRow", 16, 0, 8, 7, 1));
        assertEquals(8, invokeInt("loadoutMoveRow", 16, 1, 8, 8, -1));
        assertEquals(9, invokeInt("loadoutMoveRow", 10, 1, 8, 9, 1));
        assertEquals(-1, invokeInt("loadoutMoveRow", 0, 0, 8, -1, 1));
    }

    @Test
    void loadoutPageChangePreservesRelativeRowOrClampsToLastAvailableRow() {
        assertEquals(9, invokeInt("loadoutFocusAfterPageChange", 10, 0, 1, 8, 1));
        assertEquals(9, invokeInt("loadoutFocusAfterPageChange", 10, 0, 1, 8, 7));
        assertEquals(3, invokeInt("loadoutFocusAfterPageChange", 16, 1, 0, 8, 11));
    }

    @Test
    void everyComputedFocusRemainsInsideItsVisibleDestinationPage() {
        int radial = invokeInt("radialFocusAfterPageChange", 10, 0, 1, 0, 7);
        assertTrue(radial >= 8 && radial <= 9);

        int loadout = invokeInt("loadoutFocusAfterPageChange", 10, 0, 1, 8, 7);
        assertTrue(loadout >= 8 && loadout <= 9);
    }

    private static Class<?> navigationClass() {
        try {
            return Class.forName(CLASS_NAME);
        } catch (ClassNotFoundException exception) {
            return fail("KeyboardFocusNavigation is missing", exception);
        }
    }

    private static int invokeInt(String methodName, int... arguments) {
        try {
            Class<?> navigation = navigationClass();
            Class<?>[] parameterTypes = new Class<?>[arguments.length];
            Object[] boxed = new Object[arguments.length];
            for (int index = 0; index < arguments.length; index++) {
                parameterTypes[index] = int.class;
                boxed[index] = arguments[index];
            }
            Method method = navigation.getDeclaredMethod(methodName, parameterTypes);
            return (int) method.invoke(null, boxed);
        } catch (ReflectiveOperationException exception) {
            return fail("Missing or invalid keyboard-focus contract method: " + methodName, exception);
        }
    }
}
