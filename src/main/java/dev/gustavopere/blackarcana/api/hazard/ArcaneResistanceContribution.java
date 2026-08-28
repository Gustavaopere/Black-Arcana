package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.regex.Pattern;

/** One read-only resistance contribution returned by a provider. */
public record ArcaneResistanceContribution(
    String sourceId,
    ArcaneResistanceSourceCategory category,
    double amount
) {
    public static final double ABSOLUTE_MAX_AMOUNT = 10_000.0D;
    private static final Pattern SOURCE_ID = Pattern.compile("[a-z0-9_.:/-]{1,96}");

    public ArcaneResistanceContribution {
        Objects.requireNonNull(sourceId, "sourceId");
        Objects.requireNonNull(category, "category");
        if (!SOURCE_ID.matcher(sourceId).matches()) {
            throw new IllegalArgumentException("invalid resistance source id: " + sourceId);
        }
        if (!Double.isFinite(amount) || amount < 0.0D || amount > ABSOLUTE_MAX_AMOUNT) {
            throw new IllegalArgumentException("resistance amount outside absolute bounds");
        }
    }
}
