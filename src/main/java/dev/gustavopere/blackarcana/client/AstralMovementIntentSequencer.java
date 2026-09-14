package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Client-only sequence owner for bounded Astral movement intents. */
final class AstralMovementIntentSequencer {
    private UUID projectionId;
    private long sequence;

    Optional<AstralMoveIntentPayload> capture(
            UUID projectionId,
            double strafeAxis,
            double verticalAxis,
            double forwardAxis
    ) {
        Objects.requireNonNull(projectionId, "projectionId");
        if (!projectionId.equals(this.projectionId)) {
            this.projectionId = projectionId;
            sequence = 0L;
        }
        if (strafeAxis == 0.0D && verticalAxis == 0.0D && forwardAxis == 0.0D) {
            return Optional.empty();
        }
        if (sequence == Long.MAX_VALUE) {
            return Optional.empty();
        }
        long nextSequence = ++sequence;
        return Optional.of(new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                nextSequence,
                strafeAxis,
                verticalAxis,
                forwardAxis,
                0.0F,
                0.0F));
    }

    void reset(UUID projectionId) {
        Objects.requireNonNull(projectionId, "projectionId");
        if (projectionId.equals(this.projectionId)) {
            this.projectionId = null;
            sequence = 0L;
        }
    }
}
