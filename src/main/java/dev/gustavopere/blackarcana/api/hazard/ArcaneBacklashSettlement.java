package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;

/** One deterministic ledger result. Backlash application happens outside the pure ledger. */
public record ArcaneBacklashSettlement(
    Status status,
    double confirmedHealthDamage,
    double deltaEligibleDamage,
    double backlashDamage,
    String code
) {
    public enum Status { SETTLED, IGNORED, DENIED }

    public ArcaneBacklashSettlement {
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(code, "code");
        validateFinite("confirmedHealthDamage", confirmedHealthDamage);
        validateFinite("deltaEligibleDamage", deltaEligibleDamage);
        validateFinite("backlashDamage", backlashDamage);
        if (status == Status.SETTLED && !code.isEmpty()) {
            throw new IllegalArgumentException("settled result cannot carry a denial code");
        }
        if (status != Status.SETTLED && code.isBlank()) {
            throw new IllegalArgumentException("non-settled result requires a code");
        }
    }

    public static ArcaneBacklashSettlement settled(double confirmed, double eligible, double backlash) {
        return new ArcaneBacklashSettlement(Status.SETTLED, confirmed, eligible, backlash, "");
    }

    public static ArcaneBacklashSettlement ignored(double confirmed, String code) {
        return new ArcaneBacklashSettlement(Status.IGNORED, confirmed, 0.0D, 0.0D, code);
    }

    public static ArcaneBacklashSettlement denied(double confirmed, String code) {
        return new ArcaneBacklashSettlement(Status.DENIED, confirmed, 0.0D, 0.0D, code);
    }

    private static void validateFinite(String name, double value) {
        if (!Double.isFinite(value) || value < 0.0D) {
            throw new IllegalArgumentException(name + " must be finite and non-negative");
        }
    }
}
