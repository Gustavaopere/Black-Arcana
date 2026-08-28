package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.Collection;
import java.util.Objects;

/**
 * Canonical admission route for actual terrain work: cast-level policy, declared
 * per-spell bounds, loaded-chunk guard and cumulative per-cast budget.
 */
public final class WorldEffectAdmissionService {
    private final ConfigurableWorldEffectPolicy policy;
    private final LoadedChunkGuard chunkGuard;
    private final WorldEffectBudgetLedger budgetLedger;

    public WorldEffectAdmissionService(
        ConfigurableWorldEffectPolicy policy,
        LoadedChunkGuard chunkGuard,
        WorldEffectBudgetLedger budgetLedger
    ) {
        this.policy = Objects.requireNonNull(policy, "policy");
        this.chunkGuard = Objects.requireNonNull(chunkGuard, "chunkGuard");
        this.budgetLedger = Objects.requireNonNull(budgetLedger, "budgetLedger");
    }

    public ArcanaDecision authorize(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits
    ) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(chunks, "chunks");
        if (!request.spell().requestsWorldMutation()) {
            return ArcanaDecision.deny(
                "world_mutation_not_declared",
                "Effect attempted world mutation without declaring it in the spell definition");
        }

        ArcanaDecision policyDecision = policy.authorize(request, target);
        if (!policyDecision.allowed()) return policyDecision;

        WorldEffectProfile profile = policy.profileFor(request.spell().id()).orElse(null);
        if (profile == null) {
            return ArcanaDecision.deny("world_profile_missing", "World-mutating spell has no safety profile");
        }
        if (requestedUnits <= 0 || requestedUnits > profile.maxAffectedUnits()) {
            return ArcanaDecision.deny(
                "world_effect_declared_budget",
                "Requested work exceeds the spell's declared world-effect bound");
        }

        ArcanaDecision chunksDecision = chunkGuard.authorize(chunks);
        if (!chunksDecision.allowed()) return chunksDecision;

        return budgetLedger.tryConsume(request.castId(), requestedUnits, request.context().serverTick());
    }
}
