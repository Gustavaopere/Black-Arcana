package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Server-owned permanent knowledge. Loadout/equipped state remains a separate Stage 02 concern. */
public final class ArcanaKnowledgeLedger {
    public static final int ABSOLUTE_MAX_KNOWN_PER_CASTER = 512;
    public static final int ABSOLUTE_MAX_CASTERS = 16_384;

    public enum UnlockResult { UNLOCKED, ALREADY_KNOWN, CASTER_CAPACITY, KNOWLEDGE_CAPACITY }
    public record RestoreResult(int castersRestored, int spellsRestored, int migrated, int dropped) {
        public RestoreResult {
            if (castersRestored < 0 || spellsRestored < 0 || migrated < 0 || dropped < 0) throw new IllegalArgumentException("restore counts cannot be negative");
        }
    }

    private final int maxCasters;
    private final int maxKnownPerCaster;
    private final Map<UUID, LinkedHashSet<ArcanaSpellId>> known = new LinkedHashMap<>();

    public ArcanaKnowledgeLedger(int maxCasters, int maxKnownPerCaster) {
        if (maxCasters <= 0 || maxCasters > ABSOLUTE_MAX_CASTERS) throw new IllegalArgumentException("maxCasters outside safety ceiling");
        if (maxKnownPerCaster <= 0 || maxKnownPerCaster > ABSOLUTE_MAX_KNOWN_PER_CASTER) throw new IllegalArgumentException("maxKnownPerCaster outside safety ceiling");
        this.maxCasters = maxCasters;
        this.maxKnownPerCaster = maxKnownPerCaster;
    }

    public synchronized UnlockResult unlock(UUID casterId, ArcanaSpellId spellId) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(spellId, "spellId");
        LinkedHashSet<ArcanaSpellId> spells = known.get(casterId);
        if (spells != null && spells.contains(spellId)) return UnlockResult.ALREADY_KNOWN;
        if (spells == null) {
            if (known.size() >= maxCasters) return UnlockResult.CASTER_CAPACITY;
            spells = new LinkedHashSet<>();
            known.put(casterId, spells);
        }
        if (spells.size() >= maxKnownPerCaster) return UnlockResult.KNOWLEDGE_CAPACITY;
        spells.add(spellId);
        return UnlockResult.UNLOCKED;
    }

    public synchronized boolean revoke(UUID casterId, ArcanaSpellId spellId) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(spellId, "spellId");
        LinkedHashSet<ArcanaSpellId> spells = known.get(casterId);
        if (spells == null || !spells.remove(spellId)) return false;
        if (spells.isEmpty()) known.remove(casterId);
        return true;
    }

    public synchronized boolean knows(UUID casterId, ArcanaSpellId spellId) {
        LinkedHashSet<ArcanaSpellId> spells = known.get(Objects.requireNonNull(casterId, "casterId"));
        return spells != null && spells.contains(Objects.requireNonNull(spellId, "spellId"));
    }

    public synchronized Set<ArcanaSpellId> knownSpells(UUID casterId) {
        LinkedHashSet<ArcanaSpellId> spells = known.get(Objects.requireNonNull(casterId, "casterId"));
        return spells == null ? Set.of() : Set.copyOf(spells);
    }

    public synchronized Map<UUID, List<ArcanaSpellId>> snapshot() {
        Map<UUID, List<ArcanaSpellId>> result = new LinkedHashMap<>();
        known.forEach((caster, spells) -> result.put(caster, List.copyOf(spells)));
        return Map.copyOf(result);
    }

    public synchronized RestoreResult restore(
        Map<UUID, List<ArcanaSpellId>> snapshot,
        Set<ArcanaSpellId> activeDefinitions,
        KnowledgeMigrationTable migrations
    ) {
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(activeDefinitions, "activeDefinitions");
        Objects.requireNonNull(migrations, "migrations");
        known.clear();
        int restored = 0;
        int migrated = 0;
        int dropped = 0;
        int casters = 0;
        for (Map.Entry<UUID, List<ArcanaSpellId>> entry : snapshot.entrySet()) {
            UUID caster = entry.getKey();
            List<ArcanaSpellId> ids = entry.getValue();
            if (caster == null || ids == null) { dropped++; continue; }
            if (casters >= maxCasters) { dropped += ids.size(); continue; }
            LinkedHashSet<ArcanaSpellId> accepted = new LinkedHashSet<>();
            for (ArcanaSpellId id : ids) {
                if (id == null) { dropped++; continue; }
                var resolved = migrations.resolve(id);
                if (resolved.isEmpty()) { dropped++; continue; }
                ArcanaSpellId finalId = resolved.orElseThrow();
                if (!finalId.equals(id)) migrated++;
                if (!activeDefinitions.contains(finalId)) { dropped++; continue; }
                if (accepted.size() >= maxKnownPerCaster) { dropped++; continue; }
                if (accepted.add(finalId)) restored++;
            }
            if (!accepted.isEmpty()) { known.put(caster, accepted); casters++; }
        }
        return new RestoreResult(casters, restored, migrated, dropped);
    }
}
