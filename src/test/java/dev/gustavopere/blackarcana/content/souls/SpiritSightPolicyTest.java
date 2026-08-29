package dev.gustavopere.blackarcana.content.souls;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SpiritSightPolicyTest {
    @Test
    void onlyExplicitOccultTracesAreVisible() {
        SpiritSightPolicy policy = new SpiritSightPolicy();
        assertTrue(policy.visible(new SpiritSightPolicy.Trace(SpiritSightPolicy.TraceKind.MALUM_SPIRIT, true)));
        assertTrue(policy.visible(new SpiritSightPolicy.Trace(SpiritSightPolicy.TraceKind.BLACK_ARCANA_DOMAIN, true)));
        assertFalse(policy.visible(new SpiritSightPolicy.Trace(SpiritSightPolicy.TraceKind.HIDDEN_PLAYER, true)));
        assertFalse(policy.visible(new SpiritSightPolicy.Trace(SpiritSightPolicy.TraceKind.PRIVATE_CONTAINER, true)));
        assertFalse(policy.visible(new SpiritSightPolicy.Trace(SpiritSightPolicy.TraceKind.EIDOLON_OCCULT, false)));
    }
}
