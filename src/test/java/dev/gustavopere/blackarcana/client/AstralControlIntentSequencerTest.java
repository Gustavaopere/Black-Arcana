package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralControlIntentSequencerTest {
    private static final double EPSILON = 1.0E-6D;

    @Test
    void coalescesMultipleLookFramesIntoOneLookOnlyTickIntent() {
        AstralControlIntentSequencer sequencer = new AstralControlIntentSequencer();
        UUID projection = UUID.randomUUID();

        sequencer.captureLook(projection, 2.0D, -1.0D, 0.5D, false);
        sequencer.captureLook(projection, 1.0D, 2.0D, 0.5D, false);

        AstralMoveIntentPayload payload = sequencer.capture(projection, 0.0D, 0.0D, 0.0D).orElseThrow();
        double degreesPerRawUnit = AstralControlIntentSequencer.degreesPerRawMouseUnit(0.5D);
        assertEquals(1L, payload.sequence());
        assertEquals(3.0D * degreesPerRawUnit, payload.yawDeltaDegrees(), EPSILON);
        assertEquals(1.0D * degreesPerRawUnit, payload.pitchDeltaDegrees(), EPSILON);
        assertTrue(sequencer.capture(projection, 0.0D, 0.0D, 0.0D).isEmpty(),
                "drained look input must not replay on the next client tick");
    }

    @Test
    void movementAndLookShareOneMonotonicIntentSequence() {
        AstralControlIntentSequencer sequencer = new AstralControlIntentSequencer();
        UUID projection = UUID.randomUUID();

        sequencer.captureLook(projection, 4.0D, 2.0D, 0.75D, true);
        AstralMoveIntentPayload first = sequencer.capture(projection, 1.0D, 0.0D, -1.0D).orElseThrow();
        AstralMoveIntentPayload second = sequencer.capture(projection, 0.0D, 1.0D, 0.0D).orElseThrow();

        double degreesPerRawUnit = AstralControlIntentSequencer.degreesPerRawMouseUnit(0.75D);
        assertEquals(1L, first.sequence());
        assertEquals(2L, second.sequence());
        assertEquals(4.0D * degreesPerRawUnit, first.yawDeltaDegrees(), EPSILON);
        assertEquals(-2.0D * degreesPerRawUnit, first.pitchDeltaDegrees(), EPSILON,
                "invert-Y must be reflected in the bounded client look intent");
        assertEquals(0.0F, second.yawDeltaDegrees());
        assertEquals(0.0F, second.pitchDeltaDegrees());
    }

    @Test
    void projectionSwitchDropsPendingLookFromPreviousExactSession() {
        AstralControlIntentSequencer sequencer = new AstralControlIntentSequencer();
        UUID firstProjection = UUID.randomUUID();
        UUID secondProjection = UUID.randomUUID();

        sequencer.captureLook(firstProjection, 20.0D, 20.0D, 1.0D, false);
        AstralMoveIntentPayload payload = sequencer.capture(secondProjection, 0.0D, 0.0D, 1.0D).orElseThrow();

        assertEquals(secondProjection, payload.projectionId());
        assertEquals(1L, payload.sequence());
        assertEquals(0.0F, payload.yawDeltaDegrees());
        assertEquals(0.0F, payload.pitchDeltaDegrees());
    }

    @Test
    void neutralBodySensitivityProducesExactlyZeroVanillaTurnFactor() {
        double neutral = AstralControlIntentSequencer.PHYSICAL_BODY_NEUTRAL_SENSITIVITY;
        double vanillaBase = neutral * 0.6F + 0.2F;
        assertEquals(0.0D, vanillaBase, 0.0D,
                "server-armed Astral look redirect must not rotate the physical client body");
    }
}
