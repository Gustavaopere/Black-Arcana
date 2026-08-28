package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;

/** Per-spell server override. Overrides may only narrow global permissions at evaluation time. */
public record WorldEffectOverride(
    WorldEffectMode modeCap,
    int maxAffectedUnits,
    boolean entityDamageAllowed
) {
    public WorldEffectOverride {
        Objects.requireNonNull(modeCap, "modeCap");
        if (maxAffectedUnits <= 0 || maxAffectedUnits > WorldEffectProfile.ABSOLUTE_MAX_AFFECTED_UNITS) {
            throw new IllegalArgumentException("maxAffectedUnits outside absolute safety bounds");
        }
    }
}
