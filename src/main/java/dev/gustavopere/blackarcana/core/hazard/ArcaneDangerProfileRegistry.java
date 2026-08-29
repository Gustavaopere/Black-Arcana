package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Server-owned atomically replaceable danger profiles keyed by canonical spell id. */
public final class ArcaneDangerProfileRegistry {
    public static final int MAX_PROFILES = 4_096;
    private volatile Map<ArcanaSpellId, ArcaneDangerProfile> profiles = Map.of();

    public Optional<ArcaneDangerProfile> resolve(ArcanaSpellId spellId) {
        return Optional.ofNullable(profiles.get(Objects.requireNonNull(spellId, "spellId")));
    }

    public ArcaneDangerProfile requireHazardous(ArcanaSpellId spellId) {
        ArcaneDangerProfile profile = resolve(spellId).orElseThrow(
            () -> new IllegalStateException("missing required danger profile: " + spellId.canonical()));
        if (!profile.requiresHazardSession()) {
            throw new IllegalStateException("required danger profile is not hazardous: " + spellId.canonical());
        }
        return profile;
    }

    public synchronized void replaceAll(Map<ArcanaSpellId, ArcaneDangerProfile> replacement) {
        Objects.requireNonNull(replacement, "replacement");
        if (replacement.size() > MAX_PROFILES) throw new IllegalArgumentException("too many danger profiles");
        LinkedHashMap<ArcanaSpellId, ArcaneDangerProfile> validated = new LinkedHashMap<>();
        replacement.forEach((id, profile) -> {
            Objects.requireNonNull(id, "profile id");
            Objects.requireNonNull(profile, "profile");
            if (validated.putIfAbsent(id, profile) != null) {
                throw new IllegalArgumentException("duplicate danger profile: " + id.canonical());
            }
        });
        profiles = Map.copyOf(validated);
    }

    public Map<ArcanaSpellId, ArcaneDangerProfile> snapshot() {
        return profiles;
    }
}
