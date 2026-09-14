package dev.gustavopere.blackarcana.network;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Tracks the last server-authored Astral presentation for each bounded viewer slot. */
public final class AstralViewTransitionTracker {
    private final int maxTrackedViewers;
    private final Map<UUID, Desired> tracked = new LinkedHashMap<>();

    public AstralViewTransitionTracker(int maxTrackedViewers) {
        if (maxTrackedViewers < 1) {
            throw new IllegalArgumentException("Astral view tracker capacity must be positive");
        }
        this.maxTrackedViewers = maxTrackedViewers;
    }

    public synchronized List<AstralViewPayload> reconcile(UUID viewerId, Optional<Desired> desiredState) {
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(desiredState, "desiredState");
        return reconcileValidated(viewerId, desiredState.orElse(null));
    }

    public synchronized List<Transition> reconcileAll(Map<UUID, Desired> desiredByViewer) {
        Objects.requireNonNull(desiredByViewer, "desiredByViewer");
        if (desiredByViewer.size() > maxTrackedViewers) {
            throw new IllegalArgumentException("Astral view snapshot exceeds tracker capacity");
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

    private List<AstralViewPayload> reconcileValidated(UUID viewerId, Desired desired) {
        Desired current = tracked.get(viewerId);
        if (Objects.equals(current, desired)) {
            return List.of();
        }

        if (current == null) {
            if (desired == null || tracked.size() >= maxTrackedViewers) {
                return List.of();
            }
            tracked.put(viewerId, desired);
            return List.of(payload(AstralViewPayload.Action.BEGIN, desired));
        }

        if (desired == null) {
            tracked.remove(viewerId);
            return List.of(payload(AstralViewPayload.Action.END, current));
        }

        tracked.put(viewerId, desired);
        return List.of(
                payload(AstralViewPayload.Action.END, current),
                payload(AstralViewPayload.Action.BEGIN, desired));
    }

    private static void addTransitions(List<Transition> transitions, UUID viewerId, List<AstralViewPayload> payloads) {
        for (AstralViewPayload payload : payloads) {
            transitions.add(new Transition(viewerId, payload));
        }
    }

    private static AstralViewPayload payload(AstralViewPayload.Action action, Desired desired) {
        return new AstralViewPayload(
                ArcanaProtocol.VERSION,
                action,
                desired.projectionId(),
                desired.entityId());
    }

    public record Desired(UUID projectionId, int entityId) {
        public Desired {
            Objects.requireNonNull(projectionId, "projectionId");
            if (entityId < 0) {
                throw new IllegalArgumentException("Astral view entity id must be non-negative");
            }
        }
    }

    public record Transition(UUID viewerId, AstralViewPayload payload) {
        public Transition {
            Objects.requireNonNull(viewerId, "viewerId");
            Objects.requireNonNull(payload, "payload");
        }
    }
}
