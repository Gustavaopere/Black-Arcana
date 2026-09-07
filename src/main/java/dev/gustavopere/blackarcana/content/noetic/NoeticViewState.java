package dev.gustavopere.blackarcana.content.noetic;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Small client-facing state contract for observation modes that temporarily own the camera.
 *
 * <p>This class contains no Minecraft client classes and grants no gameplay authority. It only
 * tracks the latest server-authorized view identity so transport and physical-client adapters can
 * apply/restore presentation idempotently.</p>
 */
public final class NoeticViewState {
    private Session session;

    public synchronized boolean activate(NoeticObservationKind kind, UUID targetId) {
        Objects.requireNonNull(kind, "kind");
        Objects.requireNonNull(targetId, "targetId");
        if (!ownsCamera(kind)) {
            throw new IllegalArgumentException("Noetic observation kind does not own a client camera: " + kind);
        }

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

    public static boolean ownsCamera(NoeticObservationKind kind) {
        Objects.requireNonNull(kind, "kind");
        return kind == NoeticObservationKind.BORROWED_SIGHT
                || kind == NoeticObservationKind.ASTRAL_SEVERANCE;
    }

    public record Session(NoeticObservationKind kind, UUID targetId) {
        public Session {
            Objects.requireNonNull(kind, "kind");
            Objects.requireNonNull(targetId, "targetId");
            if (!NoeticViewState.ownsCamera(kind)) {
                throw new IllegalArgumentException("Noetic view session requires a camera-owning observation kind");
            }
        }
    }
}
