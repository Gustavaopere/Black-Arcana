package dev.gustavopere.blackarcana.core.registry;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.config.SpellDataDefinition;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;

import java.util.Collection;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public final class SpellDataCatalog {
    private volatile Map<ArcanaSpellId, SpellDataDefinition> declarativeDefinitions = Map.of();
    private volatile Map<ArcanaSpellId, SpellDataDefinition> syntheticDefinitions = Map.of();
    private volatile Map<ArcanaSpellId, SpellDataDefinition> definitions = Map.of();

    public synchronized void replaceAll(Collection<SpellDataDefinition> newDefinitions) {
        Objects.requireNonNull(newDefinitions, "newDefinitions");
        Map<ArcanaSpellId, SpellDataDefinition> nextDeclarative = validatedMap(newDefinitions);

        for (ArcanaSpellId id : nextDeclarative.keySet()) {
            if (syntheticDefinitions.containsKey(id)) {
                throw new IllegalArgumentException(
                        "declarative spell data collides with synthetic definition: " + id.canonical());
            }
        }

        Map<ArcanaSpellId, SpellDataDefinition> nextCombined = combine(nextDeclarative, syntheticDefinitions);
        declarativeDefinitions = Map.copyOf(nextDeclarative);
        definitions = nextCombined;
    }

    public synchronized void installSynthetic(SpellDataDefinition definition) {
        Objects.requireNonNull(definition, "definition");
        Map<ArcanaSpellId, SpellDataDefinition> validated = validatedMap(List.of(definition));
        Map.Entry<ArcanaSpellId, SpellDataDefinition> entry = validated.entrySet().iterator().next();
        ArcanaSpellId id = entry.getKey();

        if (declarativeDefinitions.containsKey(id)) {
            throw new IllegalArgumentException(
                    "synthetic spell data collides with declarative definition: " + id.canonical());
        }

        SpellDataDefinition existing = syntheticDefinitions.get(id);
        if (existing != null) {
            if (!existing.equals(definition)) {
                throw new IllegalStateException(
                        "synthetic spell data id already has a different definition: " + id.canonical());
            }
            return;
        }

        Map<ArcanaSpellId, SpellDataDefinition> nextSynthetic = new LinkedHashMap<>(syntheticDefinitions);
        nextSynthetic.put(id, definition);
        Map<ArcanaSpellId, SpellDataDefinition> immutableSynthetic = Map.copyOf(nextSynthetic);
        Map<ArcanaSpellId, SpellDataDefinition> nextCombined = combine(declarativeDefinitions, immutableSynthetic);
        syntheticDefinitions = immutableSynthetic;
        definitions = nextCombined;
    }

    public Optional<SpellDataDefinition> resolve(ArcanaSpellId id) {
        return Optional.ofNullable(definitions.get(Objects.requireNonNull(id, "id")));
    }

    public Map<ArcanaSpellId, SpellDataDefinition> snapshot() {
        return definitions;
    }

    public SpellPresentationPayload presentationPayload() {
        List<SpellPresentationPayload.Entry> entries = definitions.entrySet().stream()
                .sorted(Map.Entry.comparingByKey(Comparator.comparing(ArcanaSpellId::canonical)))
                .map(entry -> new SpellPresentationPayload.Entry(
                        entry.getKey().canonical(),
                        entry.getValue().translationKey(),
                        entry.getValue().iconId()))
                .toList();
        return new SpellPresentationPayload(ArcanaProtocol.VERSION, entries);
    }

    private static Map<ArcanaSpellId, SpellDataDefinition> validatedMap(
            Collection<SpellDataDefinition> candidateDefinitions) {
        if (candidateDefinitions.size() > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new IllegalArgumentException("too many spell data definitions: " + candidateDefinitions.size());
        }

        Map<ArcanaSpellId, SpellDataDefinition> next = new LinkedHashMap<>();
        for (SpellDataDefinition definition : candidateDefinitions) {
            Objects.requireNonNull(definition, "definition");
            List<String> errors = definition.validate();
            if (!errors.isEmpty()) {
                throw new IllegalArgumentException("invalid spell data " + definition.id() + ": " + String.join("; ", errors));
            }
            ArcanaSpellId id = ArcanaSpellId.parse(definition.id());
            if (next.putIfAbsent(id, definition) != null) {
                throw new IllegalArgumentException("duplicate spell data definition: " + id.canonical());
            }
        }
        return next;
    }

    private static Map<ArcanaSpellId, SpellDataDefinition> combine(
            Map<ArcanaSpellId, SpellDataDefinition> declarative,
            Map<ArcanaSpellId, SpellDataDefinition> synthetic) {
        int combinedSize = declarative.size() + synthetic.size();
        if (combinedSize > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new IllegalArgumentException("too many combined spell data definitions: " + combinedSize);
        }

        Map<ArcanaSpellId, SpellDataDefinition> combined = new LinkedHashMap<>(declarative);
        synthetic.forEach((id, definition) -> {
            if (combined.putIfAbsent(id, definition) != null) {
                throw new IllegalArgumentException("duplicate combined spell data definition: " + id.canonical());
            }
        });
        return Map.copyOf(combined);
    }
}
