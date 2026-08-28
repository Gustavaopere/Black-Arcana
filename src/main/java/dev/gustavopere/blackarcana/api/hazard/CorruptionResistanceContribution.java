package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.regex.Pattern;

/** One read-only contribution to the independent Corruption Resistance channel. */
public record CorruptionResistanceContribution(
    String sourceId,
    CorruptionResistanceSourceCategory category,
    double amount
) {
    public static final double ABSOLUTE_MAX_AMOUNT = 10_000.0D;
    private static final Pattern SOURCE_ID = Pattern.compile("[a-z0-9_.:/-]{1,96}");

    public CorruptionResistanceContribution {
        Objects.requireNonNull(sourceId, "sourceId");
        Objects.requireNonNull(category, "category");
        if (!SOURCE_ID.matcher(sourceId).matches()) {
            throw new IllegalArgumentException("invalid corruption resistance source id: " + sourceId);
        }
        if (!Double.isFinite(amount) || amount < 0.0D || amount > ABSOLUTE_MAX_AMOUNT) {
            throw new IllegalArgumentException("corruption resistance amount outside absolute bounds");
        }
    }
}
