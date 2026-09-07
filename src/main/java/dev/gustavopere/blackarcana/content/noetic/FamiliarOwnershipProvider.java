package dev.gustavopere.blackarcana.content.noetic;

import java.util.UUID;

/** Provider-neutral ownership contract for optional familiar systems. */
public interface FamiliarOwnershipProvider {
    enum Result {
        OWNED,
        NOT_OWNED,
        UNSUPPORTED
    }

    String providerId();

    Result ownership(UUID ownerId, Object candidate);
}
