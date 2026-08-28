package dev.gustavopere.blackarcana.core.integration;

import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class UnavailableOptionalIntegrationTest {
    @Test
    void missingModDescriptorFailsClosed() {
        var integration = new UnavailableOptionalIntegration(
            "example_mod",
            ArcanaIntegrationAvailability.MISSING_MOD,
            "not-loaded",
            "Optional integration mod is not loaded: example_mod");

        assertFalse(integration.available());
        assertEquals(ArcanaIntegrationAvailability.MISSING_MOD, integration.availability());
        assertTrue(integration.capabilities().isEmpty());
    }

    @Test
    void incompatibleDescriptorFailsClosed() {
        var integration = new UnavailableOptionalIntegration(
            "example_mod",
            ArcanaIntegrationAvailability.API_INCOMPATIBLE,
            "1.2.3",
            "server adapter linkage failed: NoClassDefFoundError");

        assertFalse(integration.available());
        assertEquals(ArcanaIntegrationAvailability.API_INCOMPATIBLE, integration.availability());
        assertTrue(integration.capabilities().isEmpty());
    }

    @Test
    void availableStateCannotMasqueradeAsUnavailableDescriptor() {
        assertThrows(IllegalArgumentException.class, () -> new UnavailableOptionalIntegration(
            "example_mod",
            ArcanaIntegrationAvailability.AVAILABLE,
            "1.2.3",
            "should reject"));
    }
}
