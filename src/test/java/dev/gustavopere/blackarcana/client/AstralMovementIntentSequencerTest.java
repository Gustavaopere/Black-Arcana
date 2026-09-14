package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralMovementIntentSequencerTest {
    @Test
    void idleMovementDoesNotConsumeSequence() {
        AstralMovementIntentSequencer sequencer = new AstralMovementIntentSequencer();
        UUID projection = UUID.randomUUID();

        assertTrue(sequencer.capture(projection, 0.0D, 0.0D, 0.0D).isEmpty());
        var payload = sequencer.capture(projection, 0.25D, 0.0D, 1.0D).orElseThrow();

        assertEquals(ArcanaProtocol.VERSION, payload.protocolVersion());
        assertEquals(projection, payload.projectionId());
        assertEquals(1L, payload.sequence());
        assertEquals(0.25D, payload.strafeAxis());
        assertEquals(0.0D, payload.verticalAxis());
        assertEquals(1.0D, payload.forwardAxis());
        assertEquals(0.0F, payload.yawDeltaDegrees());
        assertEquals(0.0F, payload.pitchDeltaDegrees());
    }

    @Test
    void sequenceIsMonotonicWithinOneProjectionAndRestartsForNewIdentity() {
        AstralMovementIntentSequencer sequencer = new AstralMovementIntentSequencer();
        UUID first = UUID.randomUUID();
        UUID second = UUID.randomUUID();

        assertEquals(1L, sequencer.capture(first, 1.0D, 0.0D, 0.0D).orElseThrow().sequence());
        assertEquals(2L, sequencer.capture(first, 0.0D, 1.0D, 0.0D).orElseThrow().sequence());
        assertEquals(1L, sequencer.capture(second, 0.0D, -1.0D, 0.0D).orElseThrow().sequence());
    }

    @Test
    void resetForExactProjectionCannotResetUnrelatedActiveIdentity() {
        AstralMovementIntentSequencer sequencer = new AstralMovementIntentSequencer();
        UUID active = UUID.randomUUID();
        UUID stale = UUID.randomUUID();

        assertEquals(1L, sequencer.capture(active, 1.0D, 0.0D, 0.0D).orElseThrow().sequence());
        sequencer.reset(stale);
        assertEquals(2L, sequencer.capture(active, 1.0D, 0.0D, 0.0D).orElseThrow().sequence());

        sequencer.reset(active);
        assertEquals(1L, sequencer.capture(active, 1.0D, 0.0D, 0.0D).orElseThrow().sequence());
    }
}
