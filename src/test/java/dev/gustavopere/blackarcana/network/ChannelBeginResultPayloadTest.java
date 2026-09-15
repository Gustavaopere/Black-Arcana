package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ChannelBeginResultPayloadTest {
    @Test
    void acknowledgementPreservesExactCastIdentityWithoutPretendingEffectExecuted() {
        ArcanaCastId castId = ArcanaCastId.random();
        ChannelBeginResultPayload accepted = ChannelBeginResultPayload.from(castId, ArcanaDecision.allow());
        assertEquals(castId, accepted.parsedCastId());
        assertTrue(accepted.accepted());
        assertEquals("ok", accepted.code());

        ChannelBeginResultPayload denied = ChannelBeginResultPayload.from(
                castId,
                ArcanaDecision.deny("channel_not_configured", "no server-owned channel specification"));
        assertEquals(castId, denied.parsedCastId());
        assertFalse(denied.accepted());
        assertEquals("channel_not_configured", denied.code());
    }

    @Test
    void acknowledgementIsProtocolBounded() {
        String tooLong = "x".repeat(ArcanaProtocol.MAX_RESULT_DETAIL_LENGTH + 1);
        assertThrows(IllegalArgumentException.class, () -> new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                false,
                "denied",
                tooLong));
    }
}
