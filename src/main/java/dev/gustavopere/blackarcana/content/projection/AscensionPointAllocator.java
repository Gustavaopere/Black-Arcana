package dev.gustavopere.blackarcana.content.projection;

import java.util.Objects;

/** Diminishing-return point allocator for Oathforged Ascension. */
public final class AscensionPointAllocator {
    private AscensionPointAllocator() { }

    public static Allocation allocate(Sacrifice sacrifice, Policy policy) {
        Objects.requireNonNull(sacrifice, "sacrifice");
        Objects.requireNonNull(policy, "policy");
        if (sacrifice.alreadyBlackArcanaAugmented()) {
            return new Allocation(false, 0, "recursive_input");
        }
        if (sacrifice.eligibleValue() <= 0.0D) {
            return new Allocation(false, 0, "no_eligible_value");
        }
        double normalized = sacrifice.eligibleValue() / policy.valueScale();
        int points = (int) Math.floor(Math.pow(normalized, policy.diminishingExponent()));
        points = Math.max(0, Math.min(points, policy.maxPointsPerRite()));
        return points <= 0 ? new Allocation(false, 0, "insufficient_value") : new Allocation(true, points, "");
    }

    public record Sacrifice(double eligibleValue, boolean alreadyBlackArcanaAugmented) {
        public Sacrifice {
            if (!Double.isFinite(eligibleValue) || eligibleValue < 0.0D) throw new IllegalArgumentException("eligibleValue invalid");
        }
    }

    public record Policy(double valueScale, double diminishingExponent, int maxPointsPerRite) {
        public Policy {
            if (!Double.isFinite(valueScale) || valueScale <= 0.0D) throw new IllegalArgumentException("valueScale invalid");
            if (!Double.isFinite(diminishingExponent) || diminishingExponent <= 0.0D || diminishingExponent >= 1.0D) {
                throw new IllegalArgumentException("diminishingExponent must be in (0,1)");
            }
            if (maxPointsPerRite <= 0 || maxPointsPerRite > ProjectionSafetyCeilings.MAX_ASCENSION_POINTS) {
                throw new IllegalArgumentException("maxPointsPerRite outside hard ceiling");
            }
        }
    }

    public record Allocation(boolean accepted, int points, String denialCode) {
        public Allocation { Objects.requireNonNull(denialCode, "denialCode"); }
    }
}
