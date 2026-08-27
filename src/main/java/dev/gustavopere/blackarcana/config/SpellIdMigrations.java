package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public final class SpellIdMigrations {
    private final Map<ArcanaSpellId, ArcanaSpellId> replacements;
    private final Map<ArcanaSpellId, String> removals;

    public SpellIdMigrations(Map<ArcanaSpellId, ArcanaSpellId> replacements, Map<ArcanaSpellId, String> removals) {
        this.replacements = Map.copyOf(Objects.requireNonNull(replacements));
        this.removals = Map.copyOf(Objects.requireNonNull(removals));
    }

    public Optional<ArcanaSpellId> resolve(ArcanaSpellId original) {
        Objects.requireNonNull(original, "original");
        if (removals.containsKey(original)) return Optional.empty();
        return Optional.of(replacements.getOrDefault(original, original));
    }

    public Optional<String> removalReason(ArcanaSpellId original) {
        return Optional.ofNullable(removals.get(original));
    }
}
