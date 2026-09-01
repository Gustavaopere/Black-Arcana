package dev.gustavopere.blackarcana.core.ritual;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Bounded canonical ritual-definition registry owned by the server runtime. */
public final class RitualDefinitionRegistry {
    private final int maxDefinitions;
    private final Map<ArcanaRitualId, RitualDefinition> definitions = new LinkedHashMap<>();

    public RitualDefinitionRegistry(int maxDefinitions) {
        if (maxDefinitions <= 0 || maxDefinitions > 4_096) {
            throw new IllegalArgumentException("maxDefinitions outside bounds");
        }
        this.maxDefinitions = maxDefinitions;
    }

    public synchronized void register(RitualDefinition definition) {
        Objects.requireNonNull(definition, "definition");
        if (definitions.containsKey(definition.id())) {
            throw new IllegalStateException("duplicate ritual definition: " + definition.id().canonical());
        }
        if (definitions.size() >= maxDefinitions) {
            throw new IllegalStateException("ritual definition registry is full");
        }
        definitions.put(definition.id(), definition);
    }

    public synchronized Optional<RitualDefinition> resolve(ArcanaRitualId id) {
        return Optional.ofNullable(definitions.get(Objects.requireNonNull(id, "id")));
    }

    public synchronized List<RitualDefinition> snapshot() {
        return List.copyOf(new ArrayList<>(definitions.values()));
    }

    public synchronized int size() {
        return definitions.size();
    }
}
