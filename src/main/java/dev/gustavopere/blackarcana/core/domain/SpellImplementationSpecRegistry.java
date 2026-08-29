package dev.gustavopere.blackarcana.core.domain;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Bounded registry used to prove that implemented Stage 07 mechanics have a complete specification. */
public final class SpellImplementationSpecRegistry {
    public static final int ABSOLUTE_MAX_SPECS = 256;

    private final int maxSpecs;
    private final Map<ArcanaSpellId, SpellImplementationSpec> specs = new LinkedHashMap<>();

    public SpellImplementationSpecRegistry(int maxSpecs) {
        if (maxSpecs <= 0 || maxSpecs > ABSOLUTE_MAX_SPECS) {
            throw new IllegalArgumentException("maxSpecs outside absolute bounds");
        }
        this.maxSpecs = maxSpecs;
    }

    public synchronized void register(SpellImplementationSpec spec) {
        Objects.requireNonNull(spec, "spec");
        if (specs.containsKey(spec.spellId())) {
            throw new IllegalStateException("duplicate spell implementation spec: " + spec.spellId().canonical());
        }
        if (specs.size() >= maxSpecs) {
            throw new IllegalStateException("spell implementation spec registry is full");
        }
        specs.put(spec.spellId(), spec);
    }

    public synchronized Optional<SpellImplementationSpec> find(ArcanaSpellId id) {
        return Optional.ofNullable(specs.get(Objects.requireNonNull(id, "id")));
    }

    public synchronized List<SpellImplementationSpec> snapshot() {
        return List.copyOf(specs.values());
    }
}
