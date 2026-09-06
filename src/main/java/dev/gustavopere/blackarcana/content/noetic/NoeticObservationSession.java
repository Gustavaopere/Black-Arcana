package dev.gustavopere.blackarcana.content.noetic;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Ephemeral server-owned observation state. It owns no camera authority or persistence. */
public final class NoeticObservationSession {
    public enum CloseReason {
        EXPLICIT,
        EXPIRED,
        VIEWER_LOGOUT,
        VIEWER_DEATH,
        TARGET_UNAVAILABLE,
        SERVER_STOP
    }

    private final UUID viewerId;
    private final UUID targetId;
    private final NoeticObservationKind kind;
    private final long startedAtTick;
    private final long expiresAtTick;
    private CloseReason closeReason;

    public NoeticObservationSession(
            UUID viewerId,
            UUID targetId,
            NoeticObservationKind kind,
            long startedAtTick,
            long expiresAtTick
    ) {
        this.viewerId = Objects.requireNonNull(viewerId, "viewerId");
        this.targetId = Objects.requireNonNull(targetId, "targetId");
        this.kind = Objects.requireNonNull(kind, "kind");
        if (startedAtTick < 0L || expiresAtTick <= startedAtTick) {
            throw new IllegalArgumentException("Noetic observation tick bounds are invalid");
        }
        this.startedAtTick = startedAtTick;
        this.expiresAtTick = expiresAtTick;
    }

    public UUID viewerId() { return viewerId; }
    public UUID targetId() { return targetId; }
    public NoeticObservationKind kind() { return kind; }
    public long startedAtTick() { return startedAtTick; }
    public long expiresAtTick() { return expiresAtTick; }
    public boolean expiredAt(long tick) { return tick >= expiresAtTick; }
    public synchronized boolean closed() { return closeReason != null; }
    public synchronized Optional<CloseReason> closeReason() { return Optional.ofNullable(closeReason); }

    public synchronized boolean close(CloseReason reason) {
        Objects.requireNonNull(reason, "reason");
        if (closeReason != null) return false;
        closeReason = reason;
        return true;
    }
}
