package dev.gustavopere.blackarcana.integration.rpg;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/** Explicit mapping from canonical RPG attribute ids to Black Arcana resistance channels. */
public record RpgHazardResistanceConfig(
    Map<String, Double> arcaneResistancePerRank,
    Map<String, Double> corruptionResistancePerRank,
    double maxArcaneContribution,
    double maxCorruptionContribution
) {
    public static final int MAX_ATTRIBUTE_MAPPINGS = 16;
    public static final double ABSOLUTE_MAX_PER_RANK = 100.0D;
    public static final double ABSOLUTE_MAX_TOTAL = 10_000.0D;

    public RpgHazardResistanceConfig {
        arcaneResistancePerRank = validateMap(arcaneResistancePerRank);
        corruptionResistancePerRank = validateMap(corruptionResistancePerRank);
        validateTotal(maxArcaneContribution, "maxArcaneContribution");
        validateTotal(maxCorruptionContribution, "maxCorruptionContribution");
    }

    /** Deliberately conservative; balance can override without changing the adapter. */
    public static RpgHazardResistanceConfig canonical() {
        return new RpgHazardResistanceConfig(
            Map.of("determination", 1.0D, "intelligence", 0.25D),
            Map.of("constitution", 1.0D, "determination", 0.25D),
            250.0D,
            250.0D);
    }

    private static Map<String, Double> validateMap(Map<String, Double> input) {
        Objects.requireNonNull(input, "input");
        if (input.size() > MAX_ATTRIBUTE_MAPPINGS) throw new IllegalArgumentException("too many RPG hazard mappings");
        LinkedHashMap<String, Double> result = new LinkedHashMap<>();
        input.forEach((id, coefficient) -> {
            if (id == null || !id.matches("[a-z0-9_.-]{1,64}")) throw new IllegalArgumentException("invalid RPG attribute id: " + id);
            if (coefficient == null || !Double.isFinite(coefficient) || coefficient < 0.0D || coefficient > ABSOLUTE_MAX_PER_RANK) {
                throw new IllegalArgumentException("invalid RPG hazard coefficient: " + id);
            }
            result.put(id, coefficient);
        });
        return Map.copyOf(result);
    }

    private static void validateTotal(double value, String name) {
        if (!Double.isFinite(value) || value < 0.0D || value > ABSOLUTE_MAX_TOTAL) {
            throw new IllegalArgumentException(name + " outside bounds");
        }
    }
}
