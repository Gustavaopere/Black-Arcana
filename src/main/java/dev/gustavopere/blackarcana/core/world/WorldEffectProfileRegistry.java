package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Mutable only during bootstrap/configuration; reads are synchronized and fail closed on missing profiles. */
public final class WorldEffectProfileRegistry {
    private final Map<ArcanaSpellId, WorldEffectProfile> profiles = new HashMap<>();

    public synchronized void register(ArcanaSpellId spellId, WorldEffectProfile profile) {
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(profile, "profile");
        if (profiles.putIfAbsent(spellId, profile) != null) {
            throw new IllegalStateException("duplicate world-effect profile: " + spellId);
        }
    }

    public synchronized Optional<WorldEffectProfile> find(ArcanaSpellId spellId) {
        return Optional.ofNullable(profiles.get(Objects.requireNonNull(spellId, "spellId")));
    }

    public synchronized Map<ArcanaSpellId, WorldEffectProfile> snapshot() {
        return Map.copyOf(profiles);
    }
}
