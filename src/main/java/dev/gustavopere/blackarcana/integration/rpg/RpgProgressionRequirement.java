package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import java.util.Map;
import java.util.Objects;

/** Attribute/mastery gate independent of the RPG mod's binary types. */
public record RpgProgressionRequirement(
    long minimumLevel,
    Map<String, Long> minimumAttributeRanks,
    Map<String, Integer> minimumMasteryExperience
) {
    public RpgProgressionRequirement {
        if (minimumLevel < 0L) throw new IllegalArgumentException("minimumLevel cannot be negative");
        Objects.requireNonNull(minimumAttributeRanks, "minimumAttributeRanks");
        Objects.requireNonNull(minimumMasteryExperience, "minimumMasteryExperience");
        minimumAttributeRanks = Map.copyOf(minimumAttributeRanks);
        minimumMasteryExperience = Map.copyOf(minimumMasteryExperience);
        minimumAttributeRanks.forEach((key, value) -> {
            RpgProgressionSnapshot.validateKey(key, "attribute");
            if (value == null || value < 0L) throw new IllegalArgumentException("minimum attribute rank cannot be negative");
        });
        minimumMasteryExperience.forEach((key, value) -> {
            RpgProgressionSnapshot.validateKey(key, "mastery");
            if (value == null || value < 0) throw new IllegalArgumentException("minimum mastery XP cannot be negative");
        });
    }

    public static RpgProgressionRequirement none() {
        return new RpgProgressionRequirement(0L, Map.of(), Map.of());
    }

    public ArcanaDecision evaluate(RpgProgressionSnapshot snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        if (snapshot.level() < minimumLevel) {
            return ArcanaDecision.deny(
                "rpg_level_too_low",
                "Requires RPG level " + minimumLevel + "; current level is " + snapshot.level());
        }

        for (String attribute : minimumAttributeRanks.keySet().stream().sorted().toList()) {
            long required = minimumAttributeRanks.get(attribute);
            long current = snapshot.attributeRank(attribute);
            if (current < required) {
                return ArcanaDecision.deny(
                    "rpg_attribute_too_low",
                    "Requires " + attribute + " " + required + "; current rank is " + current);
            }
        }

        for (String lane : minimumMasteryExperience.keySet().stream().sorted().toList()) {
            int required = minimumMasteryExperience.get(lane);
            int current = snapshot.masteryXp(lane);
            if (current < required) {
                return ArcanaDecision.deny(
                    "rpg_mastery_too_low",
                    "Requires mastery " + lane + " XP " + required + "; current XP is " + current);
            }
        }
        return ArcanaDecision.allow();
    }
}
