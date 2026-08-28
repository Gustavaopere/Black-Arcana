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
    private volatile Map<ArcanaSpellId, SpellDataDefinition> definitions = Map.of();

    public synchronized void replaceAll(Collection<SpellDataDefinition> newDefinitions) {
        Objects.requireNonNull(newDefinitions, "newDefinitions");
        if (newDefinitions.size() > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new IllegalArgumentException("too many spell data definitions: " + newDefinitions.size());
        }

        Map<ArcanaSpellId, SpellDataDefinition> next = new LinkedHashMap<>();
        for (SpellDataDefinition definition : newDefinitions) {
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
        definitions = Map.copyOf(next);
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
}
