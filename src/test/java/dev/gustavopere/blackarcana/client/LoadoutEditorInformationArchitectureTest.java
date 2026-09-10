package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class LoadoutEditorInformationArchitectureTest {
    private static final Path LOADOUT_SCREEN = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path EN_US = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/en_us.json");
    private static final Path PT_BR = repositoryRoot().resolve(
            "src/main/resources/assets/black_arcana/lang/pt_br.json");

    @Test
    void configuredSpellExposesDenseOneBasedSlotPosition() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");

        Object position = slotPosition(List.of(a, b, c), b).orElseThrow();

        assertEquals(2, invokeInt(position, "slotNumber"));
        assertTrue(invokeBoolean(position, "quickCastEligible"));
        assertEquals(2, invokeInt(position, "quickCastSlot"));
    }

    @Test
    void firstEightPositionsAreQuickCastEligibleButNinthIsNot() {
        List<ArcanaSpellId> draft = new ArrayList<>();
        for (int index = 0; index < 9; index++) {
            draft.add(spell("spell_" + index));
        }

        Object eighth = slotPosition(draft, draft.get(7)).orElseThrow();
        Object ninth = slotPosition(draft, draft.get(8)).orElseThrow();

        assertEquals(8, invokeInt(eighth, "slotNumber"));
        assertTrue(invokeBoolean(eighth, "quickCastEligible"));
        assertEquals(8, invokeInt(eighth, "quickCastSlot"));
        assertEquals(9, invokeInt(ninth, "slotNumber"));
        assertFalse(invokeBoolean(ninth, "quickCastEligible"));
        assertEquals(-1, invokeInt(ninth, "quickCastSlot"));
    }

    @Test
    void catalogSpellOutsideDraftHasNoConfiguredSlot() {
        ArcanaSpellId configured = spell("configured");
        ArcanaSpellId catalogOnly = spell("catalog_only");

        assertTrue(slotPosition(List.of(configured), catalogOnly).isEmpty());
    }

    @Test
    void loadoutScreenWiresSlotSemanticsWithoutPretendingQuickCastIsBound() throws Exception {
        String screen = Files.readString(LOADOUT_SCREEN);
        String english = Files.readString(EN_US);
        String portuguese = Files.readString(PT_BR);

        assertTrue(screen.contains("LoadoutEditorSemantics.slotPosition("));
        assertTrue(screen.contains("screen.black_arcana.loadout.slot"));
        assertTrue(screen.contains("screen.black_arcana.loadout.slot.quick_eligible"));
        assertTrue(english.contains("QC%s eligible"), "English cue must describe eligibility, not a binding");
        assertTrue(portuguese.contains("QC%s elegível"), "Portuguese cue must describe eligibility, not a binding");
        assertFalse(english.contains("Press 1-8"));
        assertFalse(portuguese.contains("Pressione 1-8"));
    }

    @SuppressWarnings("unchecked")
    private static Optional<Object> slotPosition(List<ArcanaSpellId> draft, ArcanaSpellId spell) {
        try {
            Class<?> semantics = Class.forName("dev.gustavopere.blackarcana.client.LoadoutEditorSemantics");
            Method method = semantics.getDeclaredMethod("slotPosition", List.class, ArcanaSpellId.class);
            return (Optional<Object>) method.invoke(null, draft, spell);
        } catch (ClassNotFoundException exception) {
            return fail("LoadoutEditorSemantics is missing", exception);
        } catch (ReflectiveOperationException exception) {
            return fail("LoadoutEditorSemantics.slotPosition(List, ArcanaSpellId) is missing or invalid", exception);
        }
    }

    private static int invokeInt(Object target, String methodName) {
        try {
            return (int) target.getClass().getDeclaredMethod(methodName).invoke(target);
        } catch (ReflectiveOperationException exception) {
            return fail("Missing slot-position integer accessor: " + methodName, exception);
        }
    }

    private static boolean invokeBoolean(Object target, String methodName) {
        try {
            return (boolean) target.getClass().getDeclaredMethod(methodName).invoke(target);
        } catch (ReflectiveOperationException exception) {
            return fail("Missing slot-position boolean accessor: " + methodName, exception);
        }
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
