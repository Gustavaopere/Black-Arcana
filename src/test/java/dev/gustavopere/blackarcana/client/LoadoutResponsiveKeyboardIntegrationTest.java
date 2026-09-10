package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class LoadoutResponsiveKeyboardIntegrationTest {
    private static final Path SCREEN = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");

    @Test
    void iconGeometryIsOwnedByResponsiveLayoutAndFitsRequiredSmallViewport() throws Exception {
        LoadoutLayout layout = LoadoutLayout.forViewport(214, 120);
        Method iconSizeMethod;
        try {
            iconSizeMethod = LoadoutLayout.class.getDeclaredMethod("iconSize");
        } catch (NoSuchMethodException exception) {
            iconSizeMethod = fail("LoadoutLayout.iconSize() must own responsive icon sizing", exception);
        }
        iconSizeMethod.setAccessible(true);
        int iconSize = (int) iconSizeMethod.invoke(layout);

        assertTrue(iconSize > 0);
        assertTrue(iconSize <= layout.rowHeight() - 2,
                "icon must fit inside a row at the required small viewport");
        int textX = layout.left() + 8 + iconSize + 4;
        assertTrue(textX < layout.left() + layout.panelWidth(),
                "icon inset must leave bounded horizontal room for spell text");

        String source = Files.readString(SCREEN);
        assertTrue(source.contains("layout.iconSize()"),
                "screen must consume responsive icon geometry");
        assertFalse(source.contains("private static final int ICON_SIZE = 16;"),
                "fixed screen-local icon geometry bypasses responsive layout authority");
    }

    @Test
    void shiftArrowReorderMovesFocusedDraftSpellWithoutChangingCatalogIdentity() throws Exception {
        ArcanaSpellId a = ArcanaSpellId.parse("black_arcana:a");
        ArcanaSpellId b = ArcanaSpellId.parse("black_arcana:b");
        ArcanaSpellId c = ArcanaSpellId.parse("black_arcana:c");
        ArcanaSpellId d = ArcanaSpellId.parse("black_arcana:d");
        List<ArcanaSpellId> catalog = List.of(c, a, b, d);
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        Method moveFocused;
        try {
            moveFocused = BlackArcanaLoadoutScreen.class.getDeclaredMethod(
                    "moveFocusedDraft", int.class, List.class, LoadoutDraft.class, int.class);
        } catch (NoSuchMethodException exception) {
            moveFocused = fail("loadout screen must expose bounded focused-draft reorder operation", exception);
        }
        moveFocused.setAccessible(true);

        assertEquals(true, moveFocused.invoke(null, 2, catalog, draft, -1));
        assertEquals(List.of(b, a, c), draft.snapshot());
        assertEquals(true, moveFocused.invoke(null, 2, catalog, draft, 1));
        assertEquals(List.of(a, b, c), draft.snapshot());
        assertEquals(false, moveFocused.invoke(null, 3, catalog, draft, -1),
                "catalog spell outside the draft must not fabricate a slot");
        assertEquals(List.of(a, b, c), draft.snapshot());
        assertEquals(false, moveFocused.invoke(null, 1, catalog, draft, -1),
                "first draft slot cannot move earlier");
        assertEquals(false, moveFocused.invoke(null, 0, catalog, draft, 1),
                "last draft slot cannot move later");
        assertEquals(List.of(a, b, c), draft.snapshot());
    }

    @Test
    void searchOwnsShiftArrowEditingContextAndReorderAddsNoNetworkOrGlobalKeyPath() throws Exception {
        String source = Files.readString(SCREEN);
        int focusedGuard = source.indexOf("searchBox != null && searchBox.isFocused()");
        int shiftModifier = source.indexOf("GLFW.GLFW_MOD_SHIFT");
        int plainUp = source.indexOf("if (keyCode == GLFW.GLFW_KEY_UP) {", shiftModifier + 1);

        assertTrue(focusedGuard >= 0);
        assertTrue(shiftModifier > focusedGuard,
                "text input must keep ownership before screen-local Shift+Arrow reorder");
        assertTrue(plainUp > shiftModifier,
                "Shift+Arrow reorder must be resolved before plain Up/Down focus movement");
        assertTrue(source.contains("moveFocusedDraft("));
        assertEquals(1, occurrences(source, "LoadoutNetworkBridge.requestUpdate("));
        assertFalse(source.contains("new KeyMapping("),
                "A.6 reorder must remain screen-local and must not create a global mapping");
    }

    private static int occurrences(String haystack, String needle) {
        int count = 0;
        int from = 0;
        while ((from = haystack.indexOf(needle, from)) >= 0) {
            count++;
            from += needle.length();
        }
        return count;
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
