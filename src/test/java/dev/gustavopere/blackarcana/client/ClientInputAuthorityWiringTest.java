package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientInputAuthorityWiringTest {
    private static final Path INPUT_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");
    private static final Path KEYMAP_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaKeyMappings.java");

    @Test
    void gameplayInputFailsClosedWhileAnotherGuiOwnsFocus() throws IOException {
        String source = normalized(INPUT_SOURCE);
        String directCast = between(source, "public static boolean castSlot(int slot)", "private static void sendImmediateCast");
        String physicalCast = between(source, "private static boolean castSlotFromInput", "private static void processChannelBeginAcknowledgement");

        assertTrue(directCast.contains("minecraft.screen != null) return false"),
                "programmatic immediate casts must fail closed while a GUI owns focus");
        assertTrue(physicalCast.contains("minecraft.screen != null) return false"),
                "physical cast dispatch must fail closed while a GUI owns focus");
        assertTrue(source.contains("if (minecraft.screen == null && !loadout.isEmpty()) { radialOpener.run(); }"),
                "radial opening must not steal input from another GUI");
        assertTrue(source.contains("if (minecraft.screen == null) { loadoutEditorOpener.run(); }"),
                "loadout-editor opening must not steal input from another GUI");
        assertTrue(source.contains("if (minecraft.screen == null) { castSlotFromInput(SELECTION.selectedSlot(), CAST_SELECTED_INPUT_ID); }"),
                "selected-cast input must be suppressed while another GUI owns focus");
        assertTrue(source.contains("if (minecraft.screen == null) { castSlotFromInput(index, QUICK_CAST_INPUT_ID_BASE + index); }"),
                "quick-cast input must be suppressed while another GUI owns focus");
        assertTrue(source.contains("SELECTION.reconcile(loadout)"),
                "client selection must continue reconciling against the synchronized server snapshot");
    }

    @Test
    void requiredOperationsUseOrdinaryRebindableMinecraftKeyMappingsWithSafeDefaults() throws IOException {
        String source = normalized(KEYMAP_SOURCE);

        assertTrue(source.contains("public static final KeyMapping OPEN_RADIAL = new KeyMapping("),
                "radial input must use ordinary Minecraft KeyMapping registration");
        assertTrue(source.contains("key.black_arcana.open_radial\", GLFW.GLFW_KEY_R, CATEGORY"),
                "radial default must remain R");
        assertTrue(source.contains("public static final KeyMapping CAST_SELECTED = new KeyMapping("),
                "selected cast must use ordinary Minecraft KeyMapping registration");
        assertTrue(source.contains("key.black_arcana.cast_selected\", GLFW.GLFW_KEY_V, CATEGORY"),
                "selected-cast default must remain V");
        assertTrue(source.contains("key.black_arcana.edit_loadout\", GLFW.GLFW_KEY_UNKNOWN, CATEGORY"),
                "loadout editor must default to unbound");
        assertTrue(source.contains("public static final KeyMapping[] QUICK_CAST = new KeyMapping[8]"),
                "exactly eight direct quick-cast convenience mappings are allowed");
        assertTrue(source.contains("key.black_arcana.quick_cast_\" + (index + 1), GLFW.GLFW_KEY_UNKNOWN, CATEGORY"),
                "quick-cast convenience mappings must default to unbound");
        assertTrue(source.contains("event.register(OPEN_RADIAL)"));
        assertTrue(source.contains("event.register(CAST_SELECTED)"));
        assertTrue(source.contains("event.register(EDIT_LOADOUT)"));
        assertTrue(source.contains("for (KeyMapping mapping : QUICK_CAST) event.register(mapping)"));
    }

    private static String normalized(Path source) throws IOException {
        return Files.readString(source).replaceAll("\\s+", " ");
    }

    private static String between(String source, String startMarker, String endMarker) {
        int start = source.indexOf(startMarker);
        int end = source.indexOf(endMarker, start + startMarker.length());
        if (start < 0 || end < 0 || end <= start) {
            throw new AssertionError("Could not isolate source region between " + startMarker + " and " + endMarker);
        }
        return source.substring(start, end);
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
        throw new IllegalStateException("Unable to locate repository root from test working directory");
    }
}
