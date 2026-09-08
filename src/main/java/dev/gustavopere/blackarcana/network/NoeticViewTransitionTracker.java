package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;

import java.util.ArrayList;
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
        return reconcileValidated(viewerId, desiredState.orElse(null));
    }

    public synchronized List<Transition> reconcileAll(Map<UUID, Desired> desiredByViewer) {
        Objects.requireNonNull(desiredByViewer, "desiredByViewer");
        if (desiredByViewer.size() > maxTrackedViewers) {
            throw new IllegalArgumentException("Noetic view snapshot exceeds tracker capacity");
        }

        Map<UUID, Desired> validated = new LinkedHashMap<>(desiredByViewer.size());
        for (Map.Entry<UUID, Desired> entry : desiredByViewer.entrySet()) {
            UUID viewerId = Objects.requireNonNull(entry.getKey(), "viewerId");
            Desired desired = Objects.requireNonNull(entry.getValue(), "desired");
            validated.put(viewerId, desired);
        }

        List<Transition> transitions = new ArrayList<>();
        for (UUID viewerId : List.copyOf(tracked.keySet())) {
            if (!validated.containsKey(viewerId)) {
                addTransitions(transitions, viewerId, reconcileValidated(viewerId, null));
            }
        }
        for (Map.Entry<UUID, Desired> entry : validated.entrySet()) {
            addTransitions(transitions, entry.getKey(), reconcileValidated(entry.getKey(), entry.getValue()));
        }
        return List.copyOf(transitions);
    }

    public synchronized int trackedCount() {
        return tracked.size();
    }

    private List<NoeticViewPayload> reconcileValidated(UUID viewerId, Desired desired) {
        Desired current = tracked.get(viewerId);
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

    private static void addTransitions(List<Transition> transitions, UUID viewerId, List<NoeticViewPayload> payloads) {
        for (NoeticViewPayload payload : payloads) {
            transitions.add(new Transition(viewerId, payload));
        }
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

    public record Transition(UUID viewerId, NoeticViewPayload payload) {
        public Transition {
            Objects.requireNonNull(viewerId, "viewerId");
            Objects.requireNonNull(payload, "payload");
        }
    }
}
