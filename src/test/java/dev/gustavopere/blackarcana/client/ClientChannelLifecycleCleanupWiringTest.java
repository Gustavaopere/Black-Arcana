package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientChannelLifecycleCleanupWiringTest {
    private static final Path INPUT_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");

    @Test
    void deathAndDimensionTransitionsDropStaleLocalChannelIdentity() throws IOException {
        String normalized = Files.readString(INPUT_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains(
                "if (!minecraft.player.isAlive() || dimensionChanged) { CHANNELS.cancel();"),
                "trusted server lifecycle will cancel the session; client must drop its stale exact cast identity too");
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
