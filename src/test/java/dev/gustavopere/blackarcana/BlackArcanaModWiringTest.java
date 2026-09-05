package dev.gustavopere.blackarcana;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class BlackArcanaModWiringTest {
    private static final Path MOD_SOURCE = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java");

    @Test
    void spaceDisplacementLifecycleRuntimesAreRegisteredOnGameBus() throws IOException {
        String source = Files.readString(MOD_SOURCE);
        assertRegistered(source, "MinecraftThresholdGateRuntime");
        assertRegistered(source, "MinecraftVeilstepReflexRuntime");
        assertRegistered(source, "MinecraftAnchorRecallRuntime");
        assertRegistered(source, "MinecraftReciprocalTranspositionRuntime");
    }

    private static void assertRegistered(String source, String runtime) {
        assertTrue(
            source.contains("import dev.gustavopere.blackarcana.integration.neoforge." + runtime + ";"),
            runtime + " must be imported by the Black Arcana composition root");
        assertTrue(
            source.contains(runtime + ".register(NeoForge.EVENT_BUS);"),
            runtime + " must register its lifecycle listeners on NeoForge.EVENT_BUS");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }

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
