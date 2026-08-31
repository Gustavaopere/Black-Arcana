package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.neoforge.HazardResistanceForecastPacket;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class HazardResistanceForecastContractTest {
    @Test
    void payloadEnforcesAvailabilityAndStatusConsistency() {
        HazardResistanceForecastPayload payload = new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            4L,
            "black_arcana:dangerous_spell",
            true,
            HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED.name(),
            ArcaneDangerTier.DANGEROUS.name(),
            16.0D,
            12.0D,
            24.0D);

        assertEquals(HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED, payload.parsedStatus());
        assertEquals(ArcaneDangerTier.DANGEROUS, payload.parsedTier());

        assertThrows(IllegalArgumentException.class, () -> new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            5L,
            payload.spellId(),
            true,
            HazardResistanceForecastPayload.Status.UNAVAILABLE.name(),
            payload.dangerTier(),
            0.0D,
            12.0D,
            24.0D));
        assertThrows(IllegalArgumentException.class, () -> new HazardResistanceForecastRequestPayload(
            ArcanaProtocol.VERSION, -1L, payload.spellId()));
    }

    @Test
    void nineFieldPacketRoundTripsThroughExplicitStreamCodec() {
        HazardResistanceForecastPacket packet = HazardResistanceForecastPacket.from(
            new HazardResistanceForecastPayload(
                ArcanaProtocol.VERSION,
                9L,
                "black_arcana:forbidden_spell",
                true,
                HazardResistanceForecastPayload.Status.BELOW_MINIMUM.name(),
                ArcaneDangerTier.FORBIDDEN.name(),
                8.0D,
                20.0D,
                40.0D));
        ByteBuf buffer = Unpooled.buffer();
        try {
            HazardResistanceForecastPacket.STREAM_CODEC.encode(buffer, packet);
            HazardResistanceForecastPacket decoded = HazardResistanceForecastPacket.STREAM_CODEC.decode(buffer);
            assertEquals(packet, decoded);
            assertEquals(HazardResistanceForecastPayload.Status.BELOW_MINIMUM, decoded.toDomain().parsedStatus());
        } finally {
            buffer.release();
        }
    }
}
