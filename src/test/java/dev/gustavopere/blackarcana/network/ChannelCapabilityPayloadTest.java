package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ChannelCapabilityPayloadTest {
    @Test
    void snapshotIsCanonicalSortedAndServerAuthored() {
        Map<ArcanaSpellId, ArcanaChannelSpec> specs = new LinkedHashMap<>();
        specs.put(ArcanaSpellId.parse("black_arcana:zeta"), new ArcanaChannelSpec(10L, 40L));
        specs.put(ArcanaSpellId.parse("black_arcana:alpha"), new ArcanaChannelSpec(5L, 20L));

        ChannelCapabilityPayload payload = ChannelCapabilityPayload.from(specs);

        assertEquals(ArcanaProtocol.VERSION, payload.protocolVersion());
        assertEquals(2, payload.entries().size());
        assertEquals("black_arcana:alpha", payload.entries().get(0).spellId());
        assertEquals(5L, payload.entries().get(0).minimumTicks());
        assertEquals(20L, payload.entries().get(0).maximumTicks());
        assertEquals("black_arcana:zeta", payload.entries().get(1).spellId());
    }

    @Test
    void malformedOrOversizedSnapshotsFailClosed() {
        assertThrows(IllegalArgumentException.class, () -> new ChannelCapabilityPayload.Entry(
                "not a resource id",
                0L,
                20L));
        assertThrows(IllegalArgumentException.class, () -> new ChannelCapabilityPayload.Entry(
                "black_arcana:test",
                -1L,
                20L));
        assertThrows(IllegalArgumentException.class, () -> new ChannelCapabilityPayload.Entry(
                "black_arcana:test",
                30L,
                20L));
    }
}
