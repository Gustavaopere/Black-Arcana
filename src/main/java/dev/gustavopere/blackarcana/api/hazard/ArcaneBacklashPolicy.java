package dev.gustavopere.blackarcana.api.hazard;

/** Immutable technical ceilings for one root-cast backlash ledger. */
public record ArcaneBacklashPolicy(
    boolean allowOwnedSummon,
    double minimumBacklashPerPositiveSettlement,
    double maximumBacklashPerSettlement,
    double maximumTotalEligibleDamage
) {
    public static final double ABSOLUTE_MAX_BACKLASH_PER_SETTLEMENT = 1_000_000.0D;
    public static final double ABSOLUTE_MAX_TOTAL_ELIGIBLE_DAMAGE = 100_000_000.0D;

    public ArcaneBacklashPolicy {
        validateFinite("minimumBacklashPerPositiveSettlement", minimumBacklashPerPositiveSettlement);
        validateFinite("maximumBacklashPerSettlement", maximumBacklashPerSettlement);
        validateFinite("maximumTotalEligibleDamage", maximumTotalEligibleDamage);
        if (minimumBacklashPerPositiveSettlement > maximumBacklashPerSettlement) {
            throw new IllegalArgumentException("minimum backlash cannot exceed maximum backlash");
        }
        if (maximumBacklashPerSettlement > ABSOLUTE_MAX_BACKLASH_PER_SETTLEMENT) {
            throw new IllegalArgumentException("maximumBacklashPerSettlement exceeds absolute ceiling");
        }
        if (maximumTotalEligibleDamage <= 0.0D
            || maximumTotalEligibleDamage > ABSOLUTE_MAX_TOTAL_ELIGIBLE_DAMAGE) {
            throw new IllegalArgumentException("maximumTotalEligibleDamage outside absolute bounds");
        }
    }

    public static ArcaneBacklashPolicy canonical() {
        return new ArcaneBacklashPolicy(false, 0.0D, 1_000_000.0D, 100_000_000.0D);
    }

    private static void validateFinite(String name, double value) {
        if (!Double.isFinite(value) || value < 0.0D) {
            throw new IllegalArgumentException(name + " must be finite and non-negative");
        }
    }
}
