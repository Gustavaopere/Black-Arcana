package dev.gustavopere.blackarcana.ci;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Stage07SpacePlayerTeleportContractTest {
    private static final Path REPOSITORY_ROOT = repositoryRoot();

    @Test
    void thresholdGateUsesTeleportContractInsteadOfRawPositionMutation() throws IOException {
        String source = Files.readString(REPOSITORY_ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftThresholdGateRuntime.java"));

        assertTrue(source.contains("living.teleportTo(destination.x(), destination.y(), destination.z())"),
            "Threshold Gate must use Entity/ServerPlayer teleportTo so player settlement reaches the player-specific teleport path");
        assertFalse(source.contains("living.setPos(destination.x(), destination.y(), destination.z())"),
            "Threshold Gate must not bypass the ServerPlayer teleport override with raw setPos");
    }

    @Test
    void reciprocalTranspositionUsesTeleportContractForSettlementAndRollback() throws IOException {
        String source = Files.readString(REPOSITORY_ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftReciprocalTranspositionRuntime.java"));

        assertTrue(source.contains("first.entity().teleportTo(secondPosition.x(), secondPosition.y(), secondPosition.z())"),
            "Reciprocal Transposition must settle the first endpoint through the teleport contract");
        assertTrue(source.contains("second.entity().teleportTo(firstPosition.x(), firstPosition.y(), firstPosition.z())"),
            "Reciprocal Transposition must settle the second endpoint through the teleport contract");
        assertFalse(source.contains("first.entity().setPos("),
            "Reciprocal Transposition must not bypass player teleport handling for the first endpoint");
        assertFalse(source.contains("second.entity().setPos("),
            "Reciprocal Transposition must not bypass player teleport handling for the second endpoint");
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
