package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;

import java.util.Objects;
import java.util.UUID;

/**
 * Client intent for one bounded Astral Severance control update.
 *
 * <p>The payload intentionally carries no caster identity and no authoritative world position. The server
 * derives the caster from the authenticated network context and applies these axes only to the exact
 * server-authored projection id.</p>
 */
public record AstralMoveIntentPayload(
        int protocolVersion,
        UUID projectionId,
        long sequence,
        double strafeAxis,
        double verticalAxis,
        double forwardAxis,
        float yawDeltaDegrees,
        float pitchDeltaDegrees
) {
    public AstralMoveIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(projectionId, "projectionId");
        if (sequence <= 0L) throw new IllegalArgumentException("Astral control sequence must be positive");
        requireUnitAxis(strafeAxis, "strafeAxis");
        requireUnitAxis(verticalAxis, "verticalAxis");
        requireUnitAxis(forwardAxis, "forwardAxis");
        if (!Float.isFinite(yawDeltaDegrees) || !Float.isFinite(pitchDeltaDegrees)) {
            throw new IllegalArgumentException("Astral look deltas must be finite");
        }
    }

    public AstralSeveranceRuntime.ControlIntent toControlIntent() {
        return new AstralSeveranceRuntime.ControlIntent(
                projectionId,
                sequence,
                strafeAxis,
                verticalAxis,
                forwardAxis,
                yawDeltaDegrees,
                pitchDeltaDegrees);
    }

    private static void requireUnitAxis(double value, String field) {
        if (!Double.isFinite(value) || value < -1.0D || value > 1.0D) {
            throw new IllegalArgumentException(field + " must be finite and within [-1, 1]");
        }
    }
}
