package dev.gustavopere.blackarcana.core.progression;

/** Normalized design-budget ceilings. These are balance targets, not technical safety ceilings. */
public enum TechniqueTier {
    T1(18D),
    T2(25D),
    T3(32D),
    T4_FORBIDDEN(40D);

    private final double adjustedBudget;
    TechniqueTier(double adjustedBudget) { this.adjustedBudget = adjustedBudget; }
    public double adjustedBudget() { return adjustedBudget; }
}
