package dev.gustavopere.blackarcana.content.noetic;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Bounded server-owned registry for Noetic observation sessions. */
public final class NoeticObservationRuntime {
    public enum StartResult {
        STARTED,
        VIEWER_ALREADY_ACTIVE,
        GLOBAL_LIMIT,
        INVALID_DURATION
    }

    private final int maxActiveSessions;
    private final Map<UUID, NoeticObservationSession> sessionsByViewer = new LinkedHashMap<>();

    public NoeticObservationRuntime(int maxActiveSessions) {
        if (maxActiveSessions <= 0 || maxActiveSessions > NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS) {
            throw new IllegalArgumentException("Noetic active-session limit exceeds the hard ceiling");
        }
        this.maxActiveSessions = maxActiveSessions;
    }

    public synchronized StartResult start(
            UUID viewerId,
            UUID targetId,
            NoeticObservationKind kind,
            long nowTick,
            int durationTicks
    ) {
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(targetId, "targetId");
        Objects.requireNonNull(kind, "kind");
        if (nowTick < 0L) throw new IllegalArgumentException("Noetic observation tick must be non-negative");
        if (durationTicks <= 0 || durationTicks > NoeticSafetyCeilings.MAX_DURATION_TICKS) {
            return StartResult.INVALID_DURATION;
        }
        if (sessionsByViewer.containsKey(viewerId)) return StartResult.VIEWER_ALREADY_ACTIVE;
        if (sessionsByViewer.size() >= maxActiveSessions) return StartResult.GLOBAL_LIMIT;

        final long expiresAtTick;
        try {
            expiresAtTick = Math.addExact(nowTick, durationTicks);
        } catch (ArithmeticException overflow) {
            return StartResult.INVALID_DURATION;
        }
        sessionsByViewer.put(viewerId,
                new NoeticObservationSession(viewerId, targetId, kind, nowTick, expiresAtTick));
        return StartResult.STARTED;
    }

    public synchronized Optional<NoeticObservationSession> session(UUID viewerId) {
        Objects.requireNonNull(viewerId, "viewerId");
        return Optional.ofNullable(sessionsByViewer.get(viewerId));
    }

    public synchronized int activeCount() {
        return sessionsByViewer.size();
    }

    public synchronized boolean close(UUID viewerId, NoeticObservationSession.CloseReason reason) {
        Objects.requireNonNull(viewerId, "viewerId");
        Objects.requireNonNull(reason, "reason");
        NoeticObservationSession session = sessionsByViewer.remove(viewerId);
        return session != null && session.close(reason);
    }

    public synchronized boolean clearViewer(UUID viewerId, NoeticObservationSession.CloseReason reason) {
        return close(viewerId, reason);
    }

    public synchronized int clearTarget(UUID targetId) {
        Objects.requireNonNull(targetId, "targetId");
        List<UUID> viewers = new ArrayList<>();
        for (Map.Entry<UUID, NoeticObservationSession> entry : sessionsByViewer.entrySet()) {
            if (entry.getValue().targetId().equals(targetId)) viewers.add(entry.getKey());
        }
        int closed = 0;
        for (UUID viewerId : viewers) {
            if (close(viewerId, NoeticObservationSession.CloseReason.TARGET_UNAVAILABLE)) closed++;
        }
        return closed;
    }

    public synchronized int expire(long nowTick) {
        if (nowTick < 0L) throw new IllegalArgumentException("Noetic observation tick must be non-negative");
        List<UUID> expiredViewers = new ArrayList<>();
        for (Map.Entry<UUID, NoeticObservationSession> entry : sessionsByViewer.entrySet()) {
            if (entry.getValue().expiredAt(nowTick)) expiredViewers.add(entry.getKey());
        }
        int closed = 0;
        for (UUID viewerId : expiredViewers) {
            if (close(viewerId, NoeticObservationSession.CloseReason.EXPIRED)) closed++;
        }
        return closed;
    }

    public synchronized int clearForServerStop() {
        List<NoeticObservationSession> sessions = new ArrayList<>(sessionsByViewer.values());
        sessionsByViewer.clear();
        int closed = 0;
        for (NoeticObservationSession session : sessions) {
            if (session.close(NoeticObservationSession.CloseReason.SERVER_STOP)) closed++;
        }
        return closed;
    }
}
