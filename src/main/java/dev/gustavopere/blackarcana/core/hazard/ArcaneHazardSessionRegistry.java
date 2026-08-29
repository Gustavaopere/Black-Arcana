package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Per-server bounded registry for active hazard sessions. */
public final class ArcaneHazardSessionRegistry {
    public static final int ABSOLUTE_MAX_SESSIONS = 16_384;

    public record OpenResult(boolean opened, Optional<ArcaneHazardSession> session, String code) {
        public OpenResult {
            Objects.requireNonNull(session, "session");
            Objects.requireNonNull(code, "code");
            if (opened != session.isPresent()) {
                throw new IllegalArgumentException("opened state must match session presence");
            }
            if (opened && !code.isEmpty()) {
                throw new IllegalArgumentException("successful open result cannot have a denial code");
            }
            if (!opened && code.isBlank()) {
                throw new IllegalArgumentException("denied open result requires a code");
            }
        }

        static OpenResult success(ArcaneHazardSession session) {
            return new OpenResult(true, Optional.of(session), "");
        }

        static OpenResult denied(String code) {
            return new OpenResult(false, Optional.empty(), code);
        }
    }

    private final int maxSessions;
    private final Map<ArcanaCastId, ArcaneHazardSession> sessions = new LinkedHashMap<>();

    public ArcaneHazardSessionRegistry(int maxSessions) {
        if (maxSessions <= 0 || maxSessions > ABSOLUTE_MAX_SESSIONS) {
            throw new IllegalArgumentException("maxSessions outside absolute bounds");
        }
        this.maxSessions = maxSessions;
    }

    public synchronized OpenResult open(ArcaneHazardSnapshot snapshot) {
        return open(snapshot, ArcaneEmergencyProtectionSnapshot.empty());
    }

    public synchronized OpenResult open(
        ArcaneHazardSnapshot snapshot,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot");
        if (!snapshot.profile().requiresHazardSession()) {
            return OpenResult.denied("profile_not_hazardous");
        }
        pruneExpired(snapshot.activatedAtTick());
        if (sessions.containsKey(snapshot.rootCastId())) {
            return OpenResult.denied("duplicate_root_cast");
        }
        if (sessions.size() >= maxSessions) {
            return OpenResult.denied("hazard_session_capacity");
        }
        ArcaneHazardSession session = new ArcaneHazardSession(snapshot, emergencyProtectionSnapshot);
        sessions.put(snapshot.rootCastId(), session);
        return OpenResult.success(session);
    }

    public synchronized Optional<ArcaneHazardSession> find(ArcanaCastId castId) {
        return Optional.ofNullable(sessions.get(Objects.requireNonNull(castId, "castId")));
    }

    public synchronized boolean close(ArcanaCastId castId) {
        ArcaneHazardSession removed = sessions.remove(Objects.requireNonNull(castId, "castId"));
        if (removed == null) return false;
        removed.close();
        return true;
    }

    public synchronized int pruneExpired(long currentTick) {
        if (currentTick < 0L) throw new IllegalArgumentException("currentTick cannot be negative");
        int removed = 0;
        Iterator<ArcaneHazardSession> iterator = sessions.values().iterator();
        while (iterator.hasNext()) {
            ArcaneHazardSession session = iterator.next();
            if (session.closed() || session.isExpired(currentTick)) {
                session.close();
                iterator.remove();
                removed++;
            }
        }
        return removed;
    }

    public synchronized int size() {
        return sessions.size();
    }
}
