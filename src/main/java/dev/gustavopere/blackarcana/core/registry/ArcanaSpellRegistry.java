package dev.gustavopere.blackarcana.core.registry;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastRequestValidator;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public final class ArcanaSpellRegistry implements CastRequestValidator {
    private volatile Map<ArcanaSpellId, ArcanaSpellDefinition> definitions = Map.of();

    public synchronized void replaceAll(Collection<ArcanaSpellDefinition> newDefinitions) {
        Objects.requireNonNull(newDefinitions, "newDefinitions");
        Map<ArcanaSpellId, ArcanaSpellDefinition> next = new LinkedHashMap<>();
        for (ArcanaSpellDefinition definition : newDefinitions) {
            Objects.requireNonNull(definition, "definition");
            ArcanaSpellDefinition previous = next.putIfAbsent(definition.id(), definition);
            if (previous != null) {
                throw new IllegalArgumentException("duplicate spell definition: " + definition.id().canonical());
            }
        }
        definitions = Map.copyOf(next);
    }

    public Optional<ArcanaSpellDefinition> resolve(ArcanaSpellId id) {
        return Optional.ofNullable(definitions.get(Objects.requireNonNull(id, "id")));
    }

    public Map<ArcanaSpellId, ArcanaSpellDefinition> snapshot() {
        return definitions;
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        ArcanaSpellDefinition canonical = definitions.get(request.spell().id());
        if (canonical == null) {
            return ArcanaDecision.deny("unknown_spell", "spell is not registered on the server");
        }
        if (!canonical.equals(request.spell())) {
            return ArcanaDecision.deny("spell_definition_mismatch", "request does not use the canonical server spell definition");
        }
        return ArcanaDecision.allow();
    }
}
