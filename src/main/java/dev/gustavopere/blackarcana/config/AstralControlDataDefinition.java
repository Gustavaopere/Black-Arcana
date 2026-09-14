package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Strict server-owned Astral control profile.
 *
 * <p>This record defines a bounded configuration surface only. It intentionally provides no default values:
 * an absent profile means production MOVE gameplay remains unavailable. Hard Noetic ceilings constrain
 * configured values but never become balance defaults.</p>
 */
public record AstralControlDataDefinition(
        int schemaVersion,
        String id,
        ConfigScope scope,
        double maxStepBlocks,
        float maxLookDeltaDegrees
) {
    public static final int CURRENT_SCHEMA_VERSION = 1;
    public static final String ASTRAL_SEVERANCE_ID = "black_arcana:astral_severance";

    public AstralControlDataDefinition {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(scope, "scope");
    }

    public List<String> validate() {
        List<String> errors = new ArrayList<>();
        if (schemaVersion != CURRENT_SCHEMA_VERSION) {
            errors.add("unsupported schemaVersion: " + schemaVersion);
        }
        if (!ASTRAL_SEVERANCE_ID.equals(id)) {
            errors.add("id must be " + ASTRAL_SEVERANCE_ID);
        }
        if (scope != ConfigScope.SERVER || !scope.isGameplayAuthority()) {
            errors.add("Astral control config must use SERVER gameplay authority");
        }
        if (!Double.isFinite(maxStepBlocks)
                || maxStepBlocks <= 0.0D
                || maxStepBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
            errors.add("maxStepBlocks outside hard Noetic bounds");
        }
        if (!Float.isFinite(maxLookDeltaDegrees)
                || maxLookDeltaDegrees <= 0.0F
                || maxLookDeltaDegrees > 180.0F) {
            errors.add("maxLookDeltaDegrees must be within (0, 180]");
        }
        return List.copyOf(errors);
    }

    public AstralSeveranceRuntime.ControlLimits toRuntimeLimits() {
        List<String> errors = validate();
        if (!errors.isEmpty()) {
            throw new IllegalArgumentException("invalid Astral control config: " + String.join("; ", errors));
        }
        return new AstralSeveranceRuntime.ControlLimits(maxStepBlocks, maxLookDeltaDegrees);
    }
}
