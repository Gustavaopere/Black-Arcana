package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertThrows;

class NoeticViewPayloadTest {
    @Test
    void astralSeveranceCannotOwnTheBorrowedSightCameraChannel() {
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.ASTRAL_SEVERANCE,
                17));
    }

    @Test
    void malformedBorrowedSightPayloadFailsClosed() {
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION + 1,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                17));
        assertThrows(IllegalArgumentException.class, () -> new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                -1));
    }
}
