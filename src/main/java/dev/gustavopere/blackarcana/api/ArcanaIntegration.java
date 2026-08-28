package dev.gustavopere.blackarcana.api;

import java.util.Set;

/**
 * Mod-agnostic descriptor for one optional integration.
 *
 * <p>Implementations may live in adapter packages that reference optional mod
 * APIs, but no optional-mod type is permitted in this contract.</p>
 */
public interface ArcanaIntegration {
    String integrationId();

    boolean available();

    String implementationVersion();

    default ArcanaIntegrationAvailability availability() {
        return available()
            ? ArcanaIntegrationAvailability.AVAILABLE
            : ArcanaIntegrationAvailability.MISSING_MOD;
    }

    default Set<ArcanaIntegrationCapability> capabilities() {
        return Set.of();
    }

    default String diagnostic() {
        return "";
    }
}
