package dev.gustavopere.blackarcana.api.hazard;

/**
 * Bounded per-spell strain contract. Values are declarative inputs to the
 * server-owned strain service; the client never supplies them.
 */
public record ArcaneStrainProfile(
    double baseStrainPerCommittedCast,
    double strainPerEligibleDamage,
    double strainPerChannelTick,
    double minimumUnavoidableStrain,
    double maxBacklashBonusMultiplier,
    double maxCorruptionBonusMultiplier,
    double hardGateThresholdUnits
) {
    public static final double ABSOLUTE_MAX_ACQUISITION_RATE = 4_096.0D;
    public static final double ABSOLUTE_MAX_BONUS_MULTIPLIER = 8.0D;
    public static final double ABSOLUTE_MAX_GATE_UNITS = 1_000_000.0D;
    public static final long ABSOLUTE_MAX_CHANNEL_TICKS = 20L * 60L * 30L;

    public ArcaneStrainProfile {
        validateBounded("baseStrainPerCommittedCast", baseStrainPerCommittedCast, ABSOLUTE_MAX_ACQUISITION_RATE);
        validateBounded("strainPerEligibleDamage", strainPerEligibleDamage, ABSOLUTE_MAX_ACQUISITION_RATE);
        validateBounded("strainPerChannelTick", strainPerChannelTick, ABSOLUTE_MAX_ACQUISITION_RATE);
        validateBounded("minimumUnavoidableStrain", minimumUnavoidableStrain, ABSOLUTE_MAX_ACQUISITION_RATE);
        validateBounded("maxBacklashBonusMultiplier", maxBacklashBonusMultiplier, ABSOLUTE_MAX_BONUS_MULTIPLIER);
        validateBounded("maxCorruptionBonusMultiplier", maxCorruptionBonusMultiplier, ABSOLUTE_MAX_BONUS_MULTIPLIER);
        validateBounded("hardGateThresholdUnits", hardGateThresholdUnits, ABSOLUTE_MAX_GATE_UNITS);
    }

    public static ArcaneStrainProfile none() {
        return new ArcaneStrainProfile(0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D);
    }

    public double rawStrain(double confirmedDamage, long channelTicks) {
        if (!Double.isFinite(confirmedDamage) || confirmedDamage < 0.0D) {
            throw new IllegalArgumentException("confirmedDamage must be finite and non-negative");
        }
        if (channelTicks < 0L || channelTicks > ABSOLUTE_MAX_CHANNEL_TICKS) {
            throw new IllegalArgumentException("channelTicks outside absolute bounds");
        }
        double raw = saturatingAdd(
            baseStrainPerCommittedCast,
            saturatingMultiply(confirmedDamage, strainPerEligibleDamage));
        return saturatingAdd(raw, saturatingMultiply((double) channelTicks, strainPerChannelTick));
    }

    /**
     * @param avoidableResidualMultiplier 0 means all avoidable strain was resisted;
     *                                    1 means none was resisted.
     */
    public double appliedStrain(double confirmedDamage, long channelTicks, double avoidableResidualMultiplier) {
        if (!Double.isFinite(avoidableResidualMultiplier)
            || avoidableResidualMultiplier < 0.0D
            || avoidableResidualMultiplier > 1.0D) {
            throw new IllegalArgumentException("avoidableResidualMultiplier must be within [0,1]");
        }
        double raw = rawStrain(confirmedDamage, channelTicks);
        if (raw == 0.0D) return 0.0D;
        double unavoidable = Math.min(raw, minimumUnavoidableStrain);
        double avoidable = Math.max(0.0D, raw - unavoidable);
        return saturatingAdd(unavoidable, saturatingMultiply(avoidable, avoidableResidualMultiplier));
    }

    public double backlashMultiplier(double currentUnits, double maxUnits) {
        return scaledMultiplier(currentUnits, maxUnits, maxBacklashBonusMultiplier);
    }

    public double corruptionMultiplier(double currentUnits, double maxUnits) {
        return scaledMultiplier(currentUnits, maxUnits, maxCorruptionBonusMultiplier);
    }

    public boolean hardGateActive(double currentUnits) {
        validateFiniteNonNegative("currentUnits", currentUnits);
        return hardGateThresholdUnits > 0.0D && currentUnits >= hardGateThresholdUnits;
    }

    private static double scaledMultiplier(double currentUnits, double maxUnits, double maxBonus) {
        validateFiniteNonNegative("currentUnits", currentUnits);
        if (!Double.isFinite(maxUnits) || maxUnits <= 0.0D) {
            throw new IllegalArgumentException("maxUnits must be finite and positive");
        }
        double fraction = Math.min(1.0D, currentUnits / maxUnits);
        return 1.0D + maxBonus * fraction;
    }

    private static void validateBounded(String name, double value, double max) {
        if (!Double.isFinite(value) || value < 0.0D || value > max) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }

    private static void validateFiniteNonNegative(String name, double value) {
        if (!Double.isFinite(value) || value < 0.0D) {
            throw new IllegalArgumentException(name + " must be finite and non-negative");
        }
    }

    private static double saturatingMultiply(double first, double second) {
        double product = first * second;
        return Double.isFinite(product) ? product : ABSOLUTE_MAX_GATE_UNITS;
    }

    private static double saturatingAdd(double first, double second) {
        double result = first + second;
        return Double.isFinite(result) ? result : ABSOLUTE_MAX_GATE_UNITS;
    }
}
