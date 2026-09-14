package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralViewClientStateTest {
    @Test
    void staleEndCannotClearNewerProjectionIdentity() {
        AstralViewClientState state = new AstralViewClientState();
        UUID oldProjection = UUID.randomUUID();
        UUID newProjection = UUID.randomUUID();

        state.accept(payload(AstralViewPayload.Action.BEGIN, oldProjection, 17));
        state.accept(payload(AstralViewPayload.Action.BEGIN, newProjection, 29));
        state.accept(payload(AstralViewPayload.Action.END, oldProjection, 17));

        assertEquals(
                new AstralViewClientState.Desired(newProjection, 29),
                state.desired().orElseThrow());

        state.accept(payload(AstralViewPayload.Action.END, newProjection, 29));
        assertTrue(state.desired().isEmpty());
    }

    @Test
    void clearRemovesPresentationStateWithoutGameplaySideEffects() {
        AstralViewClientState state = new AstralViewClientState();
        state.accept(payload(AstralViewPayload.Action.BEGIN, UUID.randomUUID(), 17));
        state.clear();
        assertTrue(state.desired().isEmpty());
    }

    private static AstralViewPayload payload(
            AstralViewPayload.Action action,
            UUID projectionId,
            int entityId
    ) {
        return new AstralViewPayload(ArcanaProtocol.VERSION, action, projectionId, entityId);
    }
}
