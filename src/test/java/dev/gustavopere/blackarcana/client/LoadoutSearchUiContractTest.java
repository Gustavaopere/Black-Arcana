package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class LoadoutSearchUiContractTest {
    private static final Path SCREEN = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path EN_US = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/en_us.json");
    private static final Path PT_BR = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/pt_br.json");

    @Test
    void responsiveHeaderReservesSearchFieldInsideSmallViewport() {
        LoadoutLayout layout = LoadoutLayout.forViewport(214, 120);

        assertTrue(layout.panelTop() >= 0);
        assertTrue(layout.titleY() >= layout.panelTop());
        assertTrue(layout.searchY() > layout.titleY());
        assertTrue(layout.searchHeight() > 0);
        assertTrue(layout.searchY() + layout.searchHeight() <= layout.top());
        assertTrue(layout.top() + layout.rowsPerPage() * layout.rowHeight() + 48 <= 120);
    }

    @Test
    void screenUsesVanillaEditBoxAndFilteredCatalogWithoutAdditionalNetworkPath() throws Exception {
        String source = Files.readString(SCREEN);
        String english = Files.readString(EN_US);
        String portuguese = Files.readString(PT_BR);

        assertTrue(source.contains("import net.minecraft.client.gui.components.EditBox;"));
        assertTrue(source.contains("private EditBox searchBox;"));
        assertTrue(source.contains("private List<ArcanaSpellId> filteredAvailable;"));
        assertTrue(source.contains("addRenderableWidget(searchBox);"));
        assertTrue(source.contains("searchBox.setResponder(this::onSearchChanged);"));
        assertTrue(source.contains("LoadoutCatalogSearch.filter("));
        assertTrue(source.contains("screen.black_arcana.loadout.search"));
        assertTrue(english.contains("Search spells"));
        assertTrue(portuguese.contains("Buscar feitiços"));
        assertEquals(1, occurrences(source, "LoadoutNetworkBridge.requestUpdate("));
    }

    @Test
    void searchFocusOwnsEditingKeysWhileEnterAndEscapeContractsRemainDeliberate() throws Exception {
        String source = Files.readString(SCREEN);
        int enter = source.indexOf("keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER");
        int tab = source.indexOf("keyCode == GLFW.GLFW_KEY_TAB");
        int focusedGuard = source.indexOf("searchBox != null && searchBox.isFocused()");
        int clear = source.indexOf("keyCode == GLFW.GLFW_KEY_BACKSPACE || keyCode == GLFW.GLFW_KEY_DELETE");
        int reset = source.indexOf("keyCode == GLFW.GLFW_KEY_R");

        assertTrue(tab >= 0, "Tab must provide a keyboard path into/out of search");
        assertTrue(enter >= 0 && enter < focusedGuard, "Enter must remain Apply even while search owns focus");
        assertTrue(focusedGuard >= 0 && focusedGuard < clear,
                "search focus must intercept Backspace/Delete before draft Clear");
        assertTrue(focusedGuard < reset, "typing R in search must not reset the draft");
        assertTrue(source.contains("setFocused(searchBox);"));
        assertTrue(source.contains("setFocused(null);"));
        assertTrue(source.contains("return super.keyPressed(keyCode, scanCode, modifiers);"));
        assertTrue(source.contains("return super.keyPressed(keyCode, scanCode, modifiers);"),
                "Escape must continue through Screen when search owns focus");
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
