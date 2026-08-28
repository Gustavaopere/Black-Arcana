package dev.gustavopere.blackarcana.core.progression;

/** Deterministic monotonic diminishing returns that asymptotically approaches, but never exceeds, a hard cap. */
public final class DiminishingReturnsCurve {
    private DiminishingReturnsCurve() { }

    public static double apply(double baseValue, double rawBonus, double hardCap, double knee) {
        requireFinite(baseValue, "baseValue");
        requireFinite(rawBonus, "rawBonus");
        requireFinite(hardCap, "hardCap");
        requireFinite(knee, "knee");
        if (baseValue < 0D || hardCap < baseValue || knee <= 0D) throw new IllegalArgumentException("invalid diminishing-return bounds");
        if (rawBonus <= 0D || baseValue == hardCap) return baseValue;
        double headroom = hardCap - baseValue;
        double ratio = rawBonus / (rawBonus + knee);
        if (!Double.isFinite(ratio)) ratio = 1D;
        double result = baseValue + headroom * Math.clamp(ratio, 0D, 1D);
        return Math.min(hardCap, Math.max(baseValue, result));
    }

    private static void requireFinite(double value, String label) {
        if (!Double.isFinite(value)) throw new IllegalArgumentException(label + " must be finite");
    }
}
