package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/**
 * Bounded danger contract captured into a hazard session.
 * Authoritative preflight thresholds remain part of the runtime profile so the
 * client advisory payload and server cast gate cannot silently diverge.
 */
public record ArcaneDangerProfile(
    ArcaneDangerTier tier,
    double backlashMultiplier,
    double corruptionCoefficient,
    double strainCoefficient,
    long damageLeaseTicks,
    int maxDamageInstances,
    double minimumArcaneResistance,
    double recommendedArcaneResistance,
    boolean emergencyProtectionAllowed
) {
    public static final double ABSOLUTE_MAX_BACKLASH_MULTIPLIER = 16.0D;
    public static final double ABSOLUTE_MAX_STATE_COEFFICIENT = 4_096.0D;
    public static final double ABSOLUTE_MAX_RESISTANCE_HINT = 10_000.0D;
    public static final long ABSOLUTE_MAX_DAMAGE_LEASE_TICKS = 20L * 60L * 30L;
    public static final int ABSOLUTE_MAX_DAMAGE_INSTANCES = 4_096;

    /** Backward-compatible constructor for profiles created before authoritative preflight hints existed. */
    public ArcaneDangerProfile(
        ArcaneDangerTier tier,
        double backlashMultiplier,
        double corruptionCoefficient,
        double strainCoefficient,
        long damageLeaseTicks,
        int maxDamageInstances
    ) {
        this(
            tier,
            backlashMultiplier,
            corruptionCoefficient,
            strainCoefficient,
            damageLeaseTicks,
            maxDamageInstances,
            0.0D,
            0.0D,
            false);
    }

    public ArcaneDangerProfile {
        Objects.requireNonNull(tier, "tier");
        validateFiniteBounded("backlashMultiplier", backlashMultiplier, ABSOLUTE_MAX_BACKLASH_MULTIPLIER);
        validateFiniteBounded("corruptionCoefficient", corruptionCoefficient, ABSOLUTE_MAX_STATE_COEFFICIENT);
        validateFiniteBounded("strainCoefficient", strainCoefficient, ABSOLUTE_MAX_STATE_COEFFICIENT);
        validateFiniteBounded("minimumArcaneResistance", minimumArcaneResistance, ABSOLUTE_MAX_RESISTANCE_HINT);
        validateFiniteBounded("recommendedArcaneResistance", recommendedArcaneResistance, ABSOLUTE_MAX_RESISTANCE_HINT);
        if (minimumArcaneResistance > recommendedArcaneResistance) {
            throw new IllegalArgumentException("minimumArcaneResistance cannot exceed recommendedArcaneResistance");
        }
        if (damageLeaseTicks < 0L || damageLeaseTicks > ABSOLUTE_MAX_DAMAGE_LEASE_TICKS) {
            throw new IllegalArgumentException("damageLeaseTicks outside absolute bounds");
        }
        if (maxDamageInstances <= 0 || maxDamageInstances > ABSOLUTE_MAX_DAMAGE_INSTANCES) {
            throw new IllegalArgumentException("maxDamageInstances outside absolute bounds");
        }
        if (tier == ArcaneDangerTier.NORMAL) {
            if (backlashMultiplier != 0.0D || corruptionCoefficient != 0.0D || strainCoefficient != 0.0D
                || damageLeaseTicks != 0L || minimumArcaneResistance != 0.0D || recommendedArcaneResistance != 0.0D
                || emergencyProtectionAllowed) {
                throw new IllegalArgumentException("NORMAL profile cannot carry severe hazard semantics");
            }
        } else if (damageLeaseTicks == 0L) {
            throw new IllegalArgumentException("hazardous profile requires a positive damage lease");
        }
        if (tier.requiresBacklashRisk() && backlashMultiplier <= 0.0D) {
            throw new IllegalArgumentException("DANGEROUS+ profile cannot silently remove backlash risk");
        }
    }

    public static ArcaneDangerProfile normal() {
        return new ArcaneDangerProfile(
            ArcaneDangerTier.NORMAL,
            0.0D,
            0.0D,
            0.0D,
            0L,
            1,
            0.0D,
            0.0D,
            false);
    }

    public boolean requiresHazardSession() {
        return tier.requiresHazardSession();
    }

    private static void validateFiniteBounded(String name, double value, double absoluteMax) {
        if (!Double.isFinite(value) || value < 0.0D || value > absoluteMax) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }
}
