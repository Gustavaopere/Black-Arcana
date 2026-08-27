package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

public final class SpellIdMigrations {
    private final Map<ArcanaSpellId, ArcanaSpellId> replacements;
    private final Map<ArcanaSpellId, String> removals;

    public SpellIdMigrations(Map<ArcanaSpellId, ArcanaSpellId> replacements, Map<ArcanaSpellId, String> removals) {
        this.replacements = Map.copyOf(Objects.requireNonNull(replacements, "replacements"));
        this.removals = Map.copyOf(Objects.requireNonNull(removals, "removals"));

        for (Map.Entry<ArcanaSpellId, String> entry : this.removals.entrySet()) {
            if (entry.getValue().isBlank()) {
                throw new IllegalArgumentException("removal reason cannot be blank: " + entry.getKey().canonical());
            }
            if (this.replacements.containsKey(entry.getKey())) {
                throw new IllegalArgumentException("spell id cannot be both replaced and removed: " + entry.getKey().canonical());
            }
        }

        for (ArcanaSpellId id : this.replacements.keySet()) {
            walk(id);
        }
    }

    public Optional<ArcanaSpellId> resolve(ArcanaSpellId original) {
        return walk(Objects.requireNonNull(original, "original")).resolved();
    }

    public Optional<String> removalReason(ArcanaSpellId original) {
        return walk(Objects.requireNonNull(original, "original")).removalReason();
    }

    private Resolution walk(ArcanaSpellId original) {
        Set<ArcanaSpellId> seen = new LinkedHashSet<>();
        ArcanaSpellId current = original;

        while (true) {
            if (!seen.add(current)) {
                String chain = seen.stream().map(ArcanaSpellId::canonical).collect(Collectors.joining(" -> "));
                throw new IllegalArgumentException("cyclic spell id migration: " + chain + " -> " + current.canonical());
            }

            String reason = removals.get(current);
            if (reason != null) {
                return new Resolution(Optional.empty(), Optional.of(reason));
            }

            ArcanaSpellId next = replacements.get(current);
            if (next == null) {
                return new Resolution(Optional.of(current), Optional.empty());
            }
            current = next;
        }
    }

    private record Resolution(Optional<ArcanaSpellId> resolved, Optional<String> removalReason) {
    }
}
