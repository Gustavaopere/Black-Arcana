package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ChannelInvocationPayloadTest {
    @Test
    void beginCarriesOnlyCastIdentitySpellAndLoadoutSlot() {
        ArcanaCastId castId = ArcanaCastId.random();
        ArcanaSpellId spellId = ArcanaSpellId.parse("black_arcana:channelled");
        ChannelBeginIntentPayload payload = new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                spellId.canonical(),
                3);

        assertEquals(castId, payload.parsedCastId());
        assertEquals(spellId, payload.parsedSpellId());
        assertEquals(3, payload.loadoutSlot());
        assertEquals("", payload.toCastIntent().targetHint(),
                "begin must not freeze a stale client target; release owns the bounded target hint");
    }

    @Test
    void releaseAndCancelCarryOnlyExactCastIdentityAndBoundedReleaseHint() {
        ArcanaCastId castId = ArcanaCastId.random();
        ChannelReleaseIntentPayload release = new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                "entity:00000000-0000-0000-0000-000000000001");
        ChannelCancelIntentPayload cancel = new ChannelCancelIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical());

        assertEquals(castId, release.parsedCastId());
        assertEquals(castId, cancel.parsedCastId());
        assertThrows(IllegalArgumentException.class, () -> new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                "x".repeat(ArcanaProtocol.MAX_TARGET_HINT_LENGTH + 1)));
    }
}
