package dev.gustavopere.blackarcana.integration.eidolon;

import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class EidolonIntegrationBridgeTest {
    @Test
    void missingModFailsClosedWithoutCallingOptionalProbe() {
        var bridge = EidolonIntegrationBridge.probe(false, "not-loaded", () -> {
            throw new AssertionError("optional probe must not run when Eidolon is absent");
        });

        assertEquals(EidolonIntegrationIds.MOD_ID, bridge.integrationId());
        assertEquals(ArcanaIntegrationAvailability.MISSING_MOD, bridge.availability());
        assertFalse(bridge.available());
        assertTrue(bridge.capabilities().isEmpty());
    }

    @Test
    void registeredProbeAdvertisesOnlyRitualHost() {
        var bridge = EidolonIntegrationBridge.probe(true, "1.21.1-0.5.0.2", () -> true);

        assertEquals(ArcanaIntegrationAvailability.AVAILABLE, bridge.availability());
        assertTrue(bridge.available());
        assertEquals("1.21.1-0.5.0.2", bridge.implementationVersion());
        assertEquals(Set.of(ArcanaIntegrationCapability.RITUAL_HOST), bridge.capabilities());
    }

    @Test
    void missingRegistrationIsApiIncompatibleAndAdvertisesNothing() {
        var bridge = EidolonIntegrationBridge.probe(true, "1.21.1-0.5.0.2", () -> false);

        assertEquals(ArcanaIntegrationAvailability.API_INCOMPATIBLE, bridge.availability());
        assertFalse(bridge.available());
        assertTrue(bridge.capabilities().isEmpty());
        assertTrue(bridge.diagnostic().contains("probe ritual was not registered"));
    }

    @Test
    void linkageFailureBecomesApiIncompatible() {
        var bridge = EidolonIntegrationBridge.probe(true, "1.21.1-0.5.0.2", () -> {
            throw new NoClassDefFoundError("simulated-eidolon-api-drift");
        });

        assertEquals(ArcanaIntegrationAvailability.API_INCOMPATIBLE, bridge.availability());
        assertFalse(bridge.available());
        assertTrue(bridge.capabilities().isEmpty());
        assertTrue(bridge.diagnostic().contains("NoClassDefFoundError"));
    }
}
