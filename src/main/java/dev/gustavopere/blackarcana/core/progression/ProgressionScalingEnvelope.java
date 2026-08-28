package dev.gustavopere.blackarcana.core.progression;

/** Local Black Arcana cap envelope applied after external RPG data is read. */
public record ProgressionScalingEnvelope(double baseMultiplier, double hardCapMultiplier, double knee) {
    public ProgressionScalingEnvelope {
        if (!Double.isFinite(baseMultiplier) || !Double.isFinite(hardCapMultiplier) || !Double.isFinite(knee)
            || baseMultiplier < 0D || hardCapMultiplier < baseMultiplier || knee <= 0D) {
            throw new IllegalArgumentException("invalid progression scaling envelope");
        }
    }

    public double multiplier(long attributeRank, int masteryXp, double attributeWeight, double masteryWeight) {
        if (attributeRank < 0L || masteryXp < 0) throw new IllegalArgumentException("progression values cannot be negative");
        if (!Double.isFinite(attributeWeight) || !Double.isFinite(masteryWeight) || attributeWeight < 0D || masteryWeight < 0D) {
            throw new IllegalArgumentException("weights must be finite and non-negative");
        }
        double raw = Math.min(Double.MAX_VALUE / 4D,
            attributeRank * attributeWeight + masteryXp * masteryWeight);
        return DiminishingReturnsCurve.apply(baseMultiplier, raw, hardCapMultiplier, knee);
    }
}
