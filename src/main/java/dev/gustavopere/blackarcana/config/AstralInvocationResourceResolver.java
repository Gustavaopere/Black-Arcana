package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Objects;
import java.util.Optional;

/**
 * Resolves the explicit server-owned Astral invocation configuration against one server runtime's
 * exact provider-native resource authority.
 *
 * <p>This resolver is deliberately side-effect free. It does not install Astral Severance, select
 * a fallback resource, derive gameplay values, or fill any missing progression/upkeep authority.</p>
 */
public final class AstralInvocationResourceResolver {
    public static final String INVOCATION_NOT_CONFIGURED = "astral_invocation_not_configured";
    public static final String RESOURCE_PROVIDER_MISSING = "astral_resource_provider_missing";

    private AstralInvocationResourceResolver() { }

    public static Resolution resolve(ArcanaServerRuntime runtime) {
        ArcanaServerRuntime checkedRuntime = Objects.requireNonNull(runtime, "runtime");
        Optional<AstralInvocationDataDefinition.Invocation> invocation =
                AstralInvocationConfigAuthority.current();
        if (invocation.isEmpty()) {
            return Resolution.denied(ArcanaDecision.deny(
                    INVOCATION_NOT_CONFIGURED,
                    "Astral Severance has no explicit server-owned invocation profile"));
        }

        AstralInvocationDataDefinition.Invocation configured = invocation.orElseThrow();
        String resourceId = configured.cost().resourceId();
        Optional<ResourceCostProvider> provider = checkedRuntime.resourceCosts().resolve(resourceId);
        if (provider.isEmpty()) {
            return Resolution.denied(ArcanaDecision.deny(
                    RESOURCE_PROVIDER_MISSING,
                    "No resource cost provider is registered for " + resourceId));
        }

        return Resolution.resolved(configured, provider.orElseThrow());
    }

    public record Resolution(
            ArcanaDecision decision,
            Optional<AstralInvocationDataDefinition.Invocation> invocation,
            Optional<ResourceCostProvider> resourceProvider
    ) {
        public Resolution {
            Objects.requireNonNull(decision, "decision");
            invocation = Objects.requireNonNull(invocation, "invocation");
            resourceProvider = Objects.requireNonNull(resourceProvider, "resourceProvider");

            if (decision.allowed()) {
                if (invocation.isEmpty() || resourceProvider.isEmpty()) {
                    throw new IllegalArgumentException("allowed Astral resource resolution must be complete");
                }
                String configuredResource = invocation.orElseThrow().cost().resourceId();
                String providerResource = resourceProvider.orElseThrow().resourceId();
                if (!configuredResource.equals(providerResource)) {
                    throw new IllegalArgumentException(
                            "resolved Astral resource provider does not own configured resource " + configuredResource);
                }
            } else if (invocation.isPresent() || resourceProvider.isPresent()) {
                throw new IllegalArgumentException("denied Astral resource resolution cannot expose partial authority");
            }
        }

        private static Resolution denied(ArcanaDecision decision) {
            ArcanaDecision checked = Objects.requireNonNull(decision, "decision");
            if (checked.allowed()) {
                throw new IllegalArgumentException("denied resolution requires a denial decision");
            }
            return new Resolution(checked, Optional.empty(), Optional.empty());
        }

        private static Resolution resolved(
                AstralInvocationDataDefinition.Invocation invocation,
                ResourceCostProvider resourceProvider
        ) {
            return new Resolution(
                    ArcanaDecision.allow(),
                    Optional.of(Objects.requireNonNull(invocation, "invocation")),
                    Optional.of(Objects.requireNonNull(resourceProvider, "resourceProvider")));
        }
    }
}
