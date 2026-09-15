package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientInputDisconnectSelectionWiringTest {
    private static final Path INPUT_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");

    @Test
    void disconnectClearsLocalSelectionBeforeReturningFromClientTick() throws IOException {
        String source = Files.readString(INPUT_SOURCE).replaceAll("\\s+", " ");
        String disconnectMarker = "if (minecraft.player == null || minecraft.getConnection() == null) {";
        int disconnect = source.indexOf(disconnectMarker);
        int selectionClear = source.indexOf("SELECTION.reconcile(List.of());", disconnect);
        int syncClear = source.indexOf("ClientArcanaSyncState.clear();", disconnect);
        int returnIndex = source.indexOf("return;", disconnect);

        assertTrue(disconnect >= 0, "client tick must retain an explicit disconnect branch");
        assertTrue(selectionClear > disconnect && selectionClear < returnIndex,
                "disconnect must clear local selection in the same tick before returning");
        assertTrue(syncClear > disconnect && syncClear < returnIndex,
                "disconnect must clear synchronized client state before returning");
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
