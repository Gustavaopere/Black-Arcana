package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Server-owned, atomically replaceable Strain behavior profiles keyed by canonical spell id. */
public final class ArcaneStrainProfileRegistry {
    public static final int MAX_PROFILES = 4_096;
    private volatile Map<ArcanaSpellId, ArcaneStrainProfile> profiles = Map.of();

    public Optional<ArcaneStrainProfile> resolve(ArcanaSpellId spellId) {
        return Optional.ofNullable(profiles.get(Objects.requireNonNull(spellId, "spellId")));
    }

    public ArcaneStrainProfile resolveOrCommittedCast(ArcanaSpellId spellId, double fallbackBaseUnits) {
        return resolve(spellId).orElseGet(() -> ArcaneStrainProfile.committedCastOnly(fallbackBaseUnits));
    }

    public synchronized void replaceAll(Map<ArcanaSpellId, ArcaneStrainProfile> replacement) {
        Objects.requireNonNull(replacement, "replacement");
        if (replacement.size() > MAX_PROFILES) throw new IllegalArgumentException("too many strain profiles");
        LinkedHashMap<ArcanaSpellId, ArcaneStrainProfile> validated = new LinkedHashMap<>();
        replacement.forEach((id, profile) -> {
            Objects.requireNonNull(id, "strain profile id");
            Objects.requireNonNull(profile, "strain profile");
            if (validated.putIfAbsent(id, profile) != null) {
                throw new IllegalArgumentException("duplicate strain profile: " + id.canonical());
            }
        });
        profiles = Map.copyOf(validated);
    }

    public Map<ArcanaSpellId, ArcaneStrainProfile> snapshot() {
        return profiles;
    }

    public int size() {
        return profiles.size();
    }
}
