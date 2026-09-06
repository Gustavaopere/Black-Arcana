package dev.gustavopere.blackarcana.content.forbidden;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Bounded server-owned session registry for localized Forbidden Domains. */
public final class ForbiddenDomainRuntime {
    public enum StartResult { STARTED, OWNER_ALREADY_ACTIVE, GLOBAL_LIMIT }

    private final int maxActiveDomains;
    private final Map<UUID, ForbiddenDomainSession> sessions = new LinkedHashMap<>();

    public ForbiddenDomainRuntime(int maxActiveDomains) {
        if (maxActiveDomains <= 0 || maxActiveDomains > ForbiddenDomainSafetyCeilings.MAX_ACTIVE_DOMAINS) {
            throw new IllegalArgumentException("maxActiveDomains must be within 1.." + ForbiddenDomainSafetyCeilings.MAX_ACTIVE_DOMAINS);
        }
        this.maxActiveDomains = maxActiveDomains;
    }

    public synchronized StartResult start(UUID ownerId, ForbiddenDomainSpec spec, long gameTick) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(spec, "spec");
        if (sessions.containsKey(ownerId)) return StartResult.OWNER_ALREADY_ACTIVE;
        if (sessions.size() >= maxActiveDomains) return StartResult.GLOBAL_LIMIT;
        sessions.put(ownerId, new ForbiddenDomainSession(ownerId, spec, gameTick));
        return StartResult.STARTED;
    }

    public synchronized Optional<ForbiddenDomainSession> session(UUID ownerId) {
        return Optional.ofNullable(sessions.get(Objects.requireNonNull(ownerId, "ownerId")));
    }

    public synchronized boolean trackParticipant(UUID ownerId, UUID participantId) {
        ForbiddenDomainSession session = sessions.get(Objects.requireNonNull(ownerId, "ownerId"));
        return session != null && session.track(participantId);
    }

    public synchronized boolean close(UUID ownerId, ForbiddenDomainSession.CloseReason reason) {
        ForbiddenDomainSession session = sessions.remove(Objects.requireNonNull(ownerId, "ownerId"));
        return session != null && session.close(reason);
    }

    public synchronized int expire(long gameTick) {
        int closed = 0;
        Iterator<Map.Entry<UUID, ForbiddenDomainSession>> iterator = sessions.entrySet().iterator();
        while (iterator.hasNext()) {
            ForbiddenDomainSession session = iterator.next().getValue();
            if (gameTick >= session.expiresAtTick()) {
                if (session.close(ForbiddenDomainSession.CloseReason.EXPIRED)) closed++;
                iterator.remove();
            }
        }
        return closed;
    }

    public synchronized boolean clearOwner(UUID ownerId) {
        return close(ownerId, ForbiddenDomainSession.CloseReason.OWNER_LOGOUT);
    }

    public synchronized int clearForServerStop() {
        int closed = 0;
        for (ForbiddenDomainSession session : sessions.values()) {
            if (session.close(ForbiddenDomainSession.CloseReason.SERVER_STOP)) closed++;
        }
        sessions.clear();
        return closed;
    }

    public synchronized int activeCount() {
        return sessions.size();
    }
}
