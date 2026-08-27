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
        Objects.requireNonNull(spells, "spells");
        if (spells.size() > ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadout exceeds maximum slot count");
        }
        loadouts.put(casterId, List.copyOf(spells));
    }

    public synchronized List<ArcanaSpellId> getLoadout(UUID casterId) {
        return loadouts.getOrDefault(Objects.requireNonNull(casterId, "casterId"), List.of());
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
}
