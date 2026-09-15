package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientInputDisconnectCleanupWiringTest {
    private static final Path CONTROLLER_SOURCE = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");

    @Test
    void disconnectCleanupReturnsBeforeDereferencingPlayerAgain() throws IOException {
        String normalized = Files.readString(CONTROLLER_SOURCE).replaceAll("\\s+", " ");

        assertTrue(
            normalized.contains(
                "DiscoverabilityClientRuntime.clearSession(); return; } ResourceKey<Level> currentDimension = minecraft.player.level().dimension();"),
            "disconnect cleanup must return before the tick path dereferences minecraft.player again");
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
