package dev.gustavopere.blackarcana.core.world;

import java.util.Optional;

/**
 * Minimal world adapter for temporary mutation lifecycle.
 * Implementations must never force-load a chunk. `false` from replaceIfCurrent
 * guarantees that no mutation was applied.
 */
public interface TemporaryBlockBackend {
    Optional<String> readLoadedState(TemporaryMutationKey key);

    boolean replaceIfCurrent(TemporaryMutationKey key, String expectedState, String replacementState);
}
