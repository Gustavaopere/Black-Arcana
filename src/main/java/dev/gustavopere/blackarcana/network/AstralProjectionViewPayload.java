package dev.gustavopere.blackarcana.network;

import java.util.Objects;
import java.util.UUID;

/** Server-authored Astral Severance camera/viewpoint transition. */
public record AstralProjectionViewPayload(
        int protocolVersion,
        Action action,
        UUID projectionId,
        int projectionEntityId
) {
    public AstralProjectionViewPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(projectionId, "projectionId");
        if (projectionEntityId < 0) {
            throw new IllegalArgumentException("Astral projection entity id must be non-negative");
        }
    }

    public enum Action {
        BEGIN,
        END
    }
}
