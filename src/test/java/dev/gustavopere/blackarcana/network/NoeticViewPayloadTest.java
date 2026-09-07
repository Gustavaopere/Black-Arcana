package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NoeticViewPayloadTest {
    @Test
    void beginAndEndCarryOnlyCameraCapableObservationKinds() {
        NoeticViewPayload begin = new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                42);
        NoeticViewPayload end = new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.END,
                NoeticObservationKind.ASTRAL_SEVERANCE,
                17);

        assertEquals(NoeticViewPayload.Action.BEGIN, begin.action());
        assertEquals(NoeticObservationKind.BORROWED_SIGHT, begin.kind());
        assertEquals(42, begin.targetEntityId());
        assertEquals(NoeticViewPayload.Action.END, end.action());
        assertEquals(NoeticObservationKind.ASTRAL_SEVERANCE, end.kind());
        assertEquals(17, end.targetEntityId());
    }

    @Test
    void payloadFailsClosedOnProtocolKindOrEntityIdentityViolations() {
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION + 1,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                1));
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.NAMESCRY,
                1));
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.END,
                NoeticObservationKind.BORROWED_SIGHT,
                -1));
    }
}
