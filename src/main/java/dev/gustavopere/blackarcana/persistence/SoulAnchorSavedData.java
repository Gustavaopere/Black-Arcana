package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.content.souls.SoulAnchorLedger;
import dev.gustavopere.blackarcana.content.souls.SoulSafetyCeilings;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.saveddata.SavedData;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Durable bounded storage for Mortal Ledger / Soul Anchor snapshots. */
public final class SoulAnchorSavedData extends SavedData {
    private static final String DATA_NAME = "black_arcana_soul_anchors";
    private static final int SCHEMA_VERSION = 1;
    public static final int MAX_PERSISTED_OWNERS = SoulSafetyCeilings.MAX_TRACKED_OWNERS;

    private List<SoulAnchorLedger.Snapshot> snapshots = List.of();

    public static SoulAnchorSavedData get(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        return server.overworld().getDataStorage().computeIfAbsent(
            new SavedData.Factory<>(SoulAnchorSavedData::new, SoulAnchorSavedData::load),
            DATA_NAME);
    }

    public static SoulAnchorSavedData load(CompoundTag root, HolderLookup.Provider registries) {
        SoulAnchorSavedData data = new SoulAnchorSavedData();
        if (root.getInt("schema") != SCHEMA_VERSION) return data;

        ListTag owners = root.getList("owners", Tag.TAG_COMPOUND);
        int count = Math.min(owners.size(), MAX_PERSISTED_OWNERS);
        ArrayList<SoulAnchorLedger.Snapshot> decoded = new ArrayList<>(count);
        Set<UUID> seenOwners = new HashSet<>();
        for (int i = 0; i < count; i++) {
            CompoundTag tag = owners.getCompound(i);
            try {
                UUID ownerId = UUID.fromString(tag.getString("owner"));
                if (!seenOwners.add(ownerId)) continue;

                ListTag recentTags = tag.getList("recent_deaths", Tag.TAG_STRING);
                int recentCount = Math.min(
                    recentTags.size(),
                    SoulSafetyCeilings.MAX_RECENT_DEATH_EVENTS_PER_OWNER);
                ArrayList<UUID> recentDeaths = new ArrayList<>(recentCount);
                for (int recentIndex = 0; recentIndex < recentCount; recentIndex++) {
                    recentDeaths.add(UUID.fromString(recentTags.getString(recentIndex)));
                }

                String lastPreventedRaw = tag.getString("last_prevented");
                UUID lastPrevented = lastPreventedRaw.isBlank()
                    ? null
                    : UUID.fromString(lastPreventedRaw);

                decoded.add(new SoulAnchorLedger.Snapshot(
                    ownerId,
                    tag.getDouble("stored_spirit"),
                    tag.getInt("anchors"),
                    tag.getLong("recovery_until"),
                    recentDeaths,
                    lastPrevented));
            } catch (RuntimeException ignored) {
                // One malformed owner record must not poison the remaining durable ledger.
            }
        }
        data.snapshots = List.copyOf(decoded);
        return data;
    }

    public synchronized List<SoulAnchorLedger.Snapshot> snapshots() {
        return snapshots;
    }

    public synchronized void replaceSnapshots(List<SoulAnchorLedger.Snapshot> replacement) {
        Objects.requireNonNull(replacement, "replacement");
        if (replacement.size() > MAX_PERSISTED_OWNERS) {
            throw new IllegalArgumentException("soul anchor persistence exceeds owner ceiling");
        }
        ArrayList<SoulAnchorLedger.Snapshot> validated = new ArrayList<>(replacement.size());
        Set<UUID> owners = new HashSet<>();
        for (SoulAnchorLedger.Snapshot snapshot : replacement) {
            Objects.requireNonNull(snapshot, "snapshot");
            if (!owners.add(snapshot.ownerId())) {
                throw new IllegalArgumentException("duplicate soul anchor persistence owner");
            }
            validated.add(snapshot);
        }
        List<SoulAnchorLedger.Snapshot> next = List.copyOf(validated);
        if (!snapshots.equals(next)) {
            snapshots = next;
            setDirty();
        }
    }

    @Override
    public synchronized CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        ListTag owners = new ListTag();
        for (SoulAnchorLedger.Snapshot snapshot : snapshots) {
            CompoundTag tag = new CompoundTag();
            tag.putString("owner", snapshot.ownerId().toString());
            tag.putDouble("stored_spirit", snapshot.storedSpiritValue());
            tag.putInt("anchors", snapshot.anchors());
            tag.putLong("recovery_until", snapshot.recoveryUntilTick());

            ListTag recentDeaths = new ListTag();
            for (UUID deathEventId : snapshot.recentDeathEventIds()) {
                recentDeaths.add(StringTag.valueOf(deathEventId.toString()));
            }
            tag.put("recent_deaths", recentDeaths);
            if (snapshot.lastPreventedDeathEvent() != null) {
                tag.putString("last_prevented", snapshot.lastPreventedDeathEvent().toString());
            }
            owners.add(tag);
        }
        root.put("owners", owners);
        return root;
    }
}
