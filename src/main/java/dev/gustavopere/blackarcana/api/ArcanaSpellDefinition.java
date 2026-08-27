package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaSpellDefinition(
        ArcanaSpellId id,
        String translationKey,
        String iconId,
        ArcanaCost cost,
        boolean requestsWorldMutation
) {
    public ArcanaSpellDefinition {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(translationKey, "translationKey");
        Objects.requireNonNull(iconId, "iconId");
        Objects.requireNonNull(cost, "cost");
        if (translationKey.isBlank() || iconId.isBlank()) {
            throw new IllegalArgumentException("presentation metadata cannot be blank");
        }
    }
}
