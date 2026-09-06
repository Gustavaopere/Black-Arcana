package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RadialToggleInputTest {
    @Test
    void toggleOpenKeyRequestsCloseButHoldReleaseRemainsSeparate() {
        assertTrue(BlackArcanaRadialScreen.shouldCloseFromOpenKey(
                BlackArcanaClientConfig.RadialBehavior.TOGGLE, true));
        assertFalse(BlackArcanaRadialScreen.shouldCloseFromOpenKey(
                BlackArcanaClientConfig.RadialBehavior.HOLD, true));
        assertFalse(BlackArcanaRadialScreen.shouldCloseFromOpenKey(
                BlackArcanaClientConfig.RadialBehavior.TOGGLE, false));
    }
}
