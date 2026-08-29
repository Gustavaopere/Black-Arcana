package dev.gustavopere.blackarcana.integration.curios;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;

import java.util.Objects;

/** Runtime descriptor for the optional Curios hazard-equipment bridge. */
public final class CuriosHazardIntegration implements ArcanaIntegration {
    public static final String MOD_ID = "curios";

    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;

    public CuriosHazardIntegration(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = Objects.requireNonNull(version, "version");
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
    }

    @Override
    public String integrationId() {
        return MOD_ID;
    }

    @Override
    public boolean available() {
        return availability.usable();
    }

    @Override
    public String implementationVersion() {
        return version;
    }

    @Override
    public ArcanaIntegrationAvailability availability() {
        return availability;
    }

    @Override
    public String diagnostic() {
        return diagnostic;
    }
}
