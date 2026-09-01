package dev.gustavopere.blackarcana.core.ritual;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public final class RitualSessionRegistry {
    private final int maxActiveSessions;
    private final Map<RitualActivationId, Session> byActivation = new LinkedHashMap<>();
    private final Map<RitualAnchor, RitualActivationId> byAnchor = new LinkedHashMap<>();

    public RitualSessionRegistry(int maxActiveSessions) {
        if (maxActiveSessions <= 0 || maxActiveSessions > 4_096) {
            throw new IllegalArgumentException("maxActiveSessions outside bounds");
        }
        this.maxActiveSessions = maxActiveSessions;
    }

    boolean hasCapacity() {
        return byActivation.size() < maxActiveSessions;
    }

    boolean anchorBusy(RitualAnchor anchor) {
        return byAnchor.containsKey(Objects.requireNonNull(anchor, "anchor"));
    }

    boolean add(Session session) {
        Objects.requireNonNull(session, "session");
        if (!hasCapacity() || byActivation.containsKey(session.activationId) || byAnchor.containsKey(session.context.anchor())) {
            return false;
        }
        byActivation.put(session.activationId, session);
        byAnchor.put(session.context.anchor(), session.activationId);
        return true;
    }

    Session get(RitualActivationId activationId) {
        return byActivation.get(activationId);
    }

    void remove(RitualActivationId activationId) {
        Session removed = byActivation.remove(activationId);
        if (removed != null) byAnchor.remove(removed.context.anchor(), activationId);
    }

    int size() {
        return byActivation.size();
    }

    List<Session> sessions(int limit) {
        if (limit <= 0) return List.of();
        List<Session> result = new ArrayList<>(Math.min(limit, byActivation.size()));
        for (Session session : byActivation.values()) {
            if (result.size() >= limit) break;
            result.add(session);
        }
        return result;
    }

    static final class Session {
        final RitualDefinition definition;
        final RitualActivationId activationId;
        final RitualContext context;
        final long startedAtTick;
        final long commitAtTick;
        final long completeAtTick;
        RitualSessionState state;

        Session(
                RitualDefinition definition,
                RitualActivationId activationId,
                RitualContext context,
                long startedAtTick,
                long commitAtTick,
                long completeAtTick,
                RitualSessionState state
        ) {
            this.definition = Objects.requireNonNull(definition, "definition");
            this.activationId = Objects.requireNonNull(activationId, "activationId");
            this.context = Objects.requireNonNull(context, "context");
            this.startedAtTick = startedAtTick;
            this.commitAtTick = commitAtTick;
            this.completeAtTick = completeAtTick;
            this.state = Objects.requireNonNull(state, "state");
        }

        RitualSessionSnapshot snapshot() {
            return new RitualSessionSnapshot(
                    definition.id(), activationId, context, startedAtTick, commitAtTick, completeAtTick, state);
        }
    }
}
