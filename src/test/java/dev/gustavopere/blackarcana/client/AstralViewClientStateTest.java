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
    void cameraBeginDoesNotAuthorizeMovementUntilExactServerArm() {
        AstralViewClientState state = new AstralViewClientState();
        UUID projection = UUID.randomUUID();
        UUID foreignProjection = UUID.randomUUID();

        state.accept(payload(AstralViewPayload.Action.BEGIN, projection, 17));
        assertTrue(state.movementControl().isEmpty(),
                "camera presentation alone must never authorize client movement redirection");

        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, foreignProjection, 29));
        assertTrue(state.movementControl().isEmpty(),
                "a foreign projection cannot arm movement control");

        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, projection, 29));
        assertTrue(state.movementControl().isEmpty(),
                "the transient entity id must match the exact active presentation");

        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, projection, 17));
        assertEquals(
                new AstralViewClientState.Desired(projection, 17),
                state.movementControl().orElseThrow());
    }

    @Test
    void endAndMoveEndOnlyClearTheirExactSession() {
        AstralViewClientState state = new AstralViewClientState();
        UUID firstProjection = UUID.randomUUID();
        UUID secondProjection = UUID.randomUUID();

        state.accept(payload(AstralViewPayload.Action.BEGIN, firstProjection, 17));
        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, firstProjection, 17));
        state.accept(payload(AstralViewPayload.Action.BEGIN, secondProjection, 29));

        assertTrue(state.movementControl().isEmpty(),
                "a new presentation identity must revoke movement authority inherited from the old session");

        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, secondProjection, 29));
        state.accept(payload(AstralViewPayload.Action.MOVE_END, firstProjection, 17));
        assertEquals(
                new AstralViewClientState.Desired(secondProjection, 29),
                state.movementControl().orElseThrow(),
                "stale movement teardown cannot disarm a newer exact session");

        state.accept(payload(AstralViewPayload.Action.END, secondProjection, 29));
        assertTrue(state.desired().isEmpty());
        assertTrue(state.movementControl().isEmpty());
    }

    @Test
    void clearRemovesPresentationAndMovementStateWithoutGameplaySideEffects() {
        AstralViewClientState state = new AstralViewClientState();
        UUID projection = UUID.randomUUID();
        state.accept(payload(AstralViewPayload.Action.BEGIN, projection, 17));
        state.accept(payload(AstralViewPayload.Action.MOVE_ARM, projection, 17));
        state.clear();
        assertTrue(state.desired().isEmpty());
        assertTrue(state.movementControl().isEmpty());
    }

    private static AstralViewPayload payload(
            AstralViewPayload.Action action,
            UUID projectionId,
            int entityId
    ) {
        return new AstralViewPayload(ArcanaProtocol.VERSION, action, projectionId, entityId);
    }
}
