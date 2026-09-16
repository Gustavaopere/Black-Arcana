package dev.gustavopere.blackarcana.client;

import com.electronwill.nightconfig.core.CommentedConfig;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientConfigAuthorityContractTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path CONFIG_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClientConfig.java");
    private static final Path CLIENT_ENTRYPOINT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path INPUT_CONTROLLER = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");
    private static final Path NETWORK_ROOT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/network");

    @Test
    void canonicalOptionsKeepDocumentedDefaultsBoundsAndEnums() throws IOException {
        String source = normalized(CONFIG_SOURCE);

        assertTrue(source.contains("enum RadialBehavior { TOGGLE, HOLD }"));
        assertTrue(source.contains("enum FeedbackLevel { MINIMAL, STANDARD, VERBOSE }"));
        assertTrue(source.contains("define(\"contextualHud\", true)"));
        assertTrue(source.contains("define(\"discoverabilityHints\", true)"));
        assertTrue(source.contains("defineInRange(\"hudScale\", 1.0D, 0.5D, 2.0D)"));
        assertTrue(source.contains("defineEnum(\"hudAnchor\", HudLayout.Anchor.BOTTOM_CENTER)"));
        assertTrue(source.contains("defineInRange(\"selectionDurationTicks\", 60, 0, 400)"));
        assertTrue(source.contains("defineInRange(\"feedbackDurationTicks\", 80, 0, 400)"));
        assertTrue(source.contains("defineEnum(\"feedbackLevel\", FeedbackLevel.STANDARD)"));
        assertTrue(source.contains("defineEnum(\"radialBehavior\", RadialBehavior.TOGGLE)"));
        assertTrue(source.contains("defineInRange(\"particleDensity\", 1.0D, 0.0D, 1.0D)"));
        assertTrue(source.contains("define(\"reducedMotion\", false)"));
        assertTrue(source.contains("define(\"reducedFlashes\", false)"));
    }

    @Test
    void modConfigSpecPreservesValidPreferencesAndRecoversInvalidOrMissingDefaults() {
        CommentedConfig config = CommentedConfig.inMemory();
        config.set("contextualHud", false);
        config.set("hudScale", 1.5D);
        config.set("selectionDurationTicks", 120);
        config.set("feedbackDurationTicks", -1);
        config.set("feedbackLevel", "VERBOSE");
        config.set("radialBehavior", "HOLD");
        config.set("particleDensity", 2.0D);
        config.set("reducedMotion", true);

        assertFalse(BlackArcanaClientConfig.SPEC.isCorrect(config),
                "missing and out-of-range values must require NeoForge config correction");

        BlackArcanaClientConfig.SPEC.correct(config);

        assertTrue(BlackArcanaClientConfig.SPEC.isCorrect(config),
                "NeoForge config correction must restore the document to the registered spec");
        assertEquals(false, config.get("contextualHud"),
                "valid customized client preferences must survive correction");
        assertEquals(true, config.get("discoverabilityHints"),
                "missing booleans must recover to the registered default");
        assertEquals(1.5D, ((Number) config.get("hudScale")).doubleValue(), 0.0D,
                "valid bounded values must survive correction");
        assertEquals(HudLayout.Anchor.BOTTOM_CENTER, config.get("hudAnchor"),
                "missing enum values must recover to the registered default");
        assertEquals(120, ((Number) config.get("selectionDurationTicks")).intValue(),
                "valid duration values must survive correction");
        assertEquals(80, ((Number) config.get("feedbackDurationTicks")).intValue(),
                "invalid duration values must recover to the registered default");
        assertEquals("VERBOSE", config.get("feedbackLevel"),
                "valid serialized enum preferences must survive correction");
        assertEquals("HOLD", config.get("radialBehavior"),
                "valid serialized radial behavior must survive correction");
        assertEquals(1.0D, ((Number) config.get("particleDensity")).doubleValue(), 0.0D,
                "out-of-range particle density must recover to the registered default");
        assertEquals(true, config.get("reducedMotion"),
                "valid accessibility preferences must survive correction");
        assertEquals(false, config.get("reducedFlashes"),
                "missing accessibility preferences must recover to the registered default");
    }

    @Test
    void preferencesAreRegisteredOnlyThroughThePhysicalClientEntrypoint() throws IOException {
        String source = normalized(CLIENT_ENTRYPOINT);

        assertTrue(source.contains("@Mod(value = BlackArcanaMod.MOD_ID, dist = Dist.CLIENT)"),
                "the config owner must remain a physical-client-only entrypoint");
        assertTrue(source.contains("container.registerConfig(ModConfig.Type.CLIENT, BlackArcanaClientConfig.SPEC)"),
                "Black Arcana preferences must remain NeoForge CLIENT config");
    }

    @Test
    void presentationPreferencesCannotEnterGameplayIntentOrNetworkAuthorityCode() throws IOException {
        String input = Files.readString(INPUT_CONTROLLER);
        assertTrue(!input.contains("BlackArcanaClientConfig"),
                "cast/channel intent emission must not derive gameplay fields from client preferences");

        List<Path> leaks;
        try (var files = Files.walk(NETWORK_ROOT)) {
            leaks = files
                    .filter(Files::isRegularFile)
                    .filter(path -> path.toString().endsWith(".java"))
                    .filter(path -> contains(path, "BlackArcanaClientConfig"))
                    .toList();
        }
        assertTrue(leaks.isEmpty(),
                () -> "client presentation config leaked into network/server-authority code: " + leaks);
    }

    private static boolean contains(Path path, String needle) {
        try {
            return Files.readString(path).contains(needle);
        } catch (IOException failure) {
            throw new IllegalStateException("Unable to inspect " + path, failure);
        }
    }

    private static String normalized(Path source) throws IOException {
        return Files.readString(source).replaceAll("\\s+", " ");
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
