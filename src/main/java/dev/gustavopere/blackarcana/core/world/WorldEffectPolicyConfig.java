package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Map;
import java.util.Objects;

public record WorldEffectPolicyConfig(
    WorldEffectMode globalMode,
    int globalMaxAffectedUnits,
    boolean entityDamageAllowed,
    Map<ArcanaSpellId, WorldEffectOverride> spellOverrides
) {
    public WorldEffectPolicyConfig {
        Objects.requireNonNull(globalMode, "globalMode");
        Objects.requireNonNull(spellOverrides, "spellOverrides");
        if (globalMaxAffectedUnits <= 0 || globalMaxAffectedUnits > WorldEffectProfile.ABSOLUTE_MAX_AFFECTED_UNITS) {
            throw new IllegalArgumentException("globalMaxAffectedUnits outside absolute safety bounds");
        }
        spellOverrides = Map.copyOf(spellOverrides);
    }

    public static WorldEffectPolicyConfig safeDefaults() {
        return new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of());
    }
}
