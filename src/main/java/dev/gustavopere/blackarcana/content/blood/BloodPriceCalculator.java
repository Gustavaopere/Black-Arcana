package dev.gustavopere.blackarcana.content.blood;

/** Pure quote calculation for the Blood Price substitution mechanic. */
public final class BloodPriceCalculator {
    private BloodPriceCalculator() { }

    public static Quote quote(
        double originalResourceCost,
        double healthFraction,
        double healthPerResourceUnit,
        double currentHealth,
        double minimumRemainingHealth
    ) {
        requireFiniteNonNegative(originalResourceCost, "originalResourceCost");
        requireFiniteNonNegative(healthPerResourceUnit, "healthPerResourceUnit");
        requireFiniteNonNegative(currentHealth, "currentHealth");
        requireFiniteNonNegative(minimumRemainingHealth, "minimumRemainingHealth");
        if (!Double.isFinite(healthFraction) || healthFraction < 0.0D
            || healthFraction > BloodSafetyCeilings.MAX_BLOOD_PRICE_FRACTION) {
            throw new IllegalArgumentException("healthFraction outside Blood Price ceiling");
        }
        if (minimumRemainingHealth < BloodSafetyCeilings.MIN_BLOOD_PRICE_REMAINING_HEALTH) {
            throw new IllegalArgumentException("minimumRemainingHealth below hard safety floor");
        }

        double substitutedResource = originalResourceCost * healthFraction;
        double healthCost = substitutedResource * healthPerResourceUnit;
        double resourceCost = originalResourceCost - substitutedResource;
        boolean affordable = currentHealth - healthCost >= minimumRemainingHealth;
        return new Quote(resourceCost, healthCost, affordable);
    }

    private static void requireFiniteNonNegative(double value, String field) {
        if (!Double.isFinite(value) || value < 0.0D) {
            throw new IllegalArgumentException(field + " must be finite and non-negative");
        }
    }

    public record Quote(double resourceCost, double healthCost, boolean affordable) {
        public Quote {
            requireFiniteNonNegative(resourceCost, "resourceCost");
            requireFiniteNonNegative(healthCost, "healthCost");
        }
    }
}
