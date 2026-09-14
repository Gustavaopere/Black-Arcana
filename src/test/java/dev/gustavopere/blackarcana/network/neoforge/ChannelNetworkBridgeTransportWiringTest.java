package dev.gustavopere.blackarcana.network.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ChannelNetworkBridgeTransportWiringTest {
    private static final Path BRIDGE_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/network/neoforge/ChannelNetworkBridge.java");

    @Test
    void registersAllChannelPacketsWithCanonicalDirectionsAndReplies() throws IOException {
        String normalized = Files.readString(BRIDGE_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains("registrar.playToServer( ChannelBeginIntentPacket.TYPE"));
        assertTrue(normalized.contains("registrar.playToServer( ChannelReleaseIntentPacket.TYPE"));
        assertTrue(normalized.contains("registrar.playToServer( ChannelCancelIntentPacket.TYPE"));
        assertTrue(normalized.contains("registrar.playToClient( ChannelBeginResultPacket.TYPE"));
        assertTrue(normalized.contains("registrar.playToClient( ChannelCapabilityPacket.TYPE"));

        assertTrue(
                occurrences(normalized, "if (!(context.player() instanceof ServerPlayer player)) return;") >= 3,
                "every C2S channel handler must derive the authenticated caster from IPayloadContext.player()");
        assertTrue(normalized.contains(
                "context.reply(ChannelBeginResultPacket.from(dispatchBeginServerbound(player, packet.toDomain())));"));
        assertTrue(normalized.contains(
                "context.reply(CastResultPacket.from(dispatchReleaseServerbound(player, packet.toDomain())));"));
        assertTrue(normalized.contains("dispatchCancelServerbound(player, packet.toDomain());"));
        assertTrue(normalized.contains("dispatchBeginResultClientbound(context.player(), packet.toDomain());"));
        assertTrue(normalized.contains("dispatchCapabilityClientbound(context.player(), packet.toDomain());"));
    }

    private static int occurrences(String haystack, String needle) {
        int count = 0;
        int index = 0;
        while ((index = haystack.indexOf(needle, index)) >= 0) {
            count++;
            index += needle.length();
        }
        return count;
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
