package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientChannelCapabilityStateTest {
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:channel_capability_probe");

    @AfterEach
    void clearState() {
        ClientArcanaSyncState.clear();
    }

    @Test
    void clientReadsOnlyServerAuthoredChannelCapabilitySnapshot() {
        ClientArcanaSyncState.replaceChannelCapabilities(new ChannelCapabilityPayload(
                ArcanaProtocol.VERSION,
                List.of(new ChannelCapabilityPayload.Entry(SPELL.canonical(), 4L, 30L))));

        assertEquals(new ArcanaChannelSpec(4L, 30L),
                ClientArcanaSyncState.channelCapability(SPELL).orElseThrow());
        assertTrue(ClientArcanaSyncState.channelCapability(
                ArcanaSpellId.parse("black_arcana:not_channeled")).isEmpty());

        ClientArcanaSyncState.clear();
        assertTrue(ClientArcanaSyncState.channelCapability(SPELL).isEmpty());
    }
}
