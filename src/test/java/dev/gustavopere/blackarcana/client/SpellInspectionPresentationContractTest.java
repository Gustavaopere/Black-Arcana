package dev.gustavopere.blackarcana.client;

import net.minecraft.network.chat.Component;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class SpellInspectionPresentationContractTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path LOADOUT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path RADIAL = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaRadialScreen.java");
    private static final Path EN_US = ROOT.resolve(
            "src/main/resources/assets/black_arcana/lang/en_us.json");
    private static final Path PT_BR = ROOT.resolve(
            "src/main/resources/assets/black_arcana/lang/pt_br.json");

    @Test
    void inspectionLinesExposeOnlyStaticIdentityAndOptionalExistingHazard() throws Exception {
        Class<?> helper = Class.forName("dev.gustavopere.blackarcana.client.SpellInspectionPresentation");
        Method lines = helper.getDeclaredMethod(
                "lines", String.class, Component.class, Component.class);
        lines.setAccessible(true);

        Component name = Component.literal("Probe Spell");
        Component hazard = Component.literal("Danger: unstable");

        @SuppressWarnings("unchecked")
        List<Component> withHazard = (List<Component>) lines.invoke(
                null, "black_arcana:probe_spell", name, hazard);
        assertEquals(3, withHazard.size());
        assertEquals("Probe Spell", withHazard.get(0).getString());
        assertTrue(withHazard.get(1).getString().contains("black_arcana:probe_spell"));
        assertEquals("Danger: unstable", withHazard.get(2).getString());

        @SuppressWarnings("unchecked")
        List<Component> withoutHazard = (List<Component>) lines.invoke(
                null, "black_arcana:probe_spell", name, null);
        assertEquals(2, withoutHazard.size());
        assertEquals("Probe Spell", withoutHazard.get(0).getString());
        assertTrue(withoutHazard.get(1).getString().contains("black_arcana:probe_spell"));
    }

    @Test
    void loadoutUsesOneInspectionTooltipForPointerAndKeyboardFocus() throws Exception {
        String loadout = Files.readString(LOADOUT);

        assertTrue(loadout.contains("SpellInspectionPresentation.lines("));
        assertTrue(loadout.contains("graphics.renderComponentTooltip("));
        assertTrue(loadout.contains("presentation.get(spell)"));
        assertTrue(loadout.contains("hazards.get(spell)"));
        assertFalse(loadout.contains("SpellInspectionNetwork"));
        assertEquals(1, occurrences(loadout, "LoadoutNetworkBridge.requestUpdate("));
    }

    @Test
    void radialAndHudAreNotExpandedIntoRichInspectionSurfaces() throws Exception {
        String radial = Files.readString(RADIAL);
        assertFalse(radial.contains("SpellInspectionPresentation"));
        assertFalse(radial.contains("screen.black_arcana.inspect.id"));
    }

    @Test
    void identityLabelIsLocalizedWithoutAddingGuessedDetailFields() throws Exception {
        String en = Files.readString(EN_US);
        String pt = Files.readString(PT_BR);
        String loadout = Files.readString(LOADOUT);

        assertTrue(en.contains("\"screen.black_arcana.inspect.id\""));
        assertTrue(pt.contains("\"screen.black_arcana.inspect.id\""));
        assertFalse(loadout.contains("ArcanaCost"));
        assertFalse(loadout.contains("ArcanaTargetSpec"));
        assertFalse(loadout.contains("cooldownGroup"));
        assertFalse(loadout.contains("providerId"));
        assertFalse(loadout.contains("domainId"));
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
