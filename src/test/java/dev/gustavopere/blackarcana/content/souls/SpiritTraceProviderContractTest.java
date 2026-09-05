package dev.gustavopere.blackarcana.content.souls;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SpiritTraceProviderContractTest {
    @Test
    void providerIdsMustBeBoundedNamespacedIdentifiers() {
        assertTrue(SpiritTraceProvider.validProviderId("black_arcana:test_spirit_sight"));
        assertFalse(SpiritTraceProvider.validProviderId("test_spirit_sight"));
        assertFalse(SpiritTraceProvider.validProviderId(""));
        assertFalse(SpiritTraceProvider.validProviderId("A:b"));
        assertFalse(SpiritTraceProvider.validProviderId("a:" + "x".repeat(SpiritTraceProvider.ABSOLUTE_MAX_PROVIDER_ID_LENGTH)));
    }

    @Test
    void queryAndTraceRejectUnboundedOrNonFiniteInput() {
        UUID viewer = UUID.randomUUID();
        new SpiritTraceProvider.Query(viewer, "minecraft:overworld", 1.0D, 2.0D, 3.0D,
            SpiritSightPolicy.ABSOLUTE_MAX_RADIUS);

        assertThrows(IllegalArgumentException.class,
            () -> new SpiritTraceProvider.Query(viewer, "minecraft:overworld", 1.0D, 2.0D, 3.0D,
                SpiritSightPolicy.ABSOLUTE_MAX_RADIUS + 1.0D));
        assertThrows(IllegalArgumentException.class,
            () -> new SpiritTraceProvider.Query(viewer, "minecraft:overworld", Double.NaN, 2.0D, 3.0D, 8.0D));
        assertThrows(IllegalArgumentException.class,
            () -> new SpiritTraceProvider.Trace(UUID.randomUUID(), Double.POSITIVE_INFINITY, 0.0D, 0.0D,
                SpiritSightPolicy.TraceKind.MALUM_SPIRIT, false));
    }
}
