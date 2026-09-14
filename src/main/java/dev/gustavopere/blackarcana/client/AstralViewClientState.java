package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.AstralViewPayload;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Client-local presentation/control state. It never grants gameplay authority on its own. */
final class AstralViewClientState {
    private Desired desired;
    private Desired movementControl;

    synchronized void accept(AstralViewPayload payload) {
        Objects.requireNonNull(payload, "payload");
        Desired identity = new Desired(payload.projectionId(), payload.entityId());
        switch (payload.action()) {
            case BEGIN -> {
                if (!Objects.equals(desired, identity)) {
                    movementControl = null;
                }
                desired = identity;
            }
            case END -> {
                if (desired != null && desired.projectionId().equals(payload.projectionId())) {
                    desired = null;
                    movementControl = null;
                }
            }
            case MOVE_ARM -> {
                if (Objects.equals(desired, identity)) {
                    movementControl = identity;
                }
            }
            case MOVE_END -> {
                if (Objects.equals(movementControl, identity)) {
                    movementControl = null;
                }
            }
        }
    }

    synchronized Optional<Desired> desired() {
        return Optional.ofNullable(desired);
    }

    synchronized Optional<Desired> movementControl() {
        return Optional.ofNullable(movementControl);
    }

    synchronized void clear() {
        desired = null;
        movementControl = null;
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
