package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/**
 * Minimal bounded danger contract used by Stage 05A session attribution.
 * Later profile/schema tasks may add explicit strategies without weakening
 * these technical ceilings or the DANGEROUS+ backlash invariant.
 */
public record ArcaneDangerProfile(
    ArcaneDangerTier tier,
    double backlashMultiplier,
    double corruptionCoefficient,
    double strainCoefficient,
    long damageLeaseTicks,
    int maxDamageInstances
) {
    public static final double ABSOLUTE_MAX_BACKLASH_MULTIPLIER = 16.0D;
    public static final double ABSOLUTE_MAX_STATE_COEFFICIENT = 4_096.0D;
    public static final long ABSOLUTE_MAX_DAMAGE_LEASE_TICKS = 20L * 60L * 30L;
    public static final int ABSOLUTE_MAX_DAMAGE_INSTANCES = 4_096;

    public ArcaneDangerProfile {
        Objects.requireNonNull(tier, "tier");
        validateFiniteBounded("backlashMultiplier", backlashMultiplier, ABSOLUTE_MAX_BACKLASH_MULTIPLIER);
        validateFiniteBounded("corruptionCoefficient", corruptionCoefficient, ABSOLUTE_MAX_STATE_COEFFICIENT);
        validateFiniteBounded("strainCoefficient", strainCoefficient, ABSOLUTE_MAX_STATE_COEFFICIENT);
        if (damageLeaseTicks < 0L || damageLeaseTicks > ABSOLUTE_MAX_DAMAGE_LEASE_TICKS) {
            throw new IllegalArgumentException("damageLeaseTicks outside absolute bounds");
        }
        if (maxDamageInstances <= 0 || maxDamageInstances > ABSOLUTE_MAX_DAMAGE_INSTANCES) {
            throw new IllegalArgumentException("maxDamageInstances outside absolute bounds");
        }
        if (tier == ArcaneDangerTier.NORMAL) {
            if (backlashMultiplier != 0.0D || corruptionCoefficient != 0.0D || strainCoefficient != 0.0D
                || damageLeaseTicks != 0L) {
                throw new IllegalArgumentException("NORMAL profile cannot carry severe hazard coefficients");
            }
        } else if (damageLeaseTicks == 0L) {
            throw new IllegalArgumentException("hazardous profile requires a positive damage lease");
        }
        if (tier.requiresBacklashRisk() && backlashMultiplier <= 0.0D) {
            throw new IllegalArgumentException("DANGEROUS+ profile cannot silently remove backlash risk");
        }
    }

    public static ArcaneDangerProfile normal() {
        return new ArcaneDangerProfile(ArcaneDangerTier.NORMAL, 0.0D, 0.0D, 0.0D, 0L, 1);
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
