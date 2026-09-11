package dev.gustavopere.blackarcana.content.noetic;

import java.util.Objects;
import java.util.UUID;

/**
 * Client-originated movement/look intent for one already-authorized projection.
 * Coordinates are deliberately absent; the server advances authoritative pose from these bounded axes.
 */
public record AstralProjectionMovementIntent(
        UUID projectionId,
        long sequence,
        float strafe,
        float forward,
        float vertical,
        float yaw,
        float pitch
) {
    public AstralProjectionMovementIntent {
        Objects.requireNonNull(projectionId, "projectionId");
        if (sequence <= 0L) {
            throw new IllegalArgumentException("Astral projection movement sequence must be positive");
        }
        if (!Float.isFinite(strafe)
                || !Float.isFinite(forward)
                || !Float.isFinite(vertical)
                || !Float.isFinite(yaw)
                || !Float.isFinite(pitch)) {
            throw new IllegalArgumentException("Astral projection movement intent must be finite");
        }
        if (pitch < -90.0F || pitch > 90.0F) {
            throw new IllegalArgumentException("Astral projection movement pitch must stay within [-90, 90]");
        }
    }

    public boolean axesWithinUnitBounds() {
        return Math.abs(strafe) <= 1.0F
                && Math.abs(forward) <= 1.0F
                && Math.abs(vertical) <= 1.0F;
    }
}
