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

    /** Legacy path: keeps evaluating the profile's declared worst-case mutation class. */
    public ArcanaDecision authorize(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits
    ) {
        ArcanaDecision preflight = preflightLegacy(request, target, chunks, requestedUnits);
        if (!preflight.allowed()) return preflight;
        return consumeBudget(request, requestedUnits);
    }

    /** Operation-specific path for adaptive spells such as Black Pyre. */
    public ArcanaDecision authorize(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits,
        WorldMutationClass requestedMutationClass
    ) {
        ArcanaDecision preflight = preflight(request, target, chunks, requestedUnits, requestedMutationClass);
        if (!preflight.allowed()) return preflight;
        return consumeBudget(request, requestedUnits);
    }

    /** Non-consuming operation-specific admission used before mutable protection rechecks. */
    public ArcanaDecision preflight(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits,
        WorldMutationClass requestedMutationClass
    ) {
        return preflightInternal(request, target, chunks, requestedUnits, null,
            Objects.requireNonNull(requestedMutationClass, "requestedMutationClass"));
    }

    /** Same as {@link #preflight(ArcanaCastRequest, ArcanaServices.TargetResolution, Collection, int, WorldMutationClass)}
     * while also verifying the exact registered mutation type. */
    public ArcanaDecision preflight(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits,
        WorldMutationType requestedMutationType,
        WorldMutationClass requestedMutationClass
    ) {
        return preflightInternal(
            request,
            target,
            chunks,
            requestedUnits,
            Objects.requireNonNull(requestedMutationType, "requestedMutationType"),
            Objects.requireNonNull(requestedMutationClass, "requestedMutationClass"));
    }

    private ArcanaDecision preflightLegacy(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits
    ) {
        return preflightInternal(request, target, chunks, requestedUnits, null, null);
    }

    private ArcanaDecision preflightInternal(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        Collection<ChunkRef> chunks,
        int requestedUnits,
        WorldMutationType requestedMutationType,
        WorldMutationClass requestedMutationClass
    ) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(chunks, "chunks");
        if (!request.spell().requestsWorldMutation()) {
            return ArcanaDecision.deny(
                "world_mutation_not_declared",
                "Effect attempted world mutation without declaring it in the spell definition");
        }

        ArcanaDecision policyDecision = requestedMutationClass == null
            ? policy.authorize(request, target)
            : policy.authorize(request, target, requestedMutationClass);
        if (!policyDecision.allowed()) return policyDecision;

        WorldEffectProfile profile = policy.profileFor(request.spell().id()).orElse(null);
        if (profile == null) {
            return ArcanaDecision.deny("world_profile_missing", "World-mutating spell has no safety profile");
        }
        if (requestedMutationType != null && profile.mutationType() != requestedMutationType) {
            return ArcanaDecision.deny(
                "world_effect_mutation_type",
                "Requested mutation type does not match the spell's registered world-effect profile");
        }
        if (requestedUnits <= 0 || requestedUnits > profile.maxAffectedUnits()) {
            return ArcanaDecision.deny(
                "world_effect_declared_budget",
                "Requested work exceeds the spell's declared world-effect bound");
        }

        return chunkGuard.authorize(chunks);
    }

    /** Package-local settlement primitive so gateways can keep protection checks ahead of budget use. */
    ArcanaDecision consumeBudget(ArcanaCastRequest request, int requestedUnits) {
        Objects.requireNonNull(request, "request");
        return budgetLedger.tryConsume(request.castId(), requestedUnits, request.context().serverTick());
    }
}
