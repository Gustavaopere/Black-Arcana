package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class CameraPresentationOwnershipWiringTest {
    @Test
    void cameraControllersRestoreOnlyTheEntityTheyActuallyOwn() throws IOException {
        assertOwnershipSafe("BorrowedSightClientController.java");
        assertOwnershipSafe("AstralSeveranceClientController.java");
    }

    private static void assertOwnershipSafe(String fileName) throws IOException {
        String source = Files.readString(repositoryRoot()
                .resolve("src/main/java/dev/gustavopere/blackarcana/client")
                .resolve(fileName));
        assertTrue(source.contains("ownedCameraEntity"), fileName + " must remember its concrete camera claim");
        assertTrue(source.contains("minecraft.getCameraEntity() == ownedCameraEntity"),
                fileName + " must not restore over another presentation controller's newer camera claim");
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
