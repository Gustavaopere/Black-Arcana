package dev.gustavopere.blackarcana.ci;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class Stage07SpaceRuntimeBootstrapContractTest {
    private static final Path MOD_ENTRYPOINT = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java");

    @Test
    void registersEveryStatefulSpaceRuntimeOnTheNeoForgeGameBus() throws IOException {
        String source = Files.readString(MOD_ENTRYPOINT);

        assertTrue(source.contains("MinecraftThresholdGateRuntime.register(NeoForge.EVENT_BUS);"),
            "Threshold Gate runtime must register server-stop cleanup on the live game bus");
        assertTrue(source.contains("MinecraftVeilstepReflexRuntime.register(NeoForge.EVENT_BUS);"),
            "Veilstep Reflex runtime must register logout/server-stop cleanup on the live game bus");
        assertTrue(source.contains("MinecraftAnchorRecallRuntime.register(NeoForge.EVENT_BUS);"),
            "Anchor Recall runtime must register logout/server-stop cleanup on the live game bus");
        assertTrue(source.contains("MinecraftReciprocalTranspositionRuntime.register(NeoForge.EVENT_BUS);"),
            "Reciprocal Transposition runtime must register server-stop cleanup on the live game bus");
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
