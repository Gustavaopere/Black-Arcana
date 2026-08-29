package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * Explicit containment metadata for one equipment item.
 * Vanilla armor/toughness never implies a profile; providers must register one deliberately.
 */
public record ArcaneEquipmentProfile(
    String profileId,
    double arcaneResistance,
    double corruptionResistance,
    double strainCapacityBonus,
    double strainRecoveryPerTick,
    String setId,
    Set<String> containmentTags
) {
    public static final double ABSOLUTE_MAX_RESISTANCE = 10_000.0D;
    public static final double ABSOLUTE_MAX_STRAIN_CAPACITY = 10_000.0D;
    public static final double ABSOLUTE_MAX_STRAIN_RECOVERY = 100.0D;
    private static final Pattern ID = Pattern.compile("[a-z0-9_.:/-]{1,96}");

    public ArcaneEquipmentProfile {
        requireId(profileId, "profileId");
        validateBounded(arcaneResistance, ABSOLUTE_MAX_RESISTANCE, "arcaneResistance");
        validateBounded(corruptionResistance, ABSOLUTE_MAX_RESISTANCE, "corruptionResistance");
        validateBounded(strainCapacityBonus, ABSOLUTE_MAX_STRAIN_CAPACITY, "strainCapacityBonus");
        validateBounded(strainRecoveryPerTick, ABSOLUTE_MAX_STRAIN_RECOVERY, "strainRecoveryPerTick");
        if (setId != null && !setId.isBlank()) requireId(setId, "setId");
        setId = setId == null || setId.isBlank() ? null : setId;
        containmentTags = Set.copyOf(Objects.requireNonNull(containmentTags, "containmentTags"));
        if (containmentTags.size() > 32) throw new IllegalArgumentException("too many containment tags");
        for (String tag : containmentTags) requireId(tag, "containmentTag");
    }

    public static ArcaneEquipmentProfile resistanceOnly(String profileId, double arcane, double corruption) {
        return new ArcaneEquipmentProfile(profileId, arcane, corruption, 0.0D, 0.0D, null, Set.of());
    }

    private static void validateBounded(double value, double max, String name) {
        if (!Double.isFinite(value) || value < 0.0D || value > max) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }

    private static void requireId(String value, String name) {
        Objects.requireNonNull(value, name);
        if (!ID.matcher(value).matches()) throw new IllegalArgumentException("invalid " + name + ": " + value);
    }
}
