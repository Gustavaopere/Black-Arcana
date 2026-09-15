package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Bounded server-owned registry declaring which canonical spells support the
 * Stage 02 channel lifecycle and the exact duration contract used by it.
 *
 * <p>Registration is deliberately first-writer-wins: a later integration may
 * not silently replace another subsystem's channel contract for the same spell.
 * Balance/profile reload belongs in an explicit reviewed authority rather than
 * mutation through this registry.</p>
 */
public final class ArcanaChannelSpecRegistry {
    private final int maxEntries;
    private final Map<ArcanaSpellId, ArcanaChannelSpec> specs = new LinkedHashMap<>();

    public ArcanaChannelSpecRegistry(int maxEntries) {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries must be positive");
        this.maxEntries = maxEntries;
    }

    public synchronized boolean register(ArcanaSpellId spellId, ArcanaChannelSpec spec) {
        ArcanaSpellId checkedId = Objects.requireNonNull(spellId, "spellId");
        ArcanaChannelSpec checkedSpec = Objects.requireNonNull(spec, "spec");
        if (specs.containsKey(checkedId) || specs.size() >= maxEntries) return false;
        specs.put(checkedId, checkedSpec);
        return true;
    }

    public synchronized Optional<ArcanaChannelSpec> resolve(ArcanaSpellId spellId) {
        return Optional.ofNullable(specs.get(Objects.requireNonNull(spellId, "spellId")));
    }

    public synchronized Map<ArcanaSpellId, ArcanaChannelSpec> snapshot() {
        return Map.copyOf(specs);
    }
}
