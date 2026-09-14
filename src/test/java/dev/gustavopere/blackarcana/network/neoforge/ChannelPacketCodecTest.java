package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import net.minecraft.network.codec.StreamCodec;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ChannelPacketCodecTest {
    private static final String CAST_ID = "11111111-1111-1111-1111-111111111111";
    private static final String SPELL_ID = "black_arcana:channel_probe";

    @Test
    void beginIntentRoundTrips() {
        ChannelBeginIntentPacket packet = ChannelBeginIntentPacket.from(new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                CAST_ID,
                SPELL_ID,
                2));
        assertEquals(packet, roundTrip(ChannelBeginIntentPacket.STREAM_CODEC, packet));
        assertEquals(packet.toDomain(), roundTrip(ChannelBeginIntentPacket.STREAM_CODEC, packet).toDomain());
    }

    @Test
    void releaseIntentRoundTrips() {
        ChannelReleaseIntentPacket packet = ChannelReleaseIntentPacket.from(new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                CAST_ID,
                "22222222-2222-2222-2222-222222222222"));
        assertEquals(packet, roundTrip(ChannelReleaseIntentPacket.STREAM_CODEC, packet));
        assertEquals(packet.toDomain(), roundTrip(ChannelReleaseIntentPacket.STREAM_CODEC, packet).toDomain());
    }

    @Test
    void cancelIntentRoundTrips() {
        ChannelCancelIntentPacket packet = ChannelCancelIntentPacket.from(new ChannelCancelIntentPayload(
                ArcanaProtocol.VERSION,
                CAST_ID));
        assertEquals(packet, roundTrip(ChannelCancelIntentPacket.STREAM_CODEC, packet));
        assertEquals(packet.toDomain(), roundTrip(ChannelCancelIntentPacket.STREAM_CODEC, packet).toDomain());
    }

    @Test
    void beginResultRoundTripsWithoutCastExecutionStatus() {
        ChannelBeginResultPacket packet = ChannelBeginResultPacket.from(new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                CAST_ID,
                true,
                "ok",
                "channel accepted"));
        assertEquals(packet, roundTrip(ChannelBeginResultPacket.STREAM_CODEC, packet));
        assertEquals(packet.toDomain(), roundTrip(ChannelBeginResultPacket.STREAM_CODEC, packet).toDomain());
    }

    @Test
    void capabilitySnapshotRoundTrips() {
        ChannelCapabilityPacket packet = ChannelCapabilityPacket.from(new ChannelCapabilityPayload(
                ArcanaProtocol.VERSION,
                List.of(
                        new ChannelCapabilityPayload.Entry("black_arcana:first", 5L, 40L),
                        new ChannelCapabilityPayload.Entry("black_arcana:second", 10L, 80L))));
        assertEquals(packet, roundTrip(ChannelCapabilityPacket.STREAM_CODEC, packet));
        assertEquals(packet.toDomain(), roundTrip(ChannelCapabilityPacket.STREAM_CODEC, packet).toDomain());
    }

    private static <T> T roundTrip(StreamCodec<ByteBuf, T> codec, T value) {
        ByteBuf buffer = Unpooled.buffer();
        try {
            codec.encode(buffer, value);
            return codec.decode(buffer);
        } finally {
            buffer.release();
        }
    }
}
