package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ChannelBeginResultClientWiringTest {
    private static final Path MOD_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java");

    @Test
    void modRoutesValidatedBeginAcknowledgementIntoClientSyncState() throws IOException {
        String normalized = Files.readString(MOD_SOURCE).replaceAll("\\s+", " ");
        assertTrue(normalized.contains(
                "ChannelNetworkBridge.installBeginResultHandler(ClientArcanaSyncState::acceptChannelBeginResult);"));
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
