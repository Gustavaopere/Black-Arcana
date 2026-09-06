package dev.gustavopere.blackarcana.content.forbidden;

import java.util.LinkedHashSet;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Server-owned ephemeral lifecycle state. It never owns or copies player inventory/persistence. */
public final class ForbiddenDomainSession {
    public enum CloseReason {
        EXPLICIT,
        EXPIRED,
        OWNER_LOGOUT,
        OWNER_DEATH,
        OWNER_UNAVAILABLE,
        SERVER_STOP
    }

    private final UUID ownerId;
    private final ForbiddenDomainSpec spec;
    private final long startedTick;
    private final long expiresAtTick;
    private final Set<UUID> participants = new LinkedHashSet<>();
    private boolean closed;
    private CloseReason closeReason;

    public ForbiddenDomainSession(UUID ownerId, ForbiddenDomainSpec spec, long startedTick) {
        this.ownerId = Objects.requireNonNull(ownerId, "ownerId");
        this.spec = Objects.requireNonNull(spec, "spec");
        if (startedTick < 0) throw new IllegalArgumentException("startedTick must be >= 0");
        this.startedTick = startedTick;
        this.expiresAtTick = Math.addExact(startedTick, spec.durationTicks());
    }

    public UUID ownerId() { return ownerId; }
    public ForbiddenDomainSpec spec() { return spec; }
    public long startedTick() { return startedTick; }
    public long expiresAtTick() { return expiresAtTick; }
    public boolean closed() { return closed; }
    public CloseReason closeReason() { return closeReason; }
    public int participantCount() { return participants.size(); }
    public Set<UUID> participants() { return Set.copyOf(participants); }

    boolean track(UUID participantId) {
        Objects.requireNonNull(participantId, "participantId");
        if (closed) return false;
        if (participants.contains(participantId)) return true;
        if (participants.size() >= spec.entityBudget()) return false;
        return participants.add(participantId);
    }

    boolean untrack(UUID participantId) {
        Objects.requireNonNull(participantId, "participantId");
        return !closed && participants.remove(participantId);
    }

    boolean close(CloseReason reason) {
        Objects.requireNonNull(reason, "reason");
        if (closed) return false;
        closed = true;
        closeReason = reason;
        participants.clear();
        return true;
    }
}
