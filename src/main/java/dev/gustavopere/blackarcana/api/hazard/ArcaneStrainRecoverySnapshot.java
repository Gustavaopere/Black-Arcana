package dev.gustavopere.blackarcana.api.hazard;

import java.util.List;
import java.util.Objects;

/** Immutable recovery calculation used by lazy decay and diagnostics. */
public record ArcaneStrainRecoverySnapshot(
    double baseUnitsPerTick,
    double bonusUnitsPerTick,
    double totalUnitsPerTick,
    List<ResolvedContribution> contributions,
    List<String> diagnostics
) {
    public ArcaneStrainRecoverySnapshot {
        if (!Double.isFinite(baseUnitsPerTick) || baseUnitsPerTick < 0.0D
            || !Double.isFinite(bonusUnitsPerTick) || bonusUnitsPerTick < 0.0D
            || !Double.isFinite(totalUnitsPerTick) || totalUnitsPerTick < 0.0D) {
            throw new IllegalArgumentException("strain recovery rates must be finite and non-negative");
        }
        contributions = List.copyOf(Objects.requireNonNull(contributions, "contributions"));
        diagnostics = List.copyOf(Objects.requireNonNull(diagnostics, "diagnostics"));
    }

    public record ResolvedContribution(String providerId, String sourceId, double bonusUnitsPerTick) {
        public ResolvedContribution {
            Objects.requireNonNull(providerId, "providerId");
            Objects.requireNonNull(sourceId, "sourceId");
            if (!Double.isFinite(bonusUnitsPerTick) || bonusUnitsPerTick < 0.0D) {
                throw new IllegalArgumentException("resolved recovery contribution must be finite and non-negative");
            }
        }
    }
}
