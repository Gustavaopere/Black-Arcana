package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.CooldownSnapshotPayload;
import dev.gustavopere.blackarcana.network.LoadoutSnapshotPayload;
import dev.gustavopere.blackarcana.network.LoadoutUpdatePayload;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import net.minecraft.network.codec.StreamCodec;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NeoForgePacketCodecTest {
    @Test
    void castIntentRoundTrips() {
        CastIntentPacket packet = CastIntentPacket.from(new CastIntentPayload(
                ArcanaProtocol.VERSION,
                "11111111-1111-1111-1111-111111111111",
                "black_arcana:test_spell",
                2,
                "22222222-2222-2222-2222-222222222222"));
        assertEquals(packet, roundTrip(CastIntentPacket.STREAM_CODEC, packet));
    }

    @Test
    void castResultRoundTrips() {
        CastResultPacket packet = CastResultPacket.from(new CastResultPayload(
                ArcanaProtocol.VERSION,
                "11111111-1111-1111-1111-111111111111",
                "SUCCESS",
                "ok",
                "executed"));
        assertEquals(packet, roundTrip(CastResultPacket.STREAM_CODEC, packet));
    }

    @Test
    void cooldownSnapshotRoundTrips() {
        CooldownSnapshotPacket packet = CooldownSnapshotPacket.from(new CooldownSnapshotPayload(
                ArcanaProtocol.VERSION,
                List.of(
                        new CooldownSnapshotPayload.Entry("black_arcana:shared_a", 20L),
                        new CooldownSnapshotPayload.Entry("black_arcana:shared_b", 40L))));
        assertEquals(packet, roundTrip(CooldownSnapshotPacket.STREAM_CODEC, packet));
    }

    @Test
    void spellPresentationRoundTrips() {
        SpellPresentationPacket packet = SpellPresentationPacket.from(new SpellPresentationPayload(
                ArcanaProtocol.VERSION,
                List.of(new SpellPresentationPayload.Entry(
                        "black_arcana:test_spell",
                        "spell.black_arcana.test_spell",
                        "black_arcana:test_spell"))));
        assertEquals(packet, roundTrip(SpellPresentationPacket.STREAM_CODEC, packet));
    }

    @Test
    void loadoutUpdateRoundTrips() {
        LoadoutUpdatePacket packet = LoadoutUpdatePacket.from(new LoadoutUpdatePayload(
                ArcanaProtocol.VERSION,
                List.of("black_arcana:first", "black_arcana:second")));
        assertEquals(packet, roundTrip(LoadoutUpdatePacket.STREAM_CODEC, packet));
    }

    @Test
    void loadoutSnapshotRoundTrips() {
        LoadoutSnapshotPacket packet = LoadoutSnapshotPacket.from(new LoadoutSnapshotPayload(
                ArcanaProtocol.VERSION,
                List.of("black_arcana:first", "black_arcana:second")));
        assertEquals(packet, roundTrip(LoadoutSnapshotPacket.STREAM_CODEC, packet));
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
