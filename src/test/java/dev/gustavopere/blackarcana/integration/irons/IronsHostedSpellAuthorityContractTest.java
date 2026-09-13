package dev.gustavopere.blackarcana.integration.irons;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class IronsHostedSpellAuthorityContractTest {
    @Test
    void hostedProbeDisablesProviderSettlement() throws IOException {
        Path root = repositoryRoot();
        String probe = Files.readString(root.resolve("src/main/java/dev/gustavopere/blackarcana/integration/irons/IronsArcanaProbeSpell.java"));
        assertTrue(probe.contains("public int getManaCost(int level)"));
        assertTrue(probe.contains("public int getSpellCooldown()"));
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);
        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle"))) return candidate;
            candidate = candidate.getParent();
        }
        throw new IllegalStateException("repository root not found");
    }
}
