package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Bounded CAS-only route for Black Arcana permanent terrain replacement. */
public final class PermanentBlockMutationGateway {
    private final WorldEffectAdmissionService admission;
    private final WorldMutationProtectionAdapterRegistry protection;
    private final TemporaryBlockBackend backend;

    public PermanentBlockMutationGateway(
        WorldEffectAdmissionService admission,
        WorldMutationProtectionAdapterRegistry protection,
        TemporaryBlockBackend backend
    ) {
        this.admission = Objects.requireNonNull(admission, "admission");
        this.protection = Objects.requireNonNull(protection, "protection");
        this.backend = Objects.requireNonNull(backend, "backend");
    }

    public ArcanaDecision replace(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        ChunkRef chunk,
        TemporaryMutationKey key,
        String replacementState,
        WorldMutationType mutationType,
        WorldMutationClass requestedMutationClass
    ) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(chunk, "chunk");
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(replacementState, "replacementState");
        Objects.requireNonNull(mutationType, "mutationType");
        Objects.requireNonNull(requestedMutationClass, "requestedMutationClass");

        if (requestedMutationClass != WorldMutationClass.LIMITED
            && requestedMutationClass != WorldMutationClass.PERMANENT) {
            return ArcanaDecision.deny(
                "permanent_mutation_class",
                "Permanent mutation gateway accepts only LIMITED or PERMANENT work");
        }
        if (!request.context().dimensionId().equals(key.dimensionId())
            || !chunk.dimensionId().equals(key.dimensionId())) {
            return ArcanaDecision.deny(
                "world_mutation_dimension",
                "Mutation key, chunk and caster context must share a dimension");
        }

        Optional<String> current;
        try {
            current = Objects.requireNonNull(backend.readLoadedState(key), "loaded state");
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("world_backend_failed", "Permanent world state read failed closed");
        }
        if (current.isEmpty()) {
            return ArcanaDecision.deny("world_state_unavailable", "Permanent target chunk is no longer loaded");
        }

        WorldMutationProtectionQuery query = new WorldMutationProtectionQuery(
            request.context().casterId(),
            request.castId(),
            request.spell().id(),
            key,
            mutationType,
            requestedMutationClass);
        ArcanaDecision protectedDecision = protection.authorize(query);
        if (!protectedDecision.allowed()) return protectedDecision;

        ArcanaDecision preflight = admission.preflight(
            request,
            target,
            List.of(chunk),
            1,
            mutationType,
            requestedMutationClass);
        if (!preflight.allowed()) return preflight;

        ArcanaDecision settlementProtection = protection.authorize(query);
        if (!settlementProtection.allowed()) return settlementProtection;

        ArcanaDecision budget = admission.consumeBudget(request, 1);
        if (!budget.allowed()) return budget;

        final boolean replaced;
        try {
            replaced = backend.replaceIfCurrent(key, current.get(), replacementState);
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("world_backend_failed", "Permanent world mutation failed closed");
        }
        if (!replaced) {
            return ArcanaDecision.deny(
                "world_state_changed",
                "Target state changed before permanent mutation applied");
        }
        return ArcanaDecision.allow();
    }
}
