package dev.gustavopere.blackarcana.network;

import java.util.Objects;
import java.util.UUID;

/**
 * Server-authored client presentation/control instruction for one exact Astral Severance projection.
 *
 * <p>{@link Action#BEGIN} and {@link Action#END} own only camera presentation. Movement redirection stays
 * fail-closed until the server separately emits {@link Action#MOVE_ARM} for the exact active projection.
 * The current Stage 07.07 production runtime does not emit MOVE_ARM while the reviewed MOVE value contract
 * remains unresolved.</p>
 */
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
        END,
        MOVE_ARM,
        MOVE_END
    }
}
