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

    public ArcanaDecision replace(
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

        ArcanaDecision admitted = admission.authorize(request, target, List.of(chunk), 1);
        if (!admitted.allowed()) return admitted;

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
