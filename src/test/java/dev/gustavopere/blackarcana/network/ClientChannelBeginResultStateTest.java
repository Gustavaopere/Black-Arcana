package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientChannelBeginResultStateTest {
    @AfterEach
    void clearState() {
        ClientArcanaSyncState.clear();
    }

    @Test
    void clientRetainsOnlyValidatedServerAuthoredBeginAcknowledgement() {
        ChannelBeginResultPayload accepted = new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                "00000000-0000-0000-0000-000000000111",
                true,
                "allowed",
                "channel session accepted");

        ClientArcanaSyncState.replaceChannelBeginResult(accepted);

        assertEquals(accepted, ClientArcanaSyncState.lastChannelBeginResult().orElseThrow());

        ClientArcanaSyncState.clear();
        assertTrue(ClientArcanaSyncState.lastChannelBeginResult().isEmpty());
    }
}
