package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.saveddata.SavedData;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Minecraft persistence adapter for Black Arcana's server-owned runtime state.
 *
 * The data is intentionally stored in the Overworld because these records are
 * global to a player/caster rather than scoped to one dimension.
 */
public final class BlackArcanaSavedData extends SavedData {
    private static final String DATA_NAME = "black_arcana_runtime";
    private static final int SCHEMA_VERSION = 1;

    private Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> cooldowns = Map.of();
    private Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> charges = Map.of();
    private Map<UUID, List<ArcanaSpellId>> loadouts = Map.of();

    public static BlackArcanaSavedData get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(BlackArcanaSavedData::new, BlackArcanaSavedData::load),
                DATA_NAME);
    }

    public static BlackArcanaSavedData load(CompoundTag root, HolderLookup.Provider registries) {
        BlackArcanaSavedData data = new BlackArcanaSavedData();
        int schema = root.getInt("schema");
        if (schema != SCHEMA_VERSION) {
            return data;
        }

        data.cooldowns = readCooldowns(root.getList("cooldowns", Tag.TAG_COMPOUND));
        data.charges = readCharges(root.getList("charges", Tag.TAG_COMPOUND));
        data.loadouts = readLoadouts(root.getList("loadouts", Tag.TAG_COMPOUND));
        return data;
    }

    public void capture(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            long now
    ) {
        this.cooldowns = cooldownService.persistentSnapshot(now);
        this.charges = chargeService.persistentSnapshot();
        this.loadouts = loadoutRegistry.snapshot();
        setDirty();
    }

    public void restore(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            long now
    ) {
        cooldownService.restorePersistentSnapshot(cooldowns, now);
        chargeService.restorePersistentSnapshot(charges);
        loadoutRegistry.restoreSnapshot(loadouts);
    }

    @Override
    public CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        root.put("cooldowns", writeCooldowns(cooldowns));
        root.put("charges", writeCharges(charges));
        root.put("loadouts", writeLoadouts(loadouts));
        return root;
    }

    private static ListTag writeCooldowns(Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> entries) {
        ListTag list = new ListTag();
        entries.forEach((key, value) -> {
            CompoundTag tag = new CompoundTag();
            tag.putUUID("caster", key.casterId());
            tag.putString("group", key.groupId());
            tag.putLong("started", value.startedAtTick());
            tag.putLong("ready", value.readyAtTick());
            list.add(tag);
        });
        return list;
    }

    private static Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> readCooldowns(ListTag list) {
        Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> result = new HashMap<>();
        for (int i = 0; i < list.size(); i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                var key = new PersistentCooldownService.CooldownKey(tag.getUUID("caster"), tag.getString("group"));
                var value = new PersistentCooldownService.SnapshotEntry(tag.getLong("started"), tag.getLong("ready"));
                result.put(key, value);
            } catch (RuntimeException ignored) {
                // Malformed individual entries are skipped rather than poisoning the entire world save.
            }
        }
        return Map.copyOf(result);
    }

    private static ListTag writeCharges(Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> entries) {
        ListTag list = new ListTag();
        entries.forEach((key, value) -> {
            CompoundTag tag = new CompoundTag();
            tag.putUUID("caster", key.casterId());
            tag.putString("group", key.groupId());
            tag.putInt("charges", value.charges());
            tag.putLong("next", value.nextRechargeAt());
            list.add(tag);
        });
        return list;
    }

    private static Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> readCharges(ListTag list) {
        Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> result = new HashMap<>();
        for (int i = 0; i < list.size(); i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                var key = new ChargePoolCooldownService.ChargeKey(tag.getUUID("caster"), tag.getString("group"));
                var value = new ChargePoolCooldownService.SnapshotEntry(tag.getInt("charges"), tag.getLong("next"));
                result.put(key, value);
            } catch (RuntimeException ignored) {
                // Skip malformed entries and retain all valid runtime state.
            }
        }
        return Map.copyOf(result);
    }

    private static ListTag writeLoadouts(Map<UUID, List<ArcanaSpellId>> entries) {
        ListTag list = new ListTag();
        entries.forEach((caster, spells) -> {
            CompoundTag tag = new CompoundTag();
            tag.putUUID("caster", caster);
            ListTag spellList = new ListTag();
            spells.forEach(spell -> spellList.add(StringTag.valueOf(spell.canonical())));
            tag.put("spells", spellList);
            list.add(tag);
        });
        return list;
    }

    private static Map<UUID, List<ArcanaSpellId>> readLoadouts(ListTag list) {
        Map<UUID, List<ArcanaSpellId>> result = new HashMap<>();
        for (int i = 0; i < list.size(); i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                UUID caster = tag.getUUID("caster");
                ListTag spellList = tag.getList("spells", Tag.TAG_STRING);
                List<ArcanaSpellId> spells = new ArrayList<>();
                for (int j = 0; j < spellList.size(); j++) {
                    spells.add(ArcanaSpellId.parse(spellList.getString(j)));
                }
                if (spells.size() <= dev.gustavopere.blackarcana.api.ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
                    result.put(caster, List.copyOf(spells));
                }
            } catch (RuntimeException ignored) {
                // A broken player's loadout must not make the entire saved data unreadable.
            }
        }
        return Map.copyOf(result);
    }
}
