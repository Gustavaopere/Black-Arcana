package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;
import java.util.UUID;

/** Provider-neutral query used by optional claim/protection integrations. */
public record ProtectionQuery(
    UUID casterId,
    String dimensionId,
    String targetId,
    EntityInteractionType interactionType
) {
    public ProtectionQuery {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(targetId, "targetId");
        Objects.requireNonNull(interactionType, "interactionType");
        if (dimensionId.isBlank() || targetId.isBlank()) {
            throw new IllegalArgumentException("protection query ids cannot be blank");
        }
    }
}
