package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.AstralViewPayload;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Client-local presentation state. It never grants gameplay authority. */
final class AstralViewClientState {
    private Desired desired;

    synchronized void accept(AstralViewPayload payload) {
        Objects.requireNonNull(payload, "payload");
        if (payload.action() == AstralViewPayload.Action.BEGIN) {
            desired = new Desired(payload.projectionId(), payload.entityId());
            return;
        }
        if (desired != null && desired.projectionId().equals(payload.projectionId())) {
            desired = null;
        }
    }

    synchronized Optional<Desired> desired() {
        return Optional.ofNullable(desired);
    }

    synchronized void clear() {
        desired = null;
    }

    record Desired(UUID projectionId, int entityId) {
        Desired {
            Objects.requireNonNull(projectionId, "projectionId");
            if (entityId < 0) {
                throw new IllegalArgumentException("Astral client entity id must be non-negative");
            }
        }
    }
}
