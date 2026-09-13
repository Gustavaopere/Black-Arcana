package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class DiscoverabilityClientWiringTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path CLIENT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path INPUT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");
    private static final Path SYNC = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/network/ClientArcanaSyncState.java");
    private static final Path BINDINGS = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/DiscoverabilityBindings.java");
    private static final Path LOADOUT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");

    @Test
    void acceptedLoadoutSnapshotIsTheEventDrivenFirstUseTrigger() throws Exception {
        String client = Files.readString(CLIENT);
        String sync = Files.readString(SYNC);

        assertTrue(client.contains(
                "ClientArcanaSyncState.installLoadoutObserver(DiscoverabilityClientRuntime::acceptLoadout);"),
                "physical client must install a narrow accepted-loadout observer");
        assertTrue(sync.contains("installLoadoutObserver"),
                "common-safe sync cache must expose the accepted-loadout observer seam");
        int cacheWrite = sync.indexOf("loadout = acceptedLoadout;");
        int notify = sync.indexOf("loadoutObserver.accept(player, acceptedLoadout);");
        assertTrue(cacheWrite >= 0, "accepted loadout must be cached before presentation notification");
        assertTrue(notify > cacheWrite,
                "discoverability may observe only the already accepted immutable loadout snapshot");
    }

    @Test
    void currentBindingAdapterUsesMinecraftMappingTruthAndNoDefaultFallbacks() throws Exception {
        String source = Files.readString(BINDINGS);

        assertTrue(source.contains("mapping.isUnbound()"),
                "unbound presentation must come from the current KeyMapping state");
        assertTrue(source.contains("mapping.getTranslatedKeyMessage().getString()"),
                "bound presentation must use Minecraft's current translated key label");
        assertTrue(!source.contains("GLFW_KEY_R") && !source.contains("GLFW_KEY_V"),
                "discoverability adapter must not invent default R/V labels");
    }

    @Test
    void hintLayerIsClientOnlyAndSessionStateClearsOnDisconnect() throws Exception {
        String client = Files.readString(CLIENT);
        String input = Files.readString(INPUT);

        assertTrue(client.contains("DiscoverabilityHintLayer::register"),
                "physical client must register the bounded hint layer");
        assertTrue(input.contains("DiscoverabilityClientRuntime.clearSession();"),
                "disconnect/session loss must clear seen, dismissed and active help state");
    }

    @Test
    void editorHelpInterceptsMutationKeysAndPointerClicksBeforeDraftActions() throws Exception {
        String source = Files.readString(LOADOUT);
        int keyHandler = source.indexOf("public boolean keyPressed");
        int helpKeyGuard = source.indexOf("if (helpVisible)", keyHandler);
        int enterAction = source.indexOf("if (keyCode == GLFW.GLFW_KEY_ENTER", keyHandler);
        int mouseHandler = source.indexOf("public boolean mouseClicked");
        int mouseHelpGuard = source.indexOf("if (helpVisible) return true;", mouseHandler);
        int mouseDraftToggle = source.indexOf("draft.toggle", mouseHandler);

        assertTrue(keyHandler >= 0 && helpKeyGuard > keyHandler && helpKeyGuard < enterAction,
                "help mode must intercept keyboard input before Enter/apply or other draft mutation keys");
        assertTrue(mouseHandler >= 0 && mouseHelpGuard > mouseHandler && mouseHelpGuard < mouseDraftToggle,
                "help mode must consume pointer clicks before draft mutation");
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
