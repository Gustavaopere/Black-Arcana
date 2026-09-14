package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientChannelInputWiringTest {
    private static final Path INPUT_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");

    @Test
    void physicalInputRoutesServerAdvertisedChannelsThroughExactBeginReleaseLifecycle() throws IOException {
        String normalized = Files.readString(INPUT_SOURCE).replaceAll("\\s+", " ");

        assertTrue(normalized.contains(
                "ClientChannelInvocationState CHANNELS = new ClientChannelInvocationState()"),
                "physical input must retain one exact pending/active channel cast id");
        assertTrue(normalized.contains("ClientArcanaSyncState.channelCapability(spell).isPresent()"),
                "only server-advertised channel capability may switch input away from immediate casting");
        assertTrue(normalized.contains("CHANNELS.begin(inputId, slot, spell, castId)"),
                "BEGIN must bind the physical input source to one exact cast id");
        assertTrue(normalized.contains("ChannelNetworkBridge.requestBegin(new ChannelBeginIntentPayload("),
                "channeled input must use the bounded BEGIN transport");
        assertTrue(normalized.contains("ChannelNetworkBridge.requestRelease(new ChannelReleaseIntentPayload("),
                "key release must use the bounded RELEASE transport");
        assertTrue(normalized.contains("CHANNELS.rejectBegin(beginResult.parsedCastId())"),
                "a server-authored BEGIN denial must clear only its exact local session");
        assertTrue(normalized.contains("ArcanaNetworkBridge.sendCastIntent(new CastIntentPayload("),
                "non-channeled spells must preserve the canonical immediate-cast path");
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
