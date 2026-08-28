package dev.gustavopere.blackarcana.integration.eidolon;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;

import java.util.Objects;
import java.util.Set;
import java.util.function.BooleanSupplier;

/**
 * Server-visible descriptor for the Eidolon 1.21.1 ritual host.
 *
 * <p>This descriptor intentionally contains no Eidolon binary types. The optional
 * bootstrap supplies the actual registry probe only after NeoForge confirms the
 * provider mod is loaded, preserving a safe core-only classloading path.</p>
 */
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

    public static EidolonIntegrationBridge probe(
        boolean modLoaded,
        String version,
        BooleanSupplier ritualRegisteredProbe
    ) {
        if (!modLoaded) {
            return new EidolonIntegrationBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "Eidolon: Repraised is not loaded");
        }
        Objects.requireNonNull(ritualRegisteredProbe, "ritualRegisteredProbe");
        try {
            if (!ritualRegisteredProbe.getAsBoolean()) {
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
