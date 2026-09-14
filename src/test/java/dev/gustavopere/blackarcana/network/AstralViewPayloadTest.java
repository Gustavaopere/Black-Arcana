package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralViewPayloadTest {
    @Test
    void exactProjectionIdentityAndRuntimeEntityIdArePreserved() {
        UUID projectionId = UUID.randomUUID();
        AstralViewPayload payload = new AstralViewPayload(
                ArcanaProtocol.VERSION,
                AstralViewPayload.Action.BEGIN,
                projectionId,
                42);

        assertEquals(projectionId, payload.projectionId());
        assertEquals(42, payload.entityId());
    }

    @Test
    void malformedPresentationInstructionsFailClosed() {
        UUID projectionId = UUID.randomUUID();
        assertThrows(IllegalArgumentException.class, () -> new AstralViewPayload(
                ArcanaProtocol.VERSION,
                AstralViewPayload.Action.BEGIN,
                projectionId,
                -1));
        assertThrows(NullPointerException.class, () -> new AstralViewPayload(
                ArcanaProtocol.VERSION,
                null,
                projectionId,
                1));
        assertThrows(NullPointerException.class, () -> new AstralViewPayload(
                ArcanaProtocol.VERSION,
                AstralViewPayload.Action.BEGIN,
                null,
                1));
    }
}
