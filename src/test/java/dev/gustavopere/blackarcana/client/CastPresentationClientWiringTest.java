package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class CastPresentationClientWiringTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path INPUT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");
    private static final Path CLIENT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path SYNC = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/network/ClientArcanaSyncState.java");

    @Test
    void castInputRecordsTheSameCanonicalCastIdThatIsSentToServer() throws Exception {
        String source = Files.readString(INPUT);

        int create = source.indexOf("ArcanaCastId castId = ArcanaCastId.random();");
        int record = source.indexOf("CastPresentationClientRuntime.recordLocalIntent(castId, spell, minecraft.player.tickCount);");
        int send = source.indexOf("castId.canonical(),");

        assertTrue(create >= 0, "cast input must create one canonical ArcanaCastId for correlation");
        assertTrue(record > create, "local anticipation must record the same cast id before transport");
        assertTrue(send > record, "the recorded cast id must be the exact id sent to the server");
    }

    @Test
    void authoritativeResultObserverIsInstalledOnlyFromPhysicalClientEntrypoint() throws Exception {
        String client = Files.readString(CLIENT);
        String sync = Files.readString(SYNC);

        assertTrue(client.contains(
                "ClientArcanaSyncState.installResultObserver(CastPresentationClientRuntime::acceptResult);"),
                "physical-client entrypoint must install the audiovisual result observer");
        assertTrue(sync.contains("installResultObserver"),
                "common-safe sync cache must expose a narrow result-observer seam");
        assertTrue(sync.contains("resultObserver.accept(player, payload);"),
                "authoritative result must be forwarded after the synchronized cache accepts it");
    }

    @Test
    void disconnectAndClientTickDriveBoundedLifecycleCleanup() throws Exception {
        String source = Files.readString(INPUT);

        assertTrue(source.contains("CastPresentationClientRuntime.clear();"),
                "disconnect/session loss must clear audiovisual correlation state");
        assertTrue(source.contains("CastPresentationClientRuntime.tick(minecraft.player);"),
                "physical-client ticks must drive stale-entry eviction");
    }

    @Test
    void deathDimensionAndScreenTransitionsTearDownTemporaryPresentationState() throws Exception {
        String source = Files.readString(INPUT);

        assertTrue(source.contains("ResourceKey<Level> presentationDimension"),
                "physical client must retain only the last observed dimension for teardown detection");
        assertTrue(source.contains("!minecraft.player.isAlive()"),
                "player death must explicitly clear temporary cast presentation state");
        assertTrue(source.contains("!presentationDimension.equals(currentDimension)"),
                "dimension transitions must explicitly clear temporary cast presentation state");
        assertTrue(source.contains("minecraft.screen != null"),
                "screen transitions must suppress/clear the transient visual pulse where relevant");
        assertTrue(source.contains("CastPresentationEffectsLayer.clear();"),
                "teardown paths must clear transient audiovisual pulse state");
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
        return fail("Unable to locate repository root from test working directory");
    }
}
