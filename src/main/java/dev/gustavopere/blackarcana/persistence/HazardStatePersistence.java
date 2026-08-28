package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

/** Narrow NBT codec for Stage 05A player hazard state. */
final class HazardStatePersistence {
    private HazardStatePersistence() { }

    static ListTag writeCorruption(Map<UUID, CorruptionStateService.PersistedState> entries, int maxEntries) {
        ListTag list = new ListTag();
        int written = 0;
        for (Map.Entry<UUID, CorruptionStateService.PersistedState> entry : entries.entrySet()) {
            if (written++ >= maxEntries) break;
            CompoundTag tag = new CompoundTag();
            tag.putUUID("player", entry.getKey());
            var state = entry.getValue();
            tag.putDouble("units", state.units());
            tag.putLong("updated", state.lastMeaningfulUpdateTick());
            tag.putLong("recovery", state.lastRecoveryTick());
            tag.putLong("acquisitions", state.acquisitionEvents());
            tag.putLong("recoveries", state.recoveryEvents());
            tag.putInt("state_schema", state.schemaVersion());
            list.add(tag);
        }
        return list;
    }

    static Map<UUID, CorruptionStateService.PersistedState> readCorruption(ListTag list, int maxEntries) {
        Map<UUID, CorruptionStateService.PersistedState> result = new LinkedHashMap<>();
        int count = Math.min(list.size(), maxEntries);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                if (tag.getInt("state_schema") != CorruptionStateService.STATE_SCHEMA_VERSION) continue;
                UUID playerId = tag.getUUID("player");
                var safe = CorruptionStateService.PersistedState.sanitize(
                    tag.getDouble("units"),
                    tag.getLong("updated"),
                    tag.getLong("recovery"),
                    tag.getLong("acquisitions"),
                    tag.getLong("recoveries"));
                result.put(playerId, safe);
            } catch (RuntimeException ignored) {
                // One malformed player record must not poison the entire global save.
            }
        }
        return Map.copyOf(result);
    }

    static ListTag writeStrain(Map<UUID, ArcaneStrainStateService.PersistedState> entries, int maxEntries) {
        ListTag list = new ListTag();
        int written = 0;
        for (Map.Entry<UUID, ArcaneStrainStateService.PersistedState> entry : entries.entrySet()) {
            if (written++ >= maxEntries) break;
            CompoundTag tag = new CompoundTag();
            tag.putUUID("player", entry.getKey());
            var state = entry.getValue();
            tag.putDouble("units", state.units());
            tag.putLong("updated", state.lastUpdateTick());
            tag.putLong("acquisitions", state.acquisitionEvents());
            tag.putLong("recoveries", state.recoveryEvents());
            tag.putInt("state_schema", state.schemaVersion());
            list.add(tag);
        }
        return list;
    }

    static Map<UUID, ArcaneStrainStateService.PersistedState> readStrain(ListTag list, int maxEntries) {
        Map<UUID, ArcaneStrainStateService.PersistedState> result = new LinkedHashMap<>();
        int count = Math.min(list.size(), maxEntries);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                if (tag.getInt("state_schema") != ArcaneStrainStateService.STATE_SCHEMA_VERSION) continue;
                UUID playerId = tag.getUUID("player");
                var safe = ArcaneStrainStateService.PersistedState.sanitize(
                    tag.getDouble("units"),
                    tag.getLong("updated"),
                    tag.getLong("acquisitions"),
                    tag.getLong("recoveries"));
                result.put(playerId, safe);
            } catch (RuntimeException ignored) {
                // Skip malformed entries and preserve all remaining hazard state.
            }
        }
        return Map.copyOf(result);
    }
}
