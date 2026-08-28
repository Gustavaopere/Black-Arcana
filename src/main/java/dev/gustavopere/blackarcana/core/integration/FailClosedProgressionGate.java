package dev.gustavopere.blackarcana.core.integration;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;
import java.util.Objects;

/** Requires an optional provider capability before delegating progression checks. */
public final class FailClosedProgressionGate implements ProgressionGate {
    private final ArcanaIntegrationRegistry integrations;
    private final String integrationId;
    private final ArcanaIntegrationCapability capability;
    private final ProgressionGate delegate;

    public FailClosedProgressionGate(
        ArcanaIntegrationRegistry integrations,
        String integrationId,
        ArcanaIntegrationCapability capability,
        ProgressionGate delegate
    ) {
        this.integrations = Objects.requireNonNull(integrations, "integrations");
        this.integrationId = Objects.requireNonNull(integrationId, "integrationId");
        this.capability = Objects.requireNonNull(capability, "capability");
        this.delegate = Objects.requireNonNull(delegate, "delegate");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaDecision provider = integrations.requireCapability(integrationId, capability);
        if (!provider.allowed()) return provider;
        return Objects.requireNonNull(delegate.check(request), "progression decision");
    }
}
