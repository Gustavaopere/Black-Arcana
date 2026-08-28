package dev.gustavopere.blackarcana.api.hazard;

import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Immutable result of the independent Corruption Resistance provider channel. */
public record CorruptionResistanceSnapshot(
    double effectiveResistance,
    double baselineResidualMultiplier,
    double curveK,
    double maxResistance,
    List<ResolvedContribution> contributions,
    Map<CorruptionResistanceSourceCategory, Double> effectiveByCategory,
    List<String> diagnostics
) {
    public CorruptionResistanceSnapshot {
        if (!Double.isFinite(effectiveResistance) || effectiveResistance < 0.0D) {
            throw new IllegalArgumentException("effectiveResistance must be finite and non-negative");
        }
        if (!Double.isFinite(baselineResidualMultiplier)
            || baselineResidualMultiplier < 0.0D || baselineResidualMultiplier > 1.0D) {
            throw new IllegalArgumentException("baselineResidualMultiplier outside [0,1]");
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
        EnumMap<CorruptionResistanceSourceCategory, Double> copy =
            new EnumMap<>(CorruptionResistanceSourceCategory.class);
        for (CorruptionResistanceSourceCategory category : CorruptionResistanceSourceCategory.values()) {
            Double value = effectiveByCategory.get(category);
            if (value == null || !Double.isFinite(value) || value < 0.0D) {
                throw new IllegalArgumentException("missing/invalid corruption resistance category: " + category);
            }
            copy.put(category, value);
        }
        effectiveByCategory = Collections.unmodifiableMap(copy);
    }

    /** Applies profile-specific effectiveness/cap and the unavoidable acquisition floor. */
    public double residualMultiplier(CorruptionAcquisitionProfile profile) {
        Objects.requireNonNull(profile, "profile");
        double scaled = Math.min(maxResistance, effectiveResistance * profile.resistanceScale());
        double applied = Math.min(scaled, profile.maxResistanceApplied());
        double residual = curveK / (curveK + applied);
        if (!Double.isFinite(residual)) throw new IllegalStateException("corruption resistance produced non-finite residual");
        return Math.max(profile.unavoidableFloorMultiplier(), Math.max(0.0D, Math.min(1.0D, residual)));
    }

    public record ResolvedContribution(
        String providerId,
        String sourceId,
        CorruptionResistanceSourceCategory category,
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
