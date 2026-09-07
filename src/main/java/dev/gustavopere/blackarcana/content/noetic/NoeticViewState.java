package dev.gustavopere.blackarcana.content.noetic;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Small client-facing state contract for Borrowed Sight camera presentation.
 *
 * <p>This class contains no Minecraft client classes and grants no gameplay authority. It only
 * tracks the latest server-authorized Borrowed Sight target so transport and physical-client
 * adapters can apply or restore presentation idempotently.</p>
 *
 * <p>Astral Severance is deliberately excluded until Stage 07.07 owns a real astral
 * viewpoint/avatar rather than reusing an arbitrary observed living entity.</p>
 */
public final class NoeticViewState {
    private Session session;

    public synchronized boolean activate(NoeticObservationKind kind, UUID targetId) {
        Objects.requireNonNull(kind, "kind");
        Objects.requireNonNull(targetId, "targetId");
        requireBorrowedSight(kind);

        Session next = new Session(kind, targetId);
        if (next.equals(session)) return false;
        session = next;
        return true;
    }

    public synchronized Optional<Session> session() {
        return Optional.ofNullable(session);
    }

    public synchronized boolean close() {
        if (session == null) return false;
        session = null;
        return true;
    }

    private static void requireBorrowedSight(NoeticObservationKind kind) {
        if (kind != NoeticObservationKind.BORROWED_SIGHT) {
            throw new IllegalArgumentException("Noetic client camera state currently supports Borrowed Sight only: " + kind);
        }
    }

    public record Session(NoeticObservationKind kind, UUID targetId) {
        public Session {
            Objects.requireNonNull(kind, "kind");
            Objects.requireNonNull(targetId, "targetId");
            requireBorrowedSight(kind);
        }
    }
}
