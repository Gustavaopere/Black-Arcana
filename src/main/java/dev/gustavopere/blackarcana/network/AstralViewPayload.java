package dev.gustavopere.blackarcana.network;

import java.util.Objects;
import java.util.UUID;

/** Server-authored client presentation instruction for one exact Astral Severance projection. */
public record AstralViewPayload(
        int protocolVersion,
        Action action,
        UUID projectionId,
        int entityId
) {
    public AstralViewPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(projectionId, "projectionId");
        if (entityId < 0) {
            throw new IllegalArgumentException("Astral view entity id must be non-negative");
        }
    }

    public enum Action {
        BEGIN,
        END
    }
}
