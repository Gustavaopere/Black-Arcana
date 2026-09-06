package dev.gustavopere.blackarcana.integration.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftNoeticRuntimeWiringTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticRuntime.java");

    @Test
    void stillnessMovementUsesEntityPreAndPostHooksInsteadOfOnlyServerPostTick() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        assertTrue(source.contains("EntityTickEvent.Pre"),
                "Stillness must have a pre-entity-tick hook so packet/previous-tick drift is corrected before entity work");
        assertTrue(source.contains("EntityTickEvent.Post"),
                "Stillness must have a post-entity-tick hook so travel during the entity tick cannot accumulate");
        assertTrue(source.contains("enforceStillnessBeforeEntityTick"),
                "Pre hook must delegate to the gaze runtime movement lock");
        assertTrue(source.contains("enforceStillnessAfterEntityTick"),
                "Post hook must delegate to the gaze runtime movement lock");
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
