package dev.gustavopere.blackarcana.content.space;

/** Clamps directional impulses to the frozen Liminal hard speed ceiling. */
public final class VectorImpulseLimiter {
    private VectorImpulseLimiter() { }

    public static Vector clamp(double x, double y, double z, double configuredMaxSpeed) {
        requireFinite(x); requireFinite(y); requireFinite(z);
        if (!Double.isFinite(configuredMaxSpeed) || configuredMaxSpeed <= 0.0D
            || configuredMaxSpeed > LiminalSafetyCeilings.MAX_RESULTING_SPEED) {
            throw new IllegalArgumentException("configuredMaxSpeed outside hard ceiling");
        }
        double length = Math.sqrt(x * x + y * y + z * z);
        if (length <= configuredMaxSpeed || length == 0.0D) return new Vector(x, y, z);
        double scale = configuredMaxSpeed / length;
        return new Vector(x * scale, y * scale, z * scale);
    }

    private static void requireFinite(double value) {
        if (!Double.isFinite(value)) throw new IllegalArgumentException("vector component must be finite");
    }

    public record Vector(double x, double y, double z) {
        public double speed() { return Math.sqrt(x * x + y * y + z * z); }
    }
}
