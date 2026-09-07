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
}
