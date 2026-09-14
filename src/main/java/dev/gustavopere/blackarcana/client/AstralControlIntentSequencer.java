package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Client-only exact-session owner for bounded Astral control intent sequencing.
 *
 * <p>Mouse look may be sampled multiple render frames before the next movement-input event. Look deltas are
 * therefore accumulated locally and drained into the next single MOVE payload together with movement axes.
 * This keeps the client compatible with the server's one-MOVE-per-caster-per-tick ingress ceiling without
 * giving the client authority over projection position.</p>
 */
final class AstralControlIntentSequencer {
    /**
     * Makes vanilla's downstream {@code sensitivity * 0.6F + 0.2F} factor exactly zero.
     * Used only after the server has explicitly armed the exact Astral control session.
     */
    static final double PHYSICAL_BODY_NEUTRAL_SENSITIVITY = -((double) 0.2F / (double) 0.6F);

    private UUID projectionId;
    private long sequence;
    private double pendingYawDegrees;
    private double pendingPitchDegrees;

    void captureLook(
            UUID projectionId,
            double rawDeltaX,
            double rawDeltaY,
            double mouseSensitivity,
            boolean invertY
    ) {
        Objects.requireNonNull(projectionId, "projectionId");
        switchProjection(projectionId);
        if (!Double.isFinite(rawDeltaX)
                || !Double.isFinite(rawDeltaY)
                || !Double.isFinite(mouseSensitivity)) {
            return;
        }

        double degreesPerRawUnit = degreesPerRawMouseUnit(mouseSensitivity);
        double yawDelta = rawDeltaX * degreesPerRawUnit;
        double pitchDelta = rawDeltaY * degreesPerRawUnit * (invertY ? -1.0D : 1.0D);
        if (!Double.isFinite(yawDelta) || !Double.isFinite(pitchDelta)) {
            return;
        }

        double nextYaw = pendingYawDegrees + yawDelta;
        double nextPitch = pendingPitchDegrees + pitchDelta;
        if (!fitsFiniteFloat(nextYaw) || !fitsFiniteFloat(nextPitch)) {
            return;
        }
        pendingYawDegrees = nextYaw;
        pendingPitchDegrees = nextPitch;
    }

    Optional<AstralMoveIntentPayload> capture(
            UUID projectionId,
            double strafeAxis,
            double verticalAxis,
            double forwardAxis
    ) {
        Objects.requireNonNull(projectionId, "projectionId");
        switchProjection(projectionId);

        boolean hasMovement = strafeAxis != 0.0D || verticalAxis != 0.0D || forwardAxis != 0.0D;
        boolean hasLook = pendingYawDegrees != 0.0D || pendingPitchDegrees != 0.0D;
        if (!hasMovement && !hasLook) {
            return Optional.empty();
        }
        if (sequence == Long.MAX_VALUE) {
            clearPendingLook();
            return Optional.empty();
        }

        long nextSequence = ++sequence;
        float yawDelta = (float) pendingYawDegrees;
        float pitchDelta = (float) pendingPitchDegrees;
        AstralMoveIntentPayload payload = new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                nextSequence,
                strafeAxis,
                verticalAxis,
                forwardAxis,
                yawDelta,
                pitchDelta);
        clearPendingLook();
        return Optional.of(payload);
    }

    void disarm(UUID projectionId) {
        Objects.requireNonNull(projectionId, "projectionId");
        switchProjection(projectionId);
        clearPendingLook();
    }

    void clear() {
        projectionId = null;
        sequence = 0L;
        clearPendingLook();
    }

    static double degreesPerRawMouseUnit(double mouseSensitivity) {
        if (!Double.isFinite(mouseSensitivity)) {
            throw new IllegalArgumentException("Mouse sensitivity must be finite");
        }
        double base = mouseSensitivity * 0.6F + 0.2F;
        return base * base * base * 8.0D * 0.15D;
    }

    private void switchProjection(UUID projectionId) {
        if (projectionId.equals(this.projectionId)) {
            return;
        }
        this.projectionId = projectionId;
        sequence = 0L;
        clearPendingLook();
    }

    private void clearPendingLook() {
        pendingYawDegrees = 0.0D;
        pendingPitchDegrees = 0.0D;
    }

    private static boolean fitsFiniteFloat(double value) {
        return Double.isFinite(value) && Math.abs(value) <= Float.MAX_VALUE;
    }
}
