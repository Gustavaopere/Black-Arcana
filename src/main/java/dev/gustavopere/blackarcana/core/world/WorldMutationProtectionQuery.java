package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.UUID;

/** Provider-neutral claim/protection query for one exact Black Arcana block mutation. */
public record WorldMutationProtectionQuery(
    UUID casterId,
    ArcanaCastId castId,
    ArcanaSpellId spellId,
    TemporaryMutationKey key,
    WorldMutationType mutationType,
    WorldMutationClass mutationClass
) {
    public WorldMutationProtectionQuery {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(mutationType, "mutationType");
        Objects.requireNonNull(mutationClass, "mutationClass");
    }

    public String dimensionId() {
        return key.dimensionId();
    }
}
