package dev.gustavopere.blackarcana.api.hazard;

/** Bounded acquisition policy for one dangerous-magic corruption source. */
public record CorruptionAcquisitionProfile(
    double baseCorruptionPerCommittedCast,
    double corruptionPerEligibleDamage,
    double unavoidableFloorMultiplier,
    double resistanceScale,
    double maxResistanceApplied
) {
    public static final double ABSOLUTE_MAX_CORRUPTION_PER_EVENT = 4_096.0D;
    public static final double ABSOLUTE_MAX_RESISTANCE_SCALE = 4.0D;
    public static final double ABSOLUTE_MAX_RESISTANCE_APPLIED = 10_000.0D;

    public CorruptionAcquisitionProfile {
        finiteRange("baseCorruptionPerCommittedCast", baseCorruptionPerCommittedCast, 0.0D, ABSOLUTE_MAX_CORRUPTION_PER_EVENT);
        finiteRange("corruptionPerEligibleDamage", corruptionPerEligibleDamage, 0.0D, ABSOLUTE_MAX_CORRUPTION_PER_EVENT);
        finiteRange("unavoidableFloorMultiplier", unavoidableFloorMultiplier, 0.0D, 1.0D);
        finiteRange("resistanceScale", resistanceScale, 0.0D, ABSOLUTE_MAX_RESISTANCE_SCALE);
        finiteRange("maxResistanceApplied", maxResistanceApplied, 0.0D, ABSOLUTE_MAX_RESISTANCE_APPLIED);
    }

    public static CorruptionAcquisitionProfile committedCastOnly(double baseUnits, double unavoidableFloorMultiplier) {
        return new CorruptionAcquisitionProfile(
            baseUnits,
            0.0D,
            unavoidableFloorMultiplier,
            1.0D,
            ABSOLUTE_MAX_RESISTANCE_APPLIED);
    }

    private static void finiteRange(String name, double value, double min, double max) {
        if (!Double.isFinite(value) || value < min || value > max) {
            throw new IllegalArgumentException(name + " outside bounds");
        }
    }
}
