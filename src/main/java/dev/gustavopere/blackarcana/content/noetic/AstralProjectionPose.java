package dev.gustavopere.blackarcana.content.noetic;

/** Immutable server-owned spatial state for an active Astral Severance projection. */
public record AstralProjectionPose(
        double x,
        double y,
        double z,
        float yaw,
        float pitch
) {
    public AstralProjectionPose {
        if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) {
            throw new IllegalArgumentException("Astral projection coordinates must be finite");
        }
        if (!Float.isFinite(yaw) || !Float.isFinite(pitch)) {
            throw new IllegalArgumentException("Astral projection rotation must be finite");
        }
        if (pitch < -90.0F || pitch > 90.0F) {
            throw new IllegalArgumentException("Astral projection pitch must stay within [-90, 90]");
        }
    }

    public double distanceTo(AstralProjectionPose other) {
        if (other == null) throw new NullPointerException("other");
        double dx = other.x - x;
        double dy = other.y - y;
        double dz = other.z - z;
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }
}
