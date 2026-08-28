package dev.gustavopere.blackarcana.core.hazard;

/** Pure diminishing-return curve for Arcane Resistance. */
public record ArcaneResistanceCurve(double k, double maxResistance) {
    public static final double CANONICAL_K = 40.0D;
    public static final double CANONICAL_MAX_RESISTANCE = 240.0D;
    public static final double ABSOLUTE_MAX_K = 10_000.0D;
    public static final double ABSOLUTE_MAX_RESISTANCE = 10_000.0D;

    public ArcaneResistanceCurve {
        if (!Double.isFinite(k) || k <= 0.0D || k > ABSOLUTE_MAX_K) {
            throw new IllegalArgumentException("k outside absolute bounds");
        }
        if (!Double.isFinite(maxResistance) || maxResistance <= 0.0D
            || maxResistance > ABSOLUTE_MAX_RESISTANCE) {
            throw new IllegalArgumentException("maxResistance outside absolute bounds");
        }
    }

    public static ArcaneResistanceCurve canonical() {
        return new ArcaneResistanceCurve(CANONICAL_K, CANONICAL_MAX_RESISTANCE);
    }

    public double residualMultiplier(double resistance) {
        if (!Double.isFinite(resistance) || resistance < 0.0D) {
            throw new IllegalArgumentException("resistance must be finite and non-negative");
        }
        double bounded = Math.min(resistance, maxResistance);
        double residual = k / (k + bounded);
        if (!Double.isFinite(residual)) throw new IllegalStateException("resistance curve produced non-finite result");
        return Math.max(0.0D, Math.min(1.0D, residual));
    }
}
