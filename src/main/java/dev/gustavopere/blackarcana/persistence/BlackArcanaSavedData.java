package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualActivationId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualDefinition;
import dev.gustavopere.blackarcana.core.ritual.RitualEngine;
import dev.gustavopere.blackarcana.core.ritual.RitualRestoreResult;
import dev.gustavopere.blackarcana.core.ritual.RitualSessionSnapshot;
import dev.gustavopere.blackarcana.core.ritual.RitualSessionState;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationTracker;
import dev.gustavopere.blackarcana.core.world.TemporaryWorldMutation;
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
 * global/runtime recovery state rather than scoped to one loaded dimension.
 */
public final class BlackArcanaSavedData extends SavedData {
    private static final String DATA_NAME = "black_arcana_runtime";
    private static final int SCHEMA_VERSION = 1;

    // Defensive restore ceilings. Normal runtime state should stay far below these values.
    public static final int MAX_PERSISTED_COOLDOWNS = 131_072;
    public static final int MAX_PERSISTED_CHARGE_POOLS = 131_072;
    public static final int MAX_PERSISTED_LOADOUT_CASTERS = 16_384;
    public static final int MAX_PERSISTED_TEMPORARY_MUTATIONS = 16_384;
    public static final int MAX_PERSISTED_RITUAL_SESSIONS = 4_096;

    private Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> cooldowns = Map.of();
    private Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> charges = Map.of();
    private Map<UUID, List<ArcanaSpellId>> loadouts = Map.of();
    private List<TemporaryWorldMutation> temporaryMutations = List.of();
    private List<RitualSessionSnapshot> ritualSessions = List.of();

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
        data.temporaryMutations = readTemporaryMutations(root.getList("temporary_mutations", Tag.TAG_COMPOUND));
        data.ritualSessions = readRitualSessions(root.getList("ritual_sessions", Tag.TAG_COMPOUND));
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

    public void capture(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            TemporaryMutationTracker temporaryMutationTracker,
            long now
    ) {
        capture(cooldownService, chargeService, loadoutRegistry, now);
        this.temporaryMutations = temporaryMutationTracker.snapshot();
        setDirty();
    }

    public void capture(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            TemporaryMutationTracker temporaryMutationTracker,
            RitualEngine ritualEngine,
            long now
    ) {
        capture(cooldownService, chargeService, loadoutRegistry, temporaryMutationTracker, now);
        this.ritualSessions = ritualEngine.snapshot(MAX_PERSISTED_RITUAL_SESSIONS);
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

    public void restore(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            TemporaryMutationTracker temporaryMutationTracker,
            long now
    ) {
        restore(cooldownService, chargeService, loadoutRegistry, now);
        temporaryMutationTracker.restoreSnapshot(temporaryMutations);
    }

    public RitualRestoreResult restore(
            PersistentCooldownService cooldownService,
            ChargePoolCooldownService chargeService,
            LoadoutRegistry loadoutRegistry,
            TemporaryMutationTracker temporaryMutationTracker,
            RitualEngine ritualEngine,
            List<RitualDefinition> definitions,
            long now
    ) {
        restore(cooldownService, chargeService, loadoutRegistry, temporaryMutationTracker, now);
        return ritualEngine.restore(definitions, ritualSessions, now);
    }

    @Override
    public CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        root.put("cooldowns", writeCooldowns(cooldowns));
        root.put("charges", writeCharges(charges));
        root.put("loadouts", writeLoadouts(loadouts));
        root.put("temporary_mutations", writeTemporaryMutations(temporaryMutations));
        root.put("ritual_sessions", writeRitualSessions(ritualSessions));
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
        int count = Math.min(list.size(), MAX_PERSISTED_COOLDOWNS);
        for (int i = 0; i < count; i++) {
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
        int count = Math.min(list.size(), MAX_PERSISTED_CHARGE_POOLS);
        for (int i = 0; i < count; i++) {
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
        int count = Math.min(list.size(), MAX_PERSISTED_LOADOUT_CASTERS);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                UUID caster = tag.getUUID("caster");
                ListTag spellList = tag.getList("spells", Tag.TAG_STRING);
                if (spellList.size() > ArcanaCastRequest.MAX_LOADOUT_SLOTS) continue;

                List<ArcanaSpellId> spells = new ArrayList<>(spellList.size());
                for (int j = 0; j < spellList.size(); j++) {
                    spells.add(ArcanaSpellId.parse(spellList.getString(j)));
                }
                result.put(caster, List.copyOf(spells));
            } catch (RuntimeException ignored) {
                // A broken player's loadout must not make the entire saved data unreadable.
            }
        }
        return Map.copyOf(result);
    }

    private static ListTag writeTemporaryMutations(List<TemporaryWorldMutation> entries) {
        ListTag list = new ListTag();
        int count = Math.min(entries.size(), MAX_PERSISTED_TEMPORARY_MUTATIONS);
        for (int i = 0; i < count; i++) {
            TemporaryWorldMutation mutation = entries.get(i);
            CompoundTag tag = new CompoundTag();
            tag.putString("dimension", mutation.key().dimensionId());
            tag.putLong("pos", mutation.key().packedBlockPos());
            tag.putUUID("owner", mutation.ownerId());
            tag.putUUID("cast", mutation.castId().value());
            tag.putString("original", mutation.originalState());
            tag.putString("replacement", mutation.replacementState());
            tag.putLong("expires", mutation.expiresAtTick());
            list.add(tag);
        }
        return list;
    }

    private static List<TemporaryWorldMutation> readTemporaryMutations(ListTag list) {
        List<TemporaryWorldMutation> result = new ArrayList<>();
        int count = Math.min(list.size(), MAX_PERSISTED_TEMPORARY_MUTATIONS);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                result.add(new TemporaryWorldMutation(
                    new TemporaryMutationKey(tag.getString("dimension"), tag.getLong("pos")),
                    tag.getUUID("owner"),
                    new ArcanaCastId(tag.getUUID("cast")),
                    tag.getString("original"),
                    tag.getString("replacement"),
                    tag.getLong("expires")));
            } catch (RuntimeException ignored) {
                // Skip malformed restoration records; never poison otherwise valid world state.
            }
        }
        return List.copyOf(result);
    }

    private static ListTag writeRitualSessions(List<RitualSessionSnapshot> entries) {
        ListTag list = new ListTag();
        int count = Math.min(entries.size(), MAX_PERSISTED_RITUAL_SESSIONS);
        for (int i = 0; i < count; i++) {
            RitualSessionSnapshot snapshot = entries.get(i);
            CompoundTag tag = new CompoundTag();
            tag.putString("ritual", snapshot.ritualId().canonical());
            tag.putUUID("activation", snapshot.activationId().value());
            tag.putUUID("caster", snapshot.context().casterId());
            ListTag participants = new ListTag();
            snapshot.context().participantIds().forEach(id -> participants.add(StringTag.valueOf(id.toString())));
            tag.put("participants", participants);
            tag.putString("dimension", snapshot.context().anchor().dimensionId());
            tag.putLong("anchor", snapshot.context().anchor().packedBlockPos());
            tag.putLong("started", snapshot.startedAtTick());
            tag.putLong("commit", snapshot.commitAtTick());
            tag.putLong("complete", snapshot.completeAtTick());
            tag.putString("state", snapshot.state().name());
            list.add(tag);
        }
        return list;
    }

    private static List<RitualSessionSnapshot> readRitualSessions(ListTag list) {
        List<RitualSessionSnapshot> result = new ArrayList<>();
        int count = Math.min(list.size(), MAX_PERSISTED_RITUAL_SESSIONS);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                ListTag participantTags = tag.getList("participants", Tag.TAG_STRING);
                if (participantTags.size() > RitualContext.MAX_PARTICIPANTS) continue;
                List<UUID> participants = new ArrayList<>(participantTags.size());
                for (int j = 0; j < participantTags.size(); j++) {
                    participants.add(UUID.fromString(participantTags.getString(j)));
                }
                RitualContext context = new RitualContext(
                        tag.getUUID("caster"),
                        participants,
                        new RitualAnchor(tag.getString("dimension"), tag.getLong("anchor")));
                result.add(new RitualSessionSnapshot(
                        ArcanaRitualId.parse(tag.getString("ritual")),
                        new RitualActivationId(tag.getUUID("activation")),
                        context,
                        tag.getLong("started"),
                        tag.getLong("commit"),
                        tag.getLong("complete"),
                        RitualSessionState.valueOf(tag.getString("state"))));
            } catch (RuntimeException ignored) {
                // Skip malformed ritual sessions and preserve all valid runtime state.
            }
        }
        return List.copyOf(result);
    }
}
