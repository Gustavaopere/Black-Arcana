package dev.gustavopere.blackarcana.content.forbidden;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Recovery journal for localized-domain sessions. Stage 07 deliberately does not create dynamic dimensions;
 * that avoids orphan dimensions/chunks while retaining a guaranteed participant return path.
 *
 * A session's participant map represents return obligations that are still pending. The owner is required when
 * a session is opened, but may disappear from a later recovery snapshot after being safely settled while other
 * participants remain offline or otherwise unavailable.
 */
public final class InnerDominionSessionJournal {
    public enum OpenResult { OPENED, DUPLICATE_SESSION, NESTED_PARTICIPANT, CAPACITY, INVALID_DURATION }
    public enum SettleResult { PARTICIPANT_SETTLED, SESSION_CLOSED, SESSION_MISSING, PARTICIPANT_MISSING }

    public record ReturnRoute(DomainReturnPoint origin, DomainReturnPoint fallback) {
        public ReturnRoute { Objects.requireNonNull(origin, "origin"); Objects.requireNonNull(fallback, "fallback"); }
    }

    public record Session(UUID sessionId, UUID ownerId, long expiresAtTick, Map<UUID, ReturnRoute> participants) {
        public Session {
            Objects.requireNonNull(sessionId, "sessionId");
            Objects.requireNonNull(ownerId, "ownerId");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
            participants = Map.copyOf(Objects.requireNonNull(participants, "participants"));
            if (participants.isEmpty()) throw new IllegalArgumentException("session must retain at least one recovery obligation");
        }
    }

    private final int maxSessions;
    private final int maxParticipants;
    private final long maxDurationTicks;
    private final Map<UUID, Session> sessions = new LinkedHashMap<>();
    private final Map<UUID, UUID> participantSessions = new LinkedHashMap<>();

    public InnerDominionSessionJournal(int maxSessions, int maxParticipants, long maxDurationTicks) {
        if (maxSessions <= 0 || maxSessions > ForbiddenDomainSafetyCeilings.MAX_ACTIVE_SESSIONS) throw new IllegalArgumentException("maxSessions outside ceiling");
        if (maxParticipants <= 0 || maxParticipants > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) throw new IllegalArgumentException("maxParticipants outside ceiling");
        if (maxDurationTicks <= 0 || maxDurationTicks > ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS) throw new IllegalArgumentException("maxDurationTicks outside ceiling");
        this.maxSessions = maxSessions;
        this.maxParticipants = maxParticipants;
        this.maxDurationTicks = maxDurationTicks;
    }

    public synchronized OpenResult open(UUID sessionId, UUID ownerId, long now, long durationTicks, Map<UUID, ReturnRoute> participants) {
        Objects.requireNonNull(sessionId, "sessionId"); Objects.requireNonNull(ownerId, "ownerId"); Objects.requireNonNull(participants, "participants");
        if (now < 0L || durationTicks <= 0L || durationTicks > maxDurationTicks || participants.isEmpty() || participants.size() > maxParticipants || !participants.containsKey(ownerId)) return OpenResult.INVALID_DURATION;
        if (sessions.containsKey(sessionId)) return OpenResult.DUPLICATE_SESSION;
        if (sessions.size() >= maxSessions) return OpenResult.CAPACITY;
        for (UUID participant : participants.keySet()) {
            Objects.requireNonNull(participant, "participant");
            if (participantSessions.containsKey(participant)) return OpenResult.NESTED_PARTICIPANT;
        }
        long expires = now > Long.MAX_VALUE - durationTicks ? Long.MAX_VALUE : now + durationTicks;
        Session session = new Session(sessionId, ownerId, expires, participants);
        sessions.put(sessionId, session);
        participants.keySet().forEach(id -> participantSessions.put(id, sessionId));
        return OpenResult.OPENED;
    }

    public synchronized Optional<Session> close(UUID sessionId) {
        Session removed = sessions.remove(Objects.requireNonNull(sessionId, "sessionId"));
        if (removed == null) return Optional.empty();
        removed.participants().keySet().forEach(id -> participantSessions.remove(id, sessionId));
        return Optional.of(removed);
    }

    public synchronized SettleResult settleParticipant(UUID sessionId, UUID participantId) {
        Objects.requireNonNull(sessionId, "sessionId");
        Objects.requireNonNull(participantId, "participantId");
        Session session = sessions.get(sessionId);
        if (session == null) return SettleResult.SESSION_MISSING;
        if (!session.participants().containsKey(participantId)) return SettleResult.PARTICIPANT_MISSING;

        participantSessions.remove(participantId, sessionId);
        if (session.participants().size() == 1) {
            sessions.remove(sessionId);
            return SettleResult.SESSION_CLOSED;
        }

        Map<UUID, ReturnRoute> remaining = new LinkedHashMap<>(session.participants());
        remaining.remove(participantId);
        sessions.put(sessionId, new Session(
            session.sessionId(),
            session.ownerId(),
            session.expiresAtTick(),
            remaining));
        return SettleResult.PARTICIPANT_SETTLED;
    }

    /** Returns due recovery obligations without mutating or releasing them. */
    public synchronized List<Session> due(long now) {
        if (now < 0L) throw new IllegalArgumentException("now cannot be negative");
        return sessions.values().stream().filter(s -> s.expiresAtTick() <= now).toList();
    }

    /** Compatibility alias retained for callers that used expiry discovery before recovery became non-destructive. */
    public synchronized List<Session> expire(long now) {
        return due(now);
    }

    public synchronized List<Session> snapshot() { return List.copyOf(sessions.values()); }

    public synchronized int restore(List<Session> snapshots, long now) {
        Objects.requireNonNull(snapshots, "snapshots");
        if (now < 0L) throw new IllegalArgumentException("now cannot be negative");
        sessions.clear(); participantSessions.clear();
        int restored = 0;
        for (Session session : snapshots) {
            if (session == null || sessions.size() >= maxSessions || session.participants().isEmpty() || session.participants().size() > maxParticipants) continue;
            if (sessions.containsKey(session.sessionId())) continue;
            boolean overlap = session.participants().keySet().stream().anyMatch(participantSessions::containsKey);
            if (overlap) continue;
            sessions.put(session.sessionId(), session);
            session.participants().keySet().forEach(id -> participantSessions.put(id, session.sessionId()));
            restored++;
        }
        return restored;
    }

    public synchronized boolean participantActive(UUID participantId) { return participantSessions.containsKey(participantId); }
    public synchronized int activeSessions() { return sessions.size(); }
}
