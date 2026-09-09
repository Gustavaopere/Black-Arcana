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

class LoadoutDraftResetTest {
    private static final Path LOADOUT_SCREEN = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path EN_US = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/en_us.json");
    private static final Path PT_BR = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/pt_br.json");

    @Test
    void openingDraftStartsCleanAndToggleMakesItDirty() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        LoadoutDraft draft = new LoadoutDraft(List.of(a));

        assertFalse(isDirty(draft));
        assertTrue(draft.toggle(b));
        assertTrue(isDirty(draft));
    }

    @Test
    void reorderAndClearMarkDirtyAgainstNonEmptyOpeningBaseline() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        assertTrue(draft.move(0, 2));
        assertTrue(isDirty(draft));

        reset(draft);
        assertFalse(isDirty(draft));
        draft.clear();
        assertTrue(isDirty(draft));
    }

    @Test
    void resetRestoresExactOpeningOrderAndReturnsToClean() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        ArcanaSpellId d = spell("d");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        assertTrue(draft.move(2, 0));
        assertTrue(draft.toggle(b));
        assertTrue(draft.toggle(d));
        assertTrue(isDirty(draft));

        reset(draft);

        assertEquals(List.of(a, b, c), draft.snapshot());
        assertFalse(isDirty(draft));
    }

    @Test
    void loadoutScreenExposesResetAsLocalActionOnly() throws Exception {
        String screen = Files.readString(LOADOUT_SCREEN);
        String english = Files.readString(EN_US);
        String portuguese = Files.readString(PT_BR);

        assertTrue(screen.contains("keyCode == GLFW.GLFW_KEY_R"));
        assertTrue(screen.contains("draft.reset();"));
        assertEquals(1, occurrences(screen, "LoadoutNetworkBridge.requestUpdate("),
                "Apply must remain the only loadout-update request site in this screen");
        assertTrue(english.contains("R: reset"));
        assertTrue(portuguese.contains("R: restaurar"));
    }

    private static boolean isDirty(LoadoutDraft draft) {
        try {
            Method method = LoadoutDraft.class.getDeclaredMethod("isDirty");
            return (boolean) method.invoke(draft);
        } catch (ReflectiveOperationException exception) {
            return fail("LoadoutDraft.isDirty() is missing or invalid", exception);
        }
    }

    private static void reset(LoadoutDraft draft) {
        try {
            Method method = LoadoutDraft.class.getDeclaredMethod("reset");
            method.invoke(draft);
        } catch (ReflectiveOperationException exception) {
            fail("LoadoutDraft.reset() is missing or invalid", exception);
        }
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

    private static ArcanaSpellId spell(String path) {
        return ArcanaSpellId.parse("black_arcana:" + path);
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
