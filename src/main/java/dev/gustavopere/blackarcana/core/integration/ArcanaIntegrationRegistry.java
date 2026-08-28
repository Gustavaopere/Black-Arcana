package dev.gustavopere.blackarcana.core.integration;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Pattern;

/** Registry for optional integration descriptors. Gameplay capability checks fail closed. */
public final class ArcanaIntegrationRegistry {
    public static final int MAX_INTEGRATIONS = 64;
    private static final Pattern ID = Pattern.compile("[a-z0-9_.-]{1,64}");

    private final Map<String, ArcanaIntegration> integrations = new LinkedHashMap<>();

    public synchronized void register(ArcanaIntegration integration) {
        Objects.requireNonNull(integration, "integration");
        String id = validatedId(integration.integrationId());
        if (integrations.size() >= MAX_INTEGRATIONS) {
            throw new IllegalStateException("integration registry capacity exceeded");
        }
        if (integrations.containsKey(id)) {
            throw new IllegalArgumentException("duplicate integration id: " + id);
        }

        ArcanaIntegrationAvailability availability = Objects.requireNonNull(
            integration.availability(), "integration availability");
        if (integration.available() != availability.usable()) {
            throw new IllegalArgumentException("integration availability flags disagree: " + id);
        }
        String version = Objects.requireNonNull(integration.implementationVersion(), "implementationVersion");
        if (version.isBlank()) {
            throw new IllegalArgumentException("integration version cannot be blank: " + id);
        }
        Objects.requireNonNull(integration.capabilities(), "integration capabilities");
        Objects.requireNonNull(integration.diagnostic(), "integration diagnostic");
        integrations.put(id, integration);
    }

    public synchronized Optional<ArcanaIntegration> find(String integrationId) {
        return Optional.ofNullable(integrations.get(validatedId(integrationId)));
    }

    public synchronized ArcanaDecision requireCapability(
        String integrationId,
        ArcanaIntegrationCapability capability
    ) {
        Objects.requireNonNull(capability, "capability");
        String id = validatedId(integrationId);
        ArcanaIntegration integration = integrations.get(id);
        if (integration == null) {
            return ArcanaDecision.deny(
                "integration_missing",
                "Required integration is not registered: " + id);
        }
        if (!integration.available()) {
            String detail = integration.diagnostic().isBlank()
                ? "Integration is unavailable: " + id + " (" + integration.availability() + ")"
                : integration.diagnostic();
            return ArcanaDecision.deny("integration_unavailable", detail);
        }
        if (!integration.capabilities().contains(capability)) {
            return ArcanaDecision.deny(
                "integration_capability_missing",
                "Integration " + id + " does not provide " + capability);
        }
        return ArcanaDecision.allow();
    }

    public synchronized List<IntegrationSnapshot> snapshot() {
        List<IntegrationSnapshot> result = new ArrayList<>(integrations.size());
        integrations.values().forEach(integration -> result.add(new IntegrationSnapshot(
            integration.integrationId(),
            integration.availability(),
            integration.implementationVersion(),
            Set.copyOf(integration.capabilities()),
            integration.diagnostic())));
        return List.copyOf(result);
    }

    public synchronized int size() {
        return integrations.size();
    }

    private static String validatedId(String integrationId) {
        Objects.requireNonNull(integrationId, "integrationId");
        if (!ID.matcher(integrationId).matches()) {
            throw new IllegalArgumentException("invalid integration id: " + integrationId);
        }
        return integrationId;
    }

    public record IntegrationSnapshot(
        String integrationId,
        ArcanaIntegrationAvailability availability,
        String implementationVersion,
        Set<ArcanaIntegrationCapability> capabilities,
        String diagnostic
    ) {
        public IntegrationSnapshot {
            integrationId = validatedId(integrationId);
            Objects.requireNonNull(availability, "availability");
            Objects.requireNonNull(implementationVersion, "implementationVersion");
            Objects.requireNonNull(capabilities, "capabilities");
            Objects.requireNonNull(diagnostic, "diagnostic");
            if (implementationVersion.isBlank()) {
                throw new IllegalArgumentException("implementationVersion cannot be blank");
            }
            capabilities = Set.copyOf(capabilities);
        }
    }
}
