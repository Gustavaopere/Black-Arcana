package dev.gustavopere.blackarcana.network.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ChannelNetworkBridgeOutboundWiringTest {
    private static final Path BRIDGE_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/network/neoforge/ChannelNetworkBridge.java");

    @Test
    void exposesOnlyValidatedIntentAndServerCapabilityOutboundHelpers() throws IOException {
        String normalized = Files.readString(BRIDGE_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains(
                "public static void requestBegin(ChannelBeginIntentPayload payload)"));
        assertTrue(normalized.contains(
                "PacketDistributor.sendToServer(ChannelBeginIntentPacket.from(Objects.requireNonNull(payload, \"payload\")));"));
        assertTrue(normalized.contains(
                "public static void requestRelease(ChannelReleaseIntentPayload payload)"));
        assertTrue(normalized.contains(
                "PacketDistributor.sendToServer(ChannelReleaseIntentPacket.from(Objects.requireNonNull(payload, \"payload\")));"));
        assertTrue(normalized.contains(
                "public static void requestCancel(ChannelCancelIntentPayload payload)"));
        assertTrue(normalized.contains(
                "PacketDistributor.sendToServer(ChannelCancelIntentPacket.from(Objects.requireNonNull(payload, \"payload\")));"));

        assertTrue(normalized.contains(
                "public static boolean sendCapability(ServerPlayer player, ChannelCapabilityPayload payload)"));
        assertTrue(normalized.contains("if (!player.connection.hasChannel(ChannelCapabilityPacket.TYPE)) return false;"));
        assertTrue(normalized.contains("PacketDistributor.sendToPlayer(player, ChannelCapabilityPacket.from(payload));"));
        assertTrue(normalized.contains("return true;"));
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
