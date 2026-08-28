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
    public static final int MAX_STATE_ID_LENGTH = 512;

    public TemporaryWorldMutation {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(originalState, "originalState");
        Objects.requireNonNull(replacementState, "replacementState");
        validateStateId(originalState);
        validateStateId(replacementState);
        if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
    }

    private static void validateStateId(String state) {
        if (state.isBlank() || state.length() > MAX_STATE_ID_LENGTH) {
            throw new IllegalArgumentException("block-state id must be non-blank and bounded");
        }
    }
}
