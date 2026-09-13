package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.network.neoforge.AstralMoveIntentPacket;
import dev.gustavopere.blackarcana.network.neoforge.AstralReturnIntentPacket;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralSeveranceNetworkIntentTest {
    @Test
    void movePayloadCarriesOnlyExactProjectionIdentitySequenceAndBoundedAxes() {
        UUID projectionId = UUID.randomUUID();
        AstralMoveIntentPayload payload = new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                7L,
                -0.5D,
                0.25D,
                1.0D,
                12.0F,
                -8.0F);

        assertEquals(
                new AstralSeveranceRuntime.ControlIntent(
                        projectionId, 7L, -0.5D, 0.25D, 1.0D, 12.0F, -8.0F),
                payload.toControlIntent());
        assertEquals(
                Set.of(
                        "protocolVersion",
                        "projectionId",
                        "sequence",
                        "strafeAxis",
                        "verticalAxis",
                        "forwardAxis",
                        "yawDeltaDegrees",
                        "pitchDeltaDegrees"),
                componentNames(AstralMoveIntentPayload.class));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("casterId"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("x"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("y"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("z"));

        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 0L, 0.0D, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, Double.NaN, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, 1.01D, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, 0.0D, 0.0D, 0.0D, Float.NaN, 0.0F));
    }

    @Test
    void returnPayloadCarriesOnlyExactProjectionIdentityAndMonotonicSequence() {
        UUID projectionId = UUID.randomUUID();
        AstralReturnIntentPayload payload = new AstralReturnIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                8L);

        assertEquals(projectionId, payload.projectionId());
        assertEquals(8L, payload.sequence());
        assertEquals(
                Set.of("protocolVersion", "projectionId", "sequence"),
                componentNames(AstralReturnIntentPayload.class));
        assertFalse(componentNames(AstralReturnIntentPayload.class).contains("casterId"));
        assertThrows(IllegalArgumentException.class, () -> new AstralReturnIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 0L));
    }

    @Test
    void wireCodecsRoundTripOnlyValidatedDomainIntent() {
        UUID projectionId = UUID.randomUUID();
        AstralMoveIntentPayload move = new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                42L,
                -1.0D,
                0.5D,
                0.25D,
                15.0F,
                -12.5F);
        AstralReturnIntentPayload returned = new AstralReturnIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                43L);

        ByteBuf moveBuffer = Unpooled.buffer();
        try {
            AstralMoveIntentPacket.STREAM_CODEC.encode(moveBuffer, AstralMoveIntentPacket.from(move));
            AstralMoveIntentPacket decoded = AstralMoveIntentPacket.STREAM_CODEC.decode(moveBuffer);
            assertEquals(move, decoded.toDomain());
            assertEquals(0, moveBuffer.readableBytes());
        } finally {
            moveBuffer.release();
        }

        ByteBuf returnBuffer = Unpooled.buffer();
        try {
            AstralReturnIntentPacket.STREAM_CODEC.encode(returnBuffer, AstralReturnIntentPacket.from(returned));
            AstralReturnIntentPacket decoded = AstralReturnIntentPacket.STREAM_CODEC.decode(returnBuffer);
            assertEquals(returned, decoded.toDomain());
            assertEquals(0, returnBuffer.readableBytes());
        } finally {
            returnBuffer.release();
        }
    }

    private static Set<String> componentNames(Class<?> recordType) {
        return Arrays.stream(recordType.getRecordComponents())
                .map(component -> component.getName())
                .collect(Collectors.toUnmodifiableSet());
    }
}
