package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeManagerLoadoutWiringTest {
    private static final Path MANAGER_SOURCE = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java");

    @Test
    void loadoutUpdateRequiresAnInstalledExecutionEngine() throws IOException {
        String normalized = source();

        assertTrue(
            normalized.contains(
                "new LoadoutUpdateService( runtime.spells(), runtime.loadouts(), runtime::hasInstalledEngine)"),
            "LoadoutUpdateService must receive installed execution-engine authority, not registry presence alone");
    }

    @Test
    void acceptedLoadoutUpdateIsPersistedBeforeReturningSnapshot() throws IOException {
        String normalized = source();

        assertTrue(
            normalized.contains(
                "LoadoutUpdateService.Result result = service.apply(player.getUUID(), update.parsedSpellIds()); if (result.decision().allowed()) persist(server, server.overworld().getGameTime()); return new LoadoutSnapshotPayload("),
            "accepted loadout updates, including clear, must persist before the authoritative snapshot is returned");
    }

    @Test
    void playerLoginAlwaysResendsAuthoritativeLoadoutSnapshot() throws IOException {
        String normalized = source();

        assertTrue(
            normalized.contains(
                "private static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event)"),
            "runtime manager must own an explicit player-login synchronization path");
        assertTrue(
            normalized.contains("LoadoutNetworkBridge.sendSnapshot(player, loadoutSnapshot(runtime, player));"),
            "player login must resend the server-owned loadout instead of trusting stale client state");
    }

    private static String source() throws IOException {
        return Files.readString(MANAGER_SOURCE).replaceAll("\\s+", " ");
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
