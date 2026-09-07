package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeManagerLoadoutWiringTest {
    private static final Path MANAGER_SOURCE = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java");

    @Test
    void loadoutUpdateRequiresAnInstalledExecutionEngine() throws IOException {
        String normalized = Files.readString(MANAGER_SOURCE).replaceAll("\\s+", " ");

        assertTrue(
            normalized.contains(
                "new LoadoutUpdateService( runtime.spells(), runtime.loadouts(), runtime::hasInstalledEngine)"),
            "LoadoutUpdateService must receive installed execution-engine authority, not registry presence alone");
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
