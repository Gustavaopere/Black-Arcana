package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceClientWiringTest {
    private static final Path CLIENT_ENTRYPOINT = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path CAMERA_CONTROLLER = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientController.java");
    private static final Path INPUT_CONTROLLER = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceInputController.java");

    @Test
    void physicalClientInstallsServerAuthoredAstralCameraAndInputHandlers() throws IOException {
        String entrypoint = Files.readString(CLIENT_ENTRYPOINT);
        assertTrue(entrypoint.contains(
                        "AstralSeveranceNetworkBridge.installViewHandler(AstralSeveranceClientController::accept);"),
                "physical client must install the Astral clientbound presentation handler");
        assertTrue(entrypoint.contains("AstralSeveranceClientController.register(NeoForge.EVENT_BUS);"),
                "physical client must register Astral camera lifecycle restoration");
        assertTrue(entrypoint.contains("AstralSeveranceInputController.register(NeoForge.EVENT_BUS);"),
                "movement redirection must be registered as a separate client-only controller");
    }

    @Test
    void cameraControllerUsesOnlyExactLoadedProjectionAndRestoresPhysicalBody() throws IOException {
        String source = Files.readString(CAMERA_CONTROLLER);
        assertTrue(source.contains("ClientTickEvent.Post"),
                "Astral camera ownership must be reconciled on the physical client tick");
        assertTrue(source.contains("minecraft.level.getEntity(desired.entityId())"),
                "Astral view must resolve only an already-loaded client entity by server-authored runtime id");
        assertTrue(source.contains("target instanceof AstralProjectionEntity"),
                "Astral camera target must be the dedicated non-owning projection representation");
        assertTrue(source.contains("target.getUUID().equals(desired.projectionId())"),
                "runtime entity id must be verified against exact server-authored projection UUID");
        assertTrue(source.contains("minecraft.setCameraEntity(target)"),
                "validated BEGIN must move only the camera to the Astral representation");
        assertTrue(source.contains("minecraft.setCameraEntity(minecraft.player)"),
                "END or unavailable representation must restore the physical body camera");
        assertFalse(source.contains("PacketDistributor"),
                "camera presentation must not create a client-authoritative gameplay path");
        assertFalse(source.contains("sendMove("),
                "camera presentation must stay separate from movement intent transport");
    }

    @Test
    void movementControllerUsesLogicalClientInputEventAndExactServerArming() throws IOException {
        String source = Files.readString(INPUT_CONTROLLER);
        assertTrue(source.contains("MovementInputUpdateEvent"),
                "movement capture must use the NeoForge logical-client movement-input seam");
        assertTrue(source.contains("AstralSeveranceClientController.movementControl()"),
                "movement must remain dormant until the exact server-authored Astral session is armed");
        assertTrue(source.contains("AstralSeveranceNetworkBridge.sendMove(payload)"),
                "the movement controller may send only bounded intent through the existing C2S bridge");
        assertTrue(source.contains("input.leftImpulse = 0.0F"));
        assertTrue(source.contains("input.forwardImpulse = 0.0F"));
        assertTrue(source.contains("input.jumping = false"));
        assertTrue(source.contains("input.shiftKeyDown = false"));
        assertFalse(source.contains("setPos("),
                "client input redirection must never author an Astral world position");
        assertFalse(source.contains("moveTo("),
                "client input redirection must never author an Astral world position");
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
