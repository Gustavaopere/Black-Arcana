package dev.gustavopere.blackarcana.integration.rpg;

import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;

/** Mod-agnostic Black Arcana projection of the RPG Skill Tree state. */
public record RpgProgressionSnapshot(
    long level,
    Map<String, Long> attributeRanks,
    Map<String, Integer> masteryExperience
) {
    private static final Pattern KEY = Pattern.compile("[a-z0-9_.:-]{1,64}");

    public RpgProgressionSnapshot {
        if (level < 0L) throw new IllegalArgumentException("level cannot be negative");
        Objects.requireNonNull(attributeRanks, "attributeRanks");
        Objects.requireNonNull(masteryExperience, "masteryExperience");
        attributeRanks = Map.copyOf(attributeRanks);
        masteryExperience = Map.copyOf(masteryExperience);
        attributeRanks.forEach((key, value) -> {
            validateKey(key, "attribute");
            if (value == null || value < 0L) throw new IllegalArgumentException("attribute rank cannot be negative");
        });
        masteryExperience.forEach((key, value) -> {
            validateKey(key, "mastery");
            if (value == null || value < 0) throw new IllegalArgumentException("mastery XP cannot be negative");
        });
    }

    public long attributeRank(String attributeId) {
        return attributeRanks.getOrDefault(attributeId, 0L);
    }

    public int masteryXp(String laneId) {
        return masteryExperience.getOrDefault(laneId, 0);
    }

    static void validateKey(String key, String label) {
        Objects.requireNonNull(key, label + " key");
        if (!KEY.matcher(key).matches()) {
            throw new IllegalArgumentException("invalid " + label + " key: " + key);
        }
    }
}
