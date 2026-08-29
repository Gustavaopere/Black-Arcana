package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;

/** Declarative cumulative threshold bonus for one explicit containment equipment set. */
public record ArcaneEquipmentSetBonus(
    String bonusId,
    String setId,
    int requiredPieces,
    double arcaneResistance,
    double corruptionResistance,
    double strainCapacityBonus,
    double strainRecoveryPerTick,
    Set<String> containmentTags
) {
    public static final int MAX_REQUIRED_PIECES = 32;
    private static final Pattern ID = Pattern.compile("[a-z0-9_.:/-]{1,96}");

    public ArcaneEquipmentSetBonus {
        requireId(bonusId, "bonusId");
        requireId(setId, "setId");
        if (requiredPieces <= 0 || requiredPieces > MAX_REQUIRED_PIECES) {
            throw new IllegalArgumentException("requiredPieces outside absolute bounds");
        }
        validateBounded(arcaneResistance, ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE, "arcaneResistance");
        validateBounded(corruptionResistance, ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE, "corruptionResistance");
        validateBounded(strainCapacityBonus, ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_CAPACITY, "strainCapacityBonus");
        validateBounded(strainRecoveryPerTick, ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_RECOVERY, "strainRecoveryPerTick");
        containmentTags = Set.copyOf(Objects.requireNonNull(containmentTags, "containmentTags"));
        if (containmentTags.size() > 32) throw new IllegalArgumentException("too many containment tags");
        for (String tag : containmentTags) requireId(tag, "containmentTag");
    }

    private static void validateBounded(double value, double maximum, String name) {
        if (!Double.isFinite(value) || value < 0.0D || value > maximum) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }

    private static void requireId(String value, String name) {
        Objects.requireNonNull(value, name);
        if (!ID.matcher(value).matches()) throw new IllegalArgumentException("invalid " + name + ": " + value);
    }
}
