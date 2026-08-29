package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.saveddata.SavedData;

/** Durable, independently dirty-tracked ledger for idempotent ritual outcomes. */
public final class RitualCompletionSavedData extends SavedData {
    private static final String DATA_NAME = "black_arcana_ritual_completions";
    private static final int SCHEMA_VERSION = 1;
    public static final int MAX_PERSISTED_COMPLETIONS = 16_384;

    private final RitualCompletionLedger ledger = new RitualCompletionLedger(MAX_PERSISTED_COMPLETIONS);

    public static RitualCompletionSavedData get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
            new SavedData.Factory<>(RitualCompletionSavedData::new, RitualCompletionSavedData::load),
            DATA_NAME);
    }

    public static RitualCompletionSavedData load(CompoundTag root, HolderLookup.Provider registries) {
        RitualCompletionSavedData data = new RitualCompletionSavedData();
        if (root.getInt("schema") != SCHEMA_VERSION) return data;

        ListTag entries = root.getList("completions", Tag.TAG_COMPOUND);
        int count = Math.min(entries.size(), MAX_PERSISTED_COMPLETIONS);
        java.util.ArrayList<RitualCompletionLedger.SnapshotEntry> snapshots = new java.util.ArrayList<>(count);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = entries.getCompound(i);
            try {
                RitualCompletionKey key = new RitualCompletionKey(
                    ArcanaRitualId.parse(tag.getString("ritual")),
                    RitualCompletionKey.Scope.valueOf(tag.getString("scope")),
                    tag.getString("subject"));
                snapshots.add(new RitualCompletionLedger.SnapshotEntry(key, tag.getLong("completed_at")));
            } catch (RuntimeException ignored) {
                // A malformed completion entry must not poison the rest of the save.
            }
        }
        data.ledger.restore(snapshots);
        return data;
    }

    public synchronized RitualCompletionLedger.CompletionResult complete(RitualCompletionKey key, long nowTick) {
        RitualCompletionLedger.CompletionResult result = ledger.complete(key, nowTick);
        if (result == RitualCompletionLedger.CompletionResult.RECORDED) setDirty();
        return result;
    }

    public synchronized boolean contains(RitualCompletionKey key) {
        return ledger.contains(key);
    }

    public synchronized int size() {
        return ledger.size();
    }

    @Override
    public synchronized CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        ListTag entries = new ListTag();
        for (RitualCompletionLedger.SnapshotEntry snapshot : ledger.snapshot(MAX_PERSISTED_COMPLETIONS)) {
            CompoundTag tag = new CompoundTag();
            tag.putString("ritual", snapshot.key().ritualId().canonical());
            tag.putString("scope", snapshot.key().scope().name());
            tag.putString("subject", snapshot.key().subjectId());
            tag.putLong("completed_at", snapshot.completedAtTick());
            entries.add(tag);
        }
        root.put("completions", entries);
        return root;
    }
}
