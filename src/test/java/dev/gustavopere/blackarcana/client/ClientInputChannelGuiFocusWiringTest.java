package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientInputChannelGuiFocusWiringTest {
    private static final Path INPUT_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");

    @Test
    void guiFocusCancelsActiveChannelBeforeReleaseCanExecuteGameplay() throws IOException {
        String source = Files.readString(INPUT_SOURCE).replaceAll("\\s+", " ");

        assertTrue(source.contains("ChannelCancelIntentPayload"),
                "GUI focus cancellation must use the existing bounded channel cancel payload");
        assertTrue(source.contains("CHANNELS.cancel().ifPresent(castId ->"),
                "GUI focus must clear the exact local active channel session");
        assertTrue(source.contains("ChannelNetworkBridge.requestCancel(new ChannelCancelIntentPayload("),
                "GUI focus must cancel the matching server-owned channel instead of releasing it");

        int guiFocus = source.indexOf("else if (minecraft.screen != null)");
        int cancel = source.indexOf("CHANNELS.cancel().ifPresent(castId ->", guiFocus);
        int release = source.indexOf("processChannelRelease(minecraft)", guiFocus);
        assertTrue(guiFocus >= 0 && cancel > guiFocus && release > cancel,
                "GUI-focus cancellation must happen before channel release processing in the client tick");
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
