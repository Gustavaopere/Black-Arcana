package dev.gustavopere.blackarcana.api.hazard;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Immutable, reproducible resistance result committed to one hazard snapshot. */
public record ArcaneResistanceSnapshot(
    double effectiveResistance,
    double residualBacklashMultiplier,
    double curveK,
    double maxResistance,
    List<ResolvedContribution> contributions,
    Map<ArcaneResistanceSourceCategory, Double> effectiveByCategory,
    List<String> diagnostics
) {
    public ArcaneResistanceSnapshot {
        if (!Double.isFinite(effectiveResistance) || effectiveResistance < 0.0D) {
            throw new IllegalArgumentException("effectiveResistance must be finite and non-negative");
        }
        if (!Double.isFinite(residualBacklashMultiplier)
            || residualBacklashMultiplier < 0.0D || residualBacklashMultiplier > 1.0D) {
            throw new IllegalArgumentException("residualBacklashMultiplier outside [0,1]");
        }
        if (!Double.isFinite(curveK) || curveK <= 0.0D) throw new IllegalArgumentException("curveK must be positive");
        if (!Double.isFinite(maxResistance) || maxResistance <= 0.0D) {
            throw new IllegalArgumentException("maxResistance must be positive");
        }
        Objects.requireNonNull(contributions, "contributions");
        Objects.requireNonNull(effectiveByCategory, "effectiveByCategory");
        Objects.requireNonNull(diagnostics, "diagnostics");
        contributions = List.copyOf(contributions);
        diagnostics = List.copyOf(diagnostics);
        EnumMap<ArcaneResistanceSourceCategory, Double> copy =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            Double value = effectiveByCategory.get(category);
            if (value == null || !Double.isFinite(value) || value < 0.0D) {
                throw new IllegalArgumentException("missing/invalid category resistance: " + category);
            }
            copy.put(category, value);
        }
        effectiveByCategory = Collections.unmodifiableMap(copy);
    }

    public record ResolvedContribution(
        String providerId,
        String sourceId,
        ArcaneResistanceSourceCategory category,
        double amount
    ) {
        public ResolvedContribution {
            Objects.requireNonNull(providerId, "providerId");
            Objects.requireNonNull(sourceId, "sourceId");
            Objects.requireNonNull(category, "category");
            if (providerId.isBlank() || sourceId.isBlank()) {
                throw new IllegalArgumentException("resolved contribution ids cannot be blank");
            }
            if (!Double.isFinite(amount) || amount < 0.0D) {
                throw new IllegalArgumentException("resolved contribution amount must be finite and non-negative");
            }
        }
    }
}
