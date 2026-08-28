package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;

/** Normalized 0..10 dimensions used to compare unlike techniques on one auditable rubric. */
public record TechniqueBudgetProfile(
    ArcanaSpellId spellId,
    TechniqueTier tier,
    int burstDps,
    int area,
    int control,
    int mobility,
    int survivability,
    int utility,
    int efficiency,
    int setupBurden,
    int riskBurden,
    int resourceBurden,
    int cooldownBurden,
    BalanceBenchmark benchmark
) {
    public TechniqueBudgetProfile {
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(tier, "tier");
        Objects.requireNonNull(benchmark, "benchmark");
        int[] values = {burstDps, area, control, mobility, survivability, utility, efficiency,
            setupBurden, riskBurden, resourceBurden, cooldownBurden};
        for (int value : values) if (value < 0 || value > 10) throw new IllegalArgumentException("budget dimensions must be 0..10");
    }

    public double outputScore() {
        return burstDps + area + control + mobility + survivability + utility + efficiency;
    }

    public double compensationScore() {
        return (setupBurden + riskBurden + resourceBurden + cooldownBurden) * 0.5D;
    }

    public double adjustedScore() {
        return Math.max(0D, outputScore() - compensationScore());
    }

    public BudgetAssessment assess() {
        double adjusted = adjustedScore();
        double ceiling = tier.adjustedBudget();
        return new BudgetAssessment(adjusted, ceiling, adjusted <= ceiling,
            adjusted <= ceiling ? 0D : adjusted - ceiling);
    }

    public record BudgetAssessment(double adjustedScore, double tierCeiling, boolean withinBudget, double overshoot) {
        public BudgetAssessment {
            if (!Double.isFinite(adjustedScore) || !Double.isFinite(tierCeiling) || !Double.isFinite(overshoot)
                || adjustedScore < 0D || tierCeiling < 0D || overshoot < 0D) {
                throw new IllegalArgumentException("assessment values must be finite and non-negative");
            }
        }
    }
}
