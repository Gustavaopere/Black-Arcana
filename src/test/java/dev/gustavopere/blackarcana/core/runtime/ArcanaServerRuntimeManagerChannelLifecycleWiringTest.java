package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeManagerChannelLifecycleWiringTest {
    private static final Path MANAGER_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java");

    @Test
    void trustedServerLifecycleInterruptionsCancelCasterChannels() throws IOException {
        String normalized = Files.readString(MANAGER_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains(
                "gameBus.addListener(ArcanaServerRuntimeManager::onPlayerLoggedOut);"),
                "logout must cancel server-owned channel state without trusting a client packet");
        assertTrue(normalized.contains(
                "gameBus.addListener(ArcanaServerRuntimeManager::onPlayerChangedDimension);"),
                "dimension transfer must interrupt the previous channel session");
        assertTrue(normalized.contains(
                "private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event)"));
        assertTrue(normalized.contains(
                "private static void onPlayerChangedDimension(PlayerEvent.PlayerChangedDimensionEvent event)"));
        assertTrue(normalized.contains("runtime.channels().cancelCaster(player.getUUID())"),
                "lifecycle handlers must cancel canonical runtime-owned state by trusted server identity");
        assertTrue(normalized.contains("if (!player.isAlive())"),
                "server tick must settle actual dead-player channel interruption after resurrection listeners finish");
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
