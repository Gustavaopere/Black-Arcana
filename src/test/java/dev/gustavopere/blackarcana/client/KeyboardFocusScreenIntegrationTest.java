package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class KeyboardFocusScreenIntegrationTest {
    private static final Path RADIAL = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaRadialScreen.java");
    private static final Path LOADOUT = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path SEMANTICS = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/CastingUxSemantics.java");

    @Test
    void radialWiresKeyboardTraversalActivationAndNonCastingSelection() throws Exception {
        String source = Files.readString(RADIAL);
        assertTrue(source.contains("KeyboardFocusNavigation.radialInitialFocus("));
        assertTrue(source.contains("GLFW.GLFW_KEY_TAB"));
        assertTrue(source.contains("KeyboardFocusNavigation.radialTraverse("));
        assertTrue(source.contains("KeyboardFocusNavigation.radialFocusAfterPageChange("));
        assertTrue(source.contains("GLFW.GLFW_KEY_SPACE"));
        assertFalse(source.contains("sendCastIntent("), "radial screen must remain a selector, not a cast path");
        assertFalse(source.contains("ArcanaNetworkBridge"), "radial screen must not gain cast-network authority");

        ArcanaSpellId a = ArcanaSpellId.parse("black_arcana:a");
        ArcanaSpellId b = ArcanaSpellId.parse("black_arcana:b");
        ClientLoadoutSelection selection = new ClientLoadoutSelection();
        Method select = BlackArcanaRadialScreen.class.getDeclaredMethod(
                "selectFocusedSlot", int.class, List.class, ClientLoadoutSelection.class);
        select.setAccessible(true);
        assertEquals(true, select.invoke(null, 1, List.of(a, b), selection));
        assertEquals(1, selection.selectedSlot());
        assertEquals(false, select.invoke(null, -1, List.of(a, b), selection));
        assertEquals(1, selection.selectedSlot());
    }

    @Test
    void loadoutWiresBoundedRowFocusAndSpaceOnlyMutatesLocalDraft() throws Exception {
        String source = Files.readString(LOADOUT);
        assertTrue(source.contains("KeyboardFocusNavigation.loadoutInitialFocus("));
        assertTrue(source.contains("GLFW.GLFW_KEY_UP"));
        assertTrue(source.contains("GLFW.GLFW_KEY_DOWN"));
        assertTrue(source.contains("KeyboardFocusNavigation.loadoutMoveRow("));
        assertTrue(source.contains("KeyboardFocusNavigation.loadoutFocusAfterPageChange("));
        assertTrue(source.contains("GLFW.GLFW_KEY_SPACE"));
        assertTrue(source.contains("keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER"),
                "Enter must remain apply");
        assertTrue(source.contains("keyCode == GLFW.GLFW_KEY_BACKSPACE || keyCode == GLFW.GLFW_KEY_DELETE"),
                "Delete/Backspace must remain clear-all draft");

        ArcanaSpellId a = ArcanaSpellId.parse("black_arcana:a");
        ArcanaSpellId b = ArcanaSpellId.parse("black_arcana:b");
        LoadoutDraft draft = new LoadoutDraft(List.of(a));
        Method toggle = BlackArcanaLoadoutScreen.class.getDeclaredMethod(
                "toggleFocusedDraft", int.class, List.class, LoadoutDraft.class);
        toggle.setAccessible(true);
        assertEquals(true, toggle.invoke(null, 1, List.of(a, b), draft));
        assertEquals(List.of(a, b), draft.snapshot());
        assertEquals(false, toggle.invoke(null, -1, List.of(a, b), draft));
        assertEquals(List.of(a, b), draft.snapshot());
    }

    @Test
    void presentationSemanticsExposeKeyboardFocusAsIndependentNonColorRole() throws IOException {
        String semantics = Files.readString(SEMANTICS);
        String radial = Files.readString(RADIAL);
        String loadout = Files.readString(LOADOUT);

        assertTrue(semantics.contains("FOCUSED"));
        assertTrue(radial.contains("[F]"), "radial keyboard focus needs a non-color marker");
        assertTrue(loadout.contains("[F]"), "loadout keyboard focus needs a non-color marker");
        assertTrue(radial.contains("KeyboardFocusNavigation.InputModality"));
        assertTrue(loadout.contains("KeyboardFocusNavigation.InputModality"));
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);

        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle")) && Files.isDirectory(candidate.resolve(".github"))) {
                return candidate;
            }
            candidate = candidate.getParent();
        }
        return fail("Unable to locate repository root from test working directory");
    }
}
