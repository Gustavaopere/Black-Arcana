package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Validated rename graph for cooldown/charge group ids. Removed groups are
 * handled separately by the active-policy pruning pass.
 */
public final class RuntimeGroupMigrations {
    private final Map<String, String> replacements;

    public RuntimeGroupMigrations(Map<String, String> replacements) {
        this.replacements = Map.copyOf(Objects.requireNonNull(replacements, "replacements"));
        this.replacements.forEach((from, to) -> {
            ArcanaSpellId.parse(Objects.requireNonNull(from, "source group id"));
            ArcanaSpellId.parse(Objects.requireNonNull(to, "target group id"));
            if (from.equals(to)) throw new IllegalArgumentException("group migration cannot replace an id with itself: " + from);
        });
        this.replacements.keySet().forEach(this::resolve);
    }

    public static RuntimeGroupMigrations none() {
        return new RuntimeGroupMigrations(Map.of());
    }

    public String resolve(String original) {
        ArcanaSpellId.parse(Objects.requireNonNull(original, "original"));
        Set<String> seen = new LinkedHashSet<>();
        String current = original;
        while (true) {
            if (!seen.add(current)) {
                String chain = seen.stream().collect(Collectors.joining(" -> "));
                throw new IllegalArgumentException("cyclic runtime group migration: " + chain + " -> " + current);
            }
            String next = replacements.get(current);
            if (next == null) return current;
            current = next;
        }
    }

    public boolean isEmpty() {
        return replacements.isEmpty();
    }
}
