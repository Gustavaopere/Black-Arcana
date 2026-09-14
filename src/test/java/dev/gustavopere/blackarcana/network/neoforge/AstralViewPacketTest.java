package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralViewPacketTest {
    @Test
    void packetRoundTripsExactAstralViewIdentityWithoutTrailingBytes() {
        AstralViewPayload payload = new AstralViewPayload(
                ArcanaProtocol.VERSION,
                AstralViewPayload.Action.BEGIN,
                UUID.randomUUID(),
                99);
        AstralViewPacket packet = AstralViewPacket.from(payload);
        ByteBuf buffer = Unpooled.buffer();
        try {
            AstralViewPacket.STREAM_CODEC.encode(buffer, packet);
            AstralViewPacket decoded = AstralViewPacket.STREAM_CODEC.decode(buffer);
            assertEquals(packet, decoded);
            assertEquals(payload, decoded.toDomain());
            assertEquals(0, buffer.readableBytes());
        } finally {
            buffer.release();
        }
    }

    @Test
    void malformedWireActionFailsClosed() {
        assertThrows(IllegalArgumentException.class, () -> new AstralViewPacket(
                ArcanaProtocol.VERSION,
                "NOT_AN_ACTION",
                UUID.randomUUID(),
                1));
    }
}
