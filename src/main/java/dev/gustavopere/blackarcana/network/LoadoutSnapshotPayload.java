package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/** Server-confirmed loadout state consumed by client presentation/input only. */
public record LoadoutSnapshotPayload(int protocolVersion, List<String> spellIds) {
    public LoadoutSnapshotPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(spellIds, "spellIds");
        spellIds = List.copyOf(spellIds);
        if (spellIds.size() > ArcanaProtocol.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadout exceeds protocol slot bound");
        }
        Set<String> unique = new HashSet<>(spellIds.size());
        for (String spellId : spellIds) {
            Objects.requireNonNull(spellId, "spellId");
            if (spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("spellId exceeds protocol bound");
            }
            ArcanaSpellId.parse(spellId);
            if (!unique.add(spellId)) {
                throw new IllegalArgumentException("duplicate loadout spell id: " + spellId);
            }
        }
    }

    public List<ArcanaSpellId> parsedSpellIds() {
        return spellIds.stream().map(ArcanaSpellId::parse).toList();
    }
}
