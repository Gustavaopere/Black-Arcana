package dev.gustavopere.blackarcana.core.integration;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;

import java.util.Objects;

/** Explicit fail-closed descriptor for a missing or incompatible optional provider. */
public record UnavailableOptionalIntegration(
    String integrationId,
    ArcanaIntegrationAvailability availability,
    String implementationVersion,
    String diagnostic
) implements ArcanaIntegration {
    public UnavailableOptionalIntegration {
        Objects.requireNonNull(integrationId, "integrationId");
        Objects.requireNonNull(availability, "availability");
        Objects.requireNonNull(implementationVersion, "implementationVersion");
        Objects.requireNonNull(diagnostic, "diagnostic");
        if (integrationId.isBlank()) throw new IllegalArgumentException("integrationId cannot be blank");
        if (availability.usable()) throw new IllegalArgumentException("unavailable descriptor cannot be AVAILABLE");
        if (implementationVersion.isBlank()) throw new IllegalArgumentException("implementationVersion cannot be blank");
        if (diagnostic.isBlank()) throw new IllegalArgumentException("diagnostic cannot be blank");
    }

    @Override
    public boolean available() {
        return false;
    }
}
