package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Tracks the last server-authored Borrowed Sight presentation for each bounded viewer slot. */
public final class NoeticViewTransitionTracker {
    private final int maxTrackedViewers;
    private final Map<UUID, Desired> tracked = new LinkedHashMap<>();

    public NoeticViewTransitionTracker(int maxTrackedViewers) {
        if (maxTrackedViewers < 1) {
            throw new IllegalArgumentException("Noetic view tracker capacity must be positive");
        }
        this.maxTrackedViewers = maxTrackedViewers;
    }

    public synchronized List<NoeticViewPayload> reconcile(UUID viewerId, Optional<Desired> desiredState) {
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(desiredState, "desiredState");

        Desired current = tracked.get(viewerId);
        Desired desired = desiredState.orElse(null);
        if (Objects.equals(current, desired)) {
            return List.of();
        }

        if (current == null) {
            if (desired == null || tracked.size() >= maxTrackedViewers) {
                return List.of();
            }
            tracked.put(viewerId, desired);
            return List.of(payload(NoeticViewPayload.Action.BEGIN, desired));
        }

        if (desired == null) {
            tracked.remove(viewerId);
            return List.of(payload(NoeticViewPayload.Action.END, current));
        }

        tracked.put(viewerId, desired);
        return List.of(
                payload(NoeticViewPayload.Action.END, current),
                payload(NoeticViewPayload.Action.BEGIN, desired));
    }

    public synchronized int trackedCount() {
        return tracked.size();
    }

    private static NoeticViewPayload payload(NoeticViewPayload.Action action, Desired desired) {
        return new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                action,
                desired.kind(),
                desired.targetEntityId());
    }

    public record Desired(NoeticObservationKind kind, int targetEntityId) {
        public Desired {
            Objects.requireNonNull(kind, "kind");
            if (kind != NoeticObservationKind.BORROWED_SIGHT) {
                throw new IllegalArgumentException("Noetic view desired state currently supports Borrowed Sight only: " + kind);
            }
            if (targetEntityId < 0) {
                throw new IllegalArgumentException("Noetic view target entity id must be non-negative");
            }
        }
    }
}
