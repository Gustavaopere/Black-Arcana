package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NoeticViewStateTest {
    @Test
    void onlyCameraObservationKindsCanOwnAClientView() {
        NoeticViewState state = new NoeticViewState();
        UUID target = UUID.randomUUID();

        assertThrows(IllegalArgumentException.class,
                () -> state.activate(NoeticObservationKind.NAMESCRY, target));
        assertThrows(IllegalArgumentException.class,
                () -> state.activate(NoeticObservationKind.OCCULT_APPRAISAL, target));

        assertTrue(state.activate(NoeticObservationKind.BORROWED_SIGHT, target));
        NoeticViewState.Session borrowed = state.session().orElseThrow();
        assertEquals(NoeticObservationKind.BORROWED_SIGHT, borrowed.kind());
        assertEquals(target, borrowed.targetId());

        assertTrue(state.close());
        assertTrue(state.activate(NoeticObservationKind.ASTRAL_SEVERANCE, target));
        assertEquals(NoeticObservationKind.ASTRAL_SEVERANCE, state.session().orElseThrow().kind());
    }

    @Test
    void duplicateActivationTargetReplacementAndCloseAreIdempotent() {
        NoeticViewState state = new NoeticViewState();
        UUID first = UUID.randomUUID();
        UUID second = UUID.randomUUID();

        assertTrue(state.activate(NoeticObservationKind.BORROWED_SIGHT, first));
        assertFalse(state.activate(NoeticObservationKind.BORROWED_SIGHT, first),
                "replayed server start must not restart the same client view");

        assertTrue(state.activate(NoeticObservationKind.BORROWED_SIGHT, second),
                "a server-authorized replacement target must be an explicit state change");
        assertEquals(second, state.session().orElseThrow().targetId());

        assertTrue(state.close());
        assertFalse(state.close(), "replayed close packets must be harmless");
        assertTrue(state.session().isEmpty());
    }
}
