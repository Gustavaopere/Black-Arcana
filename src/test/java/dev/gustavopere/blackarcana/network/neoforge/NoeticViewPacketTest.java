package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NoeticViewPacketTest {
    @Test
    void packetRoundTripsBoundedDomainInstruction() {
        NoeticViewPayload payload = new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                99);

        NoeticViewPacket packet = NoeticViewPacket.from(payload);

        assertEquals(payload, packet.toDomain());
    }

    @Test
    void packetConstructorRejectsMalformedWireEnumsOrNonCameraKinds() {
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPacket(
                ArcanaProtocol.VERSION,
                "NOT_AN_ACTION",
                NoeticObservationKind.BORROWED_SIGHT.name(),
                1));
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPacket(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN.name(),
                NoeticObservationKind.NAMESCRY.name(),
                1));
    }
}
