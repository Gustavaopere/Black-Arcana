package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.regex.Pattern;

/** Extra lazy recovery supplied by a rest, ritual, equipment or buff provider. */
public record ArcaneStrainRecoveryContribution(String sourceId, double bonusUnitsPerTick) {
    public static final double ABSOLUTE_MAX_BONUS_PER_TICK = 100.0D;
    private static final Pattern SOURCE_ID = Pattern.compile("[a-z0-9_.:/-]{1,96}");

    public ArcaneStrainRecoveryContribution {
        Objects.requireNonNull(sourceId, "sourceId");
        if (!SOURCE_ID.matcher(sourceId).matches()) {
            throw new IllegalArgumentException("invalid strain recovery source id: " + sourceId);
        }
        if (!Double.isFinite(bonusUnitsPerTick) || bonusUnitsPerTick < 0.0D
            || bonusUnitsPerTick > ABSOLUTE_MAX_BONUS_PER_TICK) {
            throw new IllegalArgumentException("bonusUnitsPerTick outside absolute bounds");
        }
    }
}
