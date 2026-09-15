package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeManagerChannelNetworkWiringTest {
    private static final Path MANAGER_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java");
    private static final Path MOD_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java");

    @Test
    void managerRoutesChannelTransportThroughCanonicalRuntimeAuthority() throws IOException {
        String normalized = Files.readString(MANAGER_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains(
                "public static ChannelBeginResultPayload handleChannelBegin(ServerPlayer player, ChannelBeginIntentPayload intent)"));
        assertTrue(normalized.contains(
                "runtime.beginChannel(ServerPlayerArcanaContext.from(player), intent)"));
        assertTrue(normalized.contains(
                "ChannelBeginResultPayload.from(intent.parsedCastId(), decision)"));

        assertTrue(normalized.contains(
                "public static CastResultPayload handleChannelRelease(ServerPlayer player, ChannelReleaseIntentPayload intent)"));
        assertTrue(normalized.contains(
                "runtime.releaseChannel(ServerPlayerArcanaContext.from(player), intent)"));
        assertTrue(normalized.contains(
                "ArcanaNetworkBridge.sendCooldownSnapshot(player, cooldownSnapshot(runtime, player, server.overworld().getGameTime()))"),
                "successful channel release must refresh the same canonical cooldown snapshot used by immediate casts");

        assertTrue(normalized.contains(
                "public static boolean handleChannelCancel(ServerPlayer player, ChannelCancelIntentPayload intent)"));
        assertTrue(normalized.contains(
                "runtime.cancelChannel(ServerPlayerArcanaContext.from(player), intent)"));

        assertTrue(normalized.contains(
                "ChannelNetworkBridge.sendCapability(player, ChannelCapabilityPayload.from(runtime.channelSpecs().snapshot()))"),
                "channel duration capability must be server-authored from the runtime registry on login");
    }

    @Test
    void modEntrypointRegistersChannelTransportAndServerHandlers() throws IOException {
        String normalized = Files.readString(MOD_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains("modEventBus.addListener(ChannelNetworkBridge::register);"));
        assertTrue(normalized.contains(
                "ChannelNetworkBridge.installBeginHandler(ArcanaServerRuntimeManager::handleChannelBegin);"));
        assertTrue(normalized.contains(
                "ChannelNetworkBridge.installReleaseHandler(ArcanaServerRuntimeManager::handleChannelRelease);"));
        assertTrue(normalized.contains(
                "ChannelNetworkBridge.installCancelHandler(ArcanaServerRuntimeManager::handleChannelCancel);"));
        assertTrue(normalized.contains(
                "ChannelNetworkBridge.installCapabilityHandler(ClientArcanaSyncState::acceptChannelCapabilities);"));
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
