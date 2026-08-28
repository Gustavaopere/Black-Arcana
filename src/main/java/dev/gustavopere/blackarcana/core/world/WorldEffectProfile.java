package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;

/** Static worst-case declaration required for every spell that requests world mutation. */
public record WorldEffectProfile(
    WorldMutationType mutationType,
    WorldMutationClass mutationClass,
    int maxAffectedUnits,
    boolean includesEntityDamage
) {
    public static final int ABSOLUTE_MAX_AFFECTED_UNITS = 65_536;

    public WorldEffectProfile {
        Objects.requireNonNull(mutationType, "mutationType");
        Objects.requireNonNull(mutationClass, "mutationClass");
        if (maxAffectedUnits <= 0 || maxAffectedUnits > ABSOLUTE_MAX_AFFECTED_UNITS) {
            throw new IllegalArgumentException("maxAffectedUnits outside absolute safety bounds");
        }
    }
}
