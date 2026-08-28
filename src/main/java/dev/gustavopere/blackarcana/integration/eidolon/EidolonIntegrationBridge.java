package dev.gustavopere.blackarcana.integration.eidolon;

import alexthw.eidolon_repraised.registries.RitualRegistry;
import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;

import java.util.Objects;
import java.util.Set;

/** Server-visible descriptor for the public Eidolon 1.21.1 ritual host. */
public final class EidolonIntegrationBridge implements ArcanaIntegration {
    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;

    private EidolonIntegrationBridge(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = normalizeVersion(version);
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
    }

    public static EidolonIntegrationBridge probe(boolean modLoaded, String version) {
        if (!modLoaded) {
            return new EidolonIntegrationBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "Eidolon: Repraised is not loaded");
        }
        try {
            boolean registered = EidolonRitualRegistration.isRegistered()
                && RitualRegistry.find(EidolonIntegrationIds.PROBE_RITUAL_ID) instanceof EidolonArcanaProbeRitual;
            if (!registered) {
                return new EidolonIntegrationBridge(
                    ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                    version,
                    "Eidolon ritual host is present but the Black Arcana probe ritual was not registered");
            }
            return new EidolonIntegrationBridge(
                ArcanaIntegrationAvailability.AVAILABLE,
                version,
                "");
        } catch (RuntimeException | LinkageError failure) {
            return new EidolonIntegrationBridge(
                ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version,
                "Eidolon 1.21.1 ritual API probe failed: " + failure.getClass().getSimpleName());
        }
    }

    @Override public String integrationId() { return EidolonIntegrationIds.MOD_ID; }
    @Override public boolean available() { return availability.usable(); }
    @Override public String implementationVersion() { return version; }
    @Override public ArcanaIntegrationAvailability availability() { return availability; }
    @Override public String diagnostic() { return diagnostic; }

    @Override
    public Set<ArcanaIntegrationCapability> capabilities() {
        return available() ? Set.of(ArcanaIntegrationCapability.RITUAL_HOST) : Set.of();
    }

    private static String normalizeVersion(String version) {
        if (version == null || version.isBlank()) return "unknown";
        return version.length() > 96 ? version.substring(0, 96) : version;
    }
}
