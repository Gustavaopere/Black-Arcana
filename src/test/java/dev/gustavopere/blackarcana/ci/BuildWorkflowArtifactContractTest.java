package dev.gustavopere.blackarcana.ci;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class BuildWorkflowArtifactContractTest {
    private static final Path WORKFLOW = Path.of(".github/workflows/build.yml");

    @Test
    void publishesValidatedMainJarAsShortLivedQaArtifact() throws IOException {
        String workflow = Files.readString(WORKFLOW);

        int jarVerification = workflow.indexOf("- name: Verify built JAR");
        int dedicatedSmoke = workflow.indexOf("- name: Dedicated-server smoke test");
        int artifactUpload = workflow.indexOf("uses: actions/upload-artifact@v4");

        assertTrue(jarVerification >= 0, "workflow must retain built-JAR verification");
        assertTrue(dedicatedSmoke > jarVerification, "dedicated-server smoke must remain after JAR verification");
        assertTrue(artifactUpload > dedicatedSmoke, "QA artifact must be published only after the full runtime gate");
        assertTrue(workflow.contains("if: github.ref == 'refs/heads/main'"), "canonical QA artifact must be main-only");
        assertTrue(workflow.contains("name: black-arcana-${{ github.sha }}"), "artifact name must identify the exact commit SHA");
        assertTrue(workflow.contains("path: build/libs/black_arcana-*.jar"), "artifact must contain the built Black Arcana JAR");
        assertTrue(workflow.contains("if-no-files-found: error"), "missing verified JAR must fail artifact publication");
        assertTrue(workflow.contains("retention-days: 7"), "QA artifact retention must remain short-lived");
    }
}
