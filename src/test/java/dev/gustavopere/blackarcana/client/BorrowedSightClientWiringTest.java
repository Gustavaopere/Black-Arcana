package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BorrowedSightClientWiringTest {
    private static final Path CLIENT_ENTRYPOINT = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path CONTROLLER = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/BorrowedSightClientController.java");

    @Test
    void physicalClientInstallsServerAuthoredBorrowedSightCameraHandler() throws IOException {
        String entrypoint = Files.readString(CLIENT_ENTRYPOINT);
        assertTrue(entrypoint.contains("NoeticViewNetworkBridge.installClientHandler(BorrowedSightClientController::accept);"),
                "physical client must install the Borrowed Sight clientbound handler");
        assertTrue(entrypoint.contains("BorrowedSightClientController.register(NeoForge.EVENT_BUS);"),
                "physical client must register Borrowed Sight lifecycle restoration");
    }

    @Test
    void controllerUsesOnlyLoadedClientEntityAndRestoresPhysicalBody() throws IOException {
        String source = Files.readString(CONTROLLER);
        assertTrue(source.contains("ClientTickEvent.Post"),
                "Borrowed Sight camera ownership must be reconciled on the physical client tick");
        assertTrue(source.contains("minecraft.level.getEntity(targetEntityId)"),
                "Borrowed Sight must resolve only an already-loaded client entity by server-authored entity id");
        assertTrue(source.contains("minecraft.setCameraEntity(target)"),
                "Borrowed Sight BEGIN must move only the physical camera to the validated target");
        assertTrue(source.contains("minecraft.setCameraEntity(minecraft.player)"),
                "Borrowed Sight END/target loss must restore the camera to the player's physical body");
        assertFalse(source.contains("PacketDistributor"),
                "physical camera presentation must not create a client-authoritative gameplay packet path");
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
