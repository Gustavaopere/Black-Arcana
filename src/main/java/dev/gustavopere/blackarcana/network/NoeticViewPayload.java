package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;

import java.util.Objects;

/** Bounded server-authored instruction for Noetic client camera presentation. */
public record NoeticViewPayload(
        int protocolVersion,
        Action action,
        NoeticObservationKind kind,
        int targetEntityId
) {
    public NoeticViewPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(kind, "kind");
        if (kind != NoeticObservationKind.BORROWED_SIGHT
                && kind != NoeticObservationKind.ASTRAL_SEVERANCE) {
            throw new IllegalArgumentException("Noetic view payload requires a camera-capable observation kind");
        }
        if (targetEntityId < 0) {
            throw new IllegalArgumentException("Noetic view target entity id must be non-negative");
        }
    }

    public enum Action {
        BEGIN,
        END
    }
}
