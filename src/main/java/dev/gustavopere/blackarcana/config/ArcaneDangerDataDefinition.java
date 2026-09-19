package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Strict declarative danger-profile data; no executable hooks are accepted from datapacks. */
public record ArcaneDangerDataDefinition(
    int schemaVersion,
    int profileVersion,
    String id,
    ArcaneDangerTier tier,
    double backlashMultiplier,
    double corruptionCoefficient,
    double strainCoefficient,
    long damageLeaseTicks,
    int maxDamageInstances,
    double minimumArcaneResistance,
    double recommendedArcaneResistance,
    ArcaneInsufficientResistancePolicy belowMinimumPolicy,
    boolean emergencyProtectionAllowed
) {
    public static final int CURRENT_SCHEMA_VERSION = 1;
    public static final int MAX_PROFILE_VERSION = 1_000_000;
    public static final double ABSOLUTE_MAX_RESISTANCE_HINT = 10_000.0D;

    /** Compatibility constructor preserving the pre-policy schema-v1 default: below minimum is a hard denial. */
    public ArcaneDangerDataDefinition(
        int schemaVersion,
        int profileVersion,
        String id,
        ArcaneDangerTier tier,
        double backlashMultiplier,
        double corruptionCoefficient,
        double strainCoefficient,
        long damageLeaseTicks,
        int maxDamageInstances,
        double minimumArcaneResistance,
        double recommendedArcaneResistance,
        boolean emergencyProtectionAllowed
    ) {
        this(
            schemaVersion,
            profileVersion,
            id,
            tier,
            backlashMultiplier,
            corruptionCoefficient,
            strainCoefficient,
            damageLeaseTicks,
            maxDamageInstances,
            minimumArcaneResistance,
            recommendedArcaneResistance,
            ArcaneInsufficientResistancePolicy.DENY_CAST,
            emergencyProtectionAllowed);
    }

    public ArcaneDangerDataDefinition {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(tier, "tier");
        Objects.requireNonNull(belowMinimumPolicy, "belowMinimumPolicy");
    }

    public List<String> validate() {
        List<String> errors = new ArrayList<>();
        if (schemaVersion != CURRENT_SCHEMA_VERSION) errors.add("unsupported schemaVersion: " + schemaVersion);
        if (profileVersion <= 0 || profileVersion > MAX_PROFILE_VERSION) errors.add("profileVersion outside bounds");
        try { ArcanaSpellId.parse(id); } catch (RuntimeException invalid) { errors.add("invalid spell id"); }
        validateFinite(errors, minimumArcaneResistance, "minimumArcaneResistance");
        validateFinite(errors, recommendedArcaneResistance, "recommendedArcaneResistance");
        if (minimumArcaneResistance > recommendedArcaneResistance) {
            errors.add("minimumArcaneResistance cannot exceed recommendedArcaneResistance");
        }
        try { toRuntimeProfile(); } catch (RuntimeException invalid) { errors.add(invalid.getMessage()); }
        return List.copyOf(errors);
    }

    public ArcaneDangerProfile toRuntimeProfile() {
        return new ArcaneDangerProfile(
            tier,
            backlashMultiplier,
            corruptionCoefficient,
            strainCoefficient,
            damageLeaseTicks,
            maxDamageInstances,
            minimumArcaneResistance,
            recommendedArcaneResistance,
            belowMinimumPolicy,
            emergencyProtectionAllowed);
    }

    private static void validateFinite(List<String> errors, double value, String name) {
        if (!Double.isFinite(value) || value < 0.0D || value > ABSOLUTE_MAX_RESISTANCE_HINT) {
            errors.add(name + " outside bounds");
        }
    }
}
