package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastRequestValidator;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

public final class LoadoutRegistry implements CastRequestValidator {
    private final Map<UUID, List<ArcanaSpellId>> loadouts = new HashMap<>();

    public synchronized void setLoadout(UUID casterId, List<ArcanaSpellId> spells) {
        Objects.requireNonNull(casterId, "casterId");
        loadouts.put(casterId, validateLoadout(spells));
    }

    public synchronized List<ArcanaSpellId> getLoadout(UUID casterId) {
        return loadouts.getOrDefault(Objects.requireNonNull(casterId, "casterId"), List.of());
    }

    public synchronized Map<UUID, List<ArcanaSpellId>> snapshot() {
        Map<UUID, List<ArcanaSpellId>> snapshot = new HashMap<>();
        loadouts.forEach((caster, spells) -> snapshot.put(caster, List.copyOf(spells)));
        return Map.copyOf(snapshot);
    }

    public synchronized void restoreSnapshot(Map<UUID, List<ArcanaSpellId>> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        Map<UUID, List<ArcanaSpellId>> validated = new HashMap<>();
        snapshot.forEach((caster, spells) -> {
            Objects.requireNonNull(caster, "casterId");
            validated.put(caster, validateLoadout(spells));
        });
        loadouts.clear();
        loadouts.putAll(validated);
    }

    public synchronized void clear(UUID casterId) {
        loadouts.remove(Objects.requireNonNull(casterId, "casterId"));
    }

    @Override
    public synchronized ArcanaDecision check(ArcanaCastRequest request) {
        List<ArcanaSpellId> loadout = loadouts.get(request.context().casterId());
        if (loadout == null || request.loadoutSlot() >= loadout.size()) {
            return ArcanaDecision.deny("loadout_slot_unavailable", "requested loadout slot is not configured for caster");
        }
        ArcanaSpellId equipped = loadout.get(request.loadoutSlot());
        if (!equipped.equals(request.spell().id())) {
            return ArcanaDecision.deny("loadout_spell_mismatch", "requested spell does not match the server-owned loadout slot");
        }
        return ArcanaDecision.allow();
    }

    private static List<ArcanaSpellId> validateLoadout(List<ArcanaSpellId> spells) {
        Objects.requireNonNull(spells, "spells");
        if (spells.size() > ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadout exceeds maximum slot count");
        }
        List<ArcanaSpellId> candidate = List.copyOf(spells);
        if (candidate.stream().distinct().count() != candidate.size()) {
            throw new IllegalArgumentException("loadout contains duplicate spells");
        }
        return candidate;
    }
}
