package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class NoeticAstralSeveranceAdmissionTest {
    @Test
    void genericObservedEntityAdmissionCannotStandInForAstralProjection() {
        NoeticObservationFacts loadedNpc = new NoeticObservationFacts(
                true,
                true,
                true,
                true,
                true,
                false,
                false,
                false);

        var decision = NoeticObservationPolicy.authorize(NoeticObservationKind.ASTRAL_SEVERANCE, loadedNpc);

        assertFalse(decision.allowed(),
                "Astral Severance must not borrow arbitrary observed-entity identity from the generic Noetic path");
        assertEquals("noetic_astral_requires_projection_lifecycle", decision.code());
    }
}
