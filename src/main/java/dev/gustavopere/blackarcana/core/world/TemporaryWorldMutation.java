package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;

import java.util.Objects;
import java.util.UUID;

public record TemporaryWorldMutation(
    TemporaryMutationKey key,
    UUID ownerId,
    ArcanaCastId castId,
    String originalState,
    String replacementState,
    long expiresAtTick
) {
    public TemporaryWorldMutation {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(originalState, "originalState");
        Objects.requireNonNull(replacementState, "replacementState");
        if (originalState.isBlank() || replacementState.isBlank()) {
            throw new IllegalArgumentException("block-state ids cannot be blank");
        }
        if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
    }
}
