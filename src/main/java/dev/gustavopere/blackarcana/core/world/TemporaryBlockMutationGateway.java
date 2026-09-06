package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Only supported core route for Black Arcana-owned temporary block replacement. */
public final class TemporaryBlockMutationGateway {
    public static final long ABSOLUTE_MAX_LIFETIME_TICKS = 20L * 60L * 60L * 24L;

    private final WorldEffectAdmissionService admission;
    private final TemporaryMutationTracker tracker;
    private final TemporaryBlockBackend backend;
    private final long maxLifetimeTicks;

    public TemporaryBlockMutationGateway(
        WorldEffectAdmissionService admission,
        TemporaryMutationTracker tracker,
        TemporaryBlockBackend backend,
        long maxLifetimeTicks
    ) {
        this.admission = Objects.requireNonNull(admission, "admission");
        this.tracker = Objects.requireNonNull(tracker, "tracker");
        this.backend = Objects.requireNonNull(backend, "backend");
        if (maxLifetimeTicks <= 0 || maxLifetimeTicks > ABSOLUTE_MAX_LIFETIME_TICKS) {
            throw new IllegalArgumentException("maxLifetimeTicks outside absolute bounds");
        }
        this.maxLifetimeTicks = maxLifetimeTicks;
    }

    /** Legacy predecessor path; behavior and worst-case profile admission remain unchanged. */
    public ArcanaDecision replace(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        ChunkRef chunk,
        TemporaryMutationKey key,
        String replacementState,
        long expiresAtTick
    ) {
        ArcanaDecision lifetime = validateCommon(request, target, chunk, key, replacementState, expiresAtTick);
        if (!lifetime.allowed()) return lifetime;

        ArcanaDecision admitted = admission.authorize(request, target, List.of(chunk), 1);
        if (!admitted.allowed()) return admitted;
        return settleTrackedReplacement(request, key, replacementState, expiresAtTick);
    }

    /**
     * Protected operation-specific path for adaptive world-effect spells. Protection is checked
     * before non-consuming world preflight and immediately before the single budget settlement.
     */
    public ArcanaDecision replaceProtected(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        ChunkRef chunk,
        TemporaryMutationKey key,
        String replacementState,
        long expiresAtTick,
        WorldMutationType mutationType,
        WorldMutationProtectionAdapterRegistry protection
    ) {
        ArcanaDecision lifetime = validateCommon(request, target, chunk, key, replacementState, expiresAtTick);
        if (!lifetime.allowed()) return lifetime;
        Objects.requireNonNull(mutationType, "mutationType");
        Objects.requireNonNull(protection, "protection");

        if (!request.context().dimensionId().equals(key.dimensionId())
            || !chunk.dimensionId().equals(key.dimensionId())) {
            return ArcanaDecision.deny(
                "world_mutation_dimension",
                "Mutation key, chunk and caster context must share a dimension");
        }

        WorldMutationProtectionQuery query = new WorldMutationProtectionQuery(
            request.context().casterId(),
            request.castId(),
            request.spell().id(),
            key,
            mutationType,
            WorldMutationClass.TEMPORARY);
        ArcanaDecision protectedDecision = protection.authorize(query);
        if (!protectedDecision.allowed()) return protectedDecision;

        ArcanaDecision preflight = admission.preflight(
            request,
            target,
            List.of(chunk),
            1,
            mutationType,
            WorldMutationClass.TEMPORARY);
        if (!preflight.allowed()) return preflight;

        ArcanaDecision settlementProtection = protection.authorize(query);
        if (!settlementProtection.allowed()) return settlementProtection;

        ArcanaDecision budget = admission.consumeBudget(request, 1);
        if (!budget.allowed()) return budget;
        return settleTrackedReplacement(request, key, replacementState, expiresAtTick);
    }

    private ArcanaDecision validateCommon(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        ChunkRef chunk,
        TemporaryMutationKey key,
        String replacementState,
        long expiresAtTick
    ) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(chunk, "chunk");
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(replacementState, "replacementState");

        long now = request.context().serverTick();
        if (expiresAtTick <= now || expiresAtTick - now > maxLifetimeTicks) {
            return ArcanaDecision.deny(
                "temporary_lifetime",
                "Temporary mutation lifetime is outside the configured bound");
        }
        return ArcanaDecision.allow();
    }

    private ArcanaDecision settleTrackedReplacement(
        ArcanaCastRequest request,
        TemporaryMutationKey key,
        String replacementState,
        long expiresAtTick
    ) {
        Optional<String> current;
        try {
            current = Objects.requireNonNull(backend.readLoadedState(key), "loaded state");
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("world_backend_failed", "Temporary world state read failed closed");
        }
        if (current.isEmpty()) {
            return ArcanaDecision.deny("world_state_unavailable", "Temporary target chunk is no longer loaded");
        }

        TemporaryMutationTracker.RegistrationResult registration = tracker.register(
            key,
            request.context().casterId(),
            request.castId(),
            current.get(),
            replacementState,
            expiresAtTick);
        if (!registration.decision().allowed()) return registration.decision();

        final boolean replaced;
        try {
            replaced = backend.replaceIfCurrent(key, current.get(), replacementState);
        } catch (RuntimeException | LinkageError failure) {
            // Keep the restoration record: the backend may have mutated before failing.
            return ArcanaDecision.deny("world_backend_failed", "Temporary world mutation failed closed");
        }
        if (!replaced) {
            tracker.rollbackRegistration(registration);
            return ArcanaDecision.deny("world_state_changed", "Target state changed before temporary mutation applied");
        }
        return ArcanaDecision.allow();
    }
}
