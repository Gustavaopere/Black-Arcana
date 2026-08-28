package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

/**
 * Canonical server-side admission route for hostile/control interactions with entities.
 * Core PvP/team/boss limits are evaluated before optional claim/protection adapters.
 */
public final class EntityInteractionAdmissionService {
    private final DefaultEntityInteractionPolicy entityPolicy;
    private final ProtectionAdapterRegistry protectionAdapters;

    public EntityInteractionAdmissionService(
        DefaultEntityInteractionPolicy entityPolicy,
        ProtectionAdapterRegistry protectionAdapters
    ) {
        this.entityPolicy = Objects.requireNonNull(entityPolicy, "entityPolicy");
        this.protectionAdapters = Objects.requireNonNull(protectionAdapters, "protectionAdapters");
    }

    public EntityInteractionAuthorization authorize(
        EntityInteractionType type,
        EntityProtectionFacts facts,
        ProtectionQuery query
    ) {
        Objects.requireNonNull(type, "type");
        Objects.requireNonNull(facts, "facts");
        Objects.requireNonNull(query, "query");
        if (query.interactionType() != type) {
            return EntityInteractionAuthorization.deny(
                "protection_query_mismatch",
                "Protection query interaction type does not match the requested effect",
                facts.boss() ? EntityEffectLimits.bossSafeDefaults() : EntityEffectLimits.standard());
        }

        EntityInteractionAuthorization base = entityPolicy.authorize(type, facts);
        if (!base.decision().allowed()) return base;

        ArcanaDecision external = protectionAdapters.authorize(query);
        if (!external.allowed()) {
            return EntityInteractionAuthorization.deny(
                external.code(),
                external.detail(),
                base.limits());
        }
        return base;
    }
}
