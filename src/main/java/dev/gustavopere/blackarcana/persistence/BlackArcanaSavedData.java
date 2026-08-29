package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEmergencyProtectionStateService;
import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashDebt;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashRegistry;
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
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
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

    public static final int MAX_PERSISTED_COOLDOWNS = 131_072;
    public static final int MAX_PERSISTED_CHARGE_POOLS = 131_072;
    public static final int MAX_PERSISTED_LOADOUT_CASTERS = 16_384;
    public static final int MAX_PERSISTED_TEMPORARY_MUTATIONS = 16_384;
    public static final int MAX_PERSISTED_CORRUPTION_PLAYERS = 16_384;
    public static final int MAX_PERSISTED_STRAIN_PLAYERS = 16_384;
    public static final int MAX_PERSISTED_PENDING_BACKLASH_PLAYERS = 16_384;
    public static final int MAX_PERSISTED_PENDING_BACKLASH_DEBTS = 65_536;
    public static final int MAX_PERSISTED_EMERGENCY_RESOURCES = 65_536;

    private Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> cooldowns = Map.of();
    private Map<ChargePoolCooldownService.ChargeKey, ChargePoolCooldownService.SnapshotEntry> charges = Map.of();
    private Map<UUID, List<ArcanaSpellId>> loadouts = Map.of();
    private List<TemporaryWorldMutation> temporaryMutations = List.of();
    private Map<UUID, CorruptionStateService.PersistedState> corruptionStates = Map.of();
    private Map<UUID, ArcaneStrainStateService.PersistedState> strainStates = Map.of();
    private Map<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
        emergencyProtectionStates = Map.of();
    private final Map<UUID, List<PendingBacklashDebt>> pendingBacklashDebts = new LinkedHashMap<>();
    private int pendingBacklashDebtCount;

    public static BlackArcanaSavedData get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(BlackArcanaSavedData::new, BlackArcanaSavedData::load),
                DATA_NAME);
    }

    public static BlackArcanaSavedData load(CompoundTag root, HolderLookup.Provider registries) {
        BlackArcanaSavedData data = new BlackArcanaSavedData();
        int schema = root.getInt("schema");
        if (schema != SCHEMA_VERSION) return data;

        data.cooldowns = readCooldowns(root.getList("cooldowns", Tag.TAG_COMPOUND));
        data.charges = readCharges(root.getList("charges", Tag.TAG_COMPOUND));
        data.loadouts = readLoadouts(root.getList("loadouts", Tag.TAG_COMPOUND));
        data.temporaryMutations = readTemporaryMutations(root.getList("temporary_mutations", Tag.TAG_COMPOUND));
        data.corruptionStates = HazardStatePersistence.readCorruption(
            root.getList("corruption", Tag.TAG_COMPOUND), MAX_PERSISTED_CORRUPTION_PLAYERS);
        data.strainStates = HazardStatePersistence.readStrain(
            root.getList("strain", Tag.TAG_COMPOUND), MAX_PERSISTED_STRAIN_PLAYERS);
        data.emergencyProtectionStates = readEmergencyProtection(
            root.getList("emergency_protection", Tag.TAG_COMPOUND), MAX_PERSISTED_EMERGENCY_RESOURCES);

        Map<UUID, List<PendingBacklashDebt>> contextual = readPendingBacklashDebts(
            root.getList("pending_backlash_debts", Tag.TAG_COMPOUND),
            MAX_PERSISTED_PENDING_BACKLASH_PLAYERS,
            MAX_PERSISTED_PENDING_BACKLASH_DEBTS);
        data.pendingBacklashDebts.putAll(contextual);

        // Schema 1 originally stored only aggregate amounts. Keep those saves valid and, if a
        // structured entry is malformed, fail closed to the aggregate debt without inventing
        // emergency-protection context.
        Map<UUID, Double> legacy = readPendingBacklash(
            root.getList("pending_backlash", Tag.TAG_COMPOUND), MAX_PERSISTED_PENDING_BACKLASH_PLAYERS);
        for (Map.Entry<UUID, Double> entry : legacy.entrySet()) {
            if (data.pendingBacklashDebts.size() >= MAX_PERSISTED_PENDING_BACKLASH_PLAYERS) break;
            data.pendingBacklashDebts.putIfAbsent(entry.getKey(), List.of(PendingBacklashDebt.legacy(entry.getValue())));
        }
        data.pendingBacklashDebtCount = countPendingDebts(data.pendingBacklashDebts);
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

    public void captureHazards(CorruptionStateService corruption, ArcaneStrainStateService strain) {
        this.corruptionStates = Map.copyOf(corruption.persistentSnapshot());
        this.strainStates = Map.copyOf(strain.persistentSnapshot());
        setDirty();
    }

    public void captureHazards(
        CorruptionStateService corruption,
        ArcaneStrainStateService strain,
        ArcaneEmergencyProtectionStateService emergencyProtection
    ) {
        Objects.requireNonNull(emergencyProtection, "emergencyProtection");
        captureHazards(corruption, strain);
        this.emergencyProtectionStates = boundedEmergencySnapshot(emergencyProtection.persistentSnapshot());
        setDirty();
    }

    public void capturePendingBacklash(PendingBacklashRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        replacePendingBacklashDebts(registry.persistentDebtsSnapshot());
        setDirty();
    }

    /** Backward-compatible incremental update. Amount-only callers create legacy/unprotected debt. */
    public boolean updatePendingBacklash(UUID playerId, double amount) {
        Objects.requireNonNull(playerId, "playerId");
        if (!Double.isFinite(amount) || amount < 0.0D) {
            throw new IllegalArgumentException("pending backlash must be finite and non-negative");
        }
        if (amount == 0.0D) return updatePendingBacklash(playerId, List.of());
        double bounded = Math.min(amount, PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER);
        boolean fullyStored = updatePendingBacklash(playerId, List.of(PendingBacklashDebt.legacy(bounded)));
        return fullyStored && amount <= PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER;
    }

    /** Incremental contextual update used by the live damage pipeline. */
    public boolean updatePendingBacklash(UUID playerId, List<PendingBacklashDebt> debts) {
        Objects.requireNonNull(playerId, "playerId");
        Objects.requireNonNull(debts, "debts");
        List<PendingBacklashDebt> previous = pendingBacklashDebts.remove(playerId);
        if (previous != null) pendingBacklashDebtCount -= previous.size();
        if (debts.isEmpty()) {
            if (previous != null) setDirty();
            return true;
        }
        if (!pendingBacklashDebts.containsKey(playerId)
            && pendingBacklashDebts.size() >= MAX_PERSISTED_PENDING_BACKLASH_PLAYERS) {
            if (previous != null) {
                pendingBacklashDebts.put(playerId, previous);
                pendingBacklashDebtCount += previous.size();
            }
            return false;
        }

        int availableGlobal = MAX_PERSISTED_PENDING_BACKLASH_DEBTS - pendingBacklashDebtCount;
        int limit = Math.min(
            Math.min(debts.size(), PendingBacklashRegistry.ABSOLUTE_MAX_DEBTS_PER_PLAYER),
            Math.max(0, availableGlobal));
        List<PendingBacklashDebt> bounded = new ArrayList<>(limit);
        double total = 0.0D;
        boolean fullyStored = debts.size() <= limit;
        for (int i = 0; i < limit; i++) {
            PendingBacklashDebt debt = Objects.requireNonNull(debts.get(i), "debt");
            double remaining = PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER - total;
            if (remaining <= 0.0D) {
                fullyStored = false;
                break;
            }
            double amount = Math.min(debt.amount(), remaining);
            bounded.add(amount == debt.amount() ? debt : debt.withAmount(amount));
            total += amount;
            if (amount < debt.amount()) fullyStored = false;
        }
        if (bounded.isEmpty()) {
            if (previous != null) {
                pendingBacklashDebts.put(playerId, previous);
                pendingBacklashDebtCount += previous.size();
            }
            return false;
        }
        pendingBacklashDebts.put(playerId, List.copyOf(bounded));
        pendingBacklashDebtCount += bounded.size();
        setDirty();
        return fullyStored;
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

    public void restoreHazards(CorruptionStateService corruption, ArcaneStrainStateService strain) {
        corruption.restoreSnapshot(corruptionStates);
        strain.restoreSnapshot(strainStates);
    }

    public void restoreHazards(
        CorruptionStateService corruption,
        ArcaneStrainStateService strain,
        ArcaneEmergencyProtectionStateService emergencyProtection
    ) {
        Objects.requireNonNull(emergencyProtection, "emergencyProtection");
        restoreHazards(corruption, strain);
        emergencyProtection.restoreSnapshot(emergencyProtectionStates);
    }

    public void restorePendingBacklash(PendingBacklashRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        registry.restoreDebtsSnapshot(copyPendingBacklashDebts(pendingBacklashDebts));
    }

    @Override
    public CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        root.put("cooldowns", writeCooldowns(cooldowns));
        root.put("charges", writeCharges(charges));
        root.put("loadouts", writeLoadouts(loadouts));
        root.put("temporary_mutations", writeTemporaryMutations(temporaryMutations));
        root.put("corruption", HazardStatePersistence.writeCorruption(corruptionStates, MAX_PERSISTED_CORRUPTION_PLAYERS));
        root.put("strain", HazardStatePersistence.writeStrain(strainStates, MAX_PERSISTED_STRAIN_PLAYERS));
        root.put("emergency_protection", writeEmergencyProtection(emergencyProtectionStates));
        root.put("pending_backlash_debts", writePendingBacklashDebts(pendingBacklashDebts));
        // Keep the aggregate field as a fail-closed fallback for schema-1 saves/readers.
        root.put("pending_backlash", writePendingBacklash(aggregatePendingBacklash(pendingBacklashDebts)));
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
            } catch (RuntimeException ignored) { }
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
            } catch (RuntimeException ignored) { }
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
                for (int j = 0; j < spellList.size(); j++) spells.add(ArcanaSpellId.parse(spellList.getString(j)));
                result.put(caster, List.copyOf(spells));
            } catch (RuntimeException ignored) { }
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
            } catch (RuntimeException ignored) { }
        }
        return List.copyOf(result);
    }

    private static Map<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
    boundedEmergencySnapshot(
        Map<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState> source
    ) {
        Objects.requireNonNull(source, "source");
        LinkedHashMap<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
            result = new LinkedHashMap<>();
        for (Map.Entry<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
            entry : source.entrySet()) {
            if (result.size() >= MAX_PERSISTED_EMERGENCY_RESOURCES) break;
            if (entry.getKey() == null || entry.getValue() == null || entry.getValue().readyAtTick() <= 0L) continue;
            result.put(entry.getKey(), entry.getValue());
        }
        return Map.copyOf(result);
    }

    private static ListTag writeEmergencyProtection(
        Map<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState> entries
    ) {
        ListTag list = new ListTag();
        int written = 0;
        for (Map.Entry<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
            entry : entries.entrySet()) {
            if (written >= MAX_PERSISTED_EMERGENCY_RESOURCES) break;
            if (entry.getKey() == null || entry.getValue() == null || entry.getValue().readyAtTick() <= 0L) continue;
            CompoundTag tag = new CompoundTag();
            tag.putUUID("player", entry.getKey().playerId());
            tag.putString("resource", entry.getKey().resourceId());
            tag.putLong("ready", entry.getValue().readyAtTick());
            list.add(tag);
            written++;
        }
        return list;
    }

    private static Map<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
    readEmergencyProtection(ListTag list, int maxEntries) {
        LinkedHashMap<ArcaneEmergencyProtectionStateService.ResourceKey, ArcaneEmergencyProtectionStateService.PersistedState>
            result = new LinkedHashMap<>();
        int count = Math.min(list.size(), maxEntries);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                long readyAtTick = tag.getLong("ready");
                if (readyAtTick <= 0L) continue;
                var key = new ArcaneEmergencyProtectionStateService.ResourceKey(
                    tag.getUUID("player"), tag.getString("resource"));
                result.putIfAbsent(key, new ArcaneEmergencyProtectionStateService.PersistedState(readyAtTick));
            } catch (RuntimeException ignored) { }
        }
        return Map.copyOf(result);
    }

    private void replacePendingBacklashDebts(Map<UUID, List<PendingBacklashDebt>> source) {
        pendingBacklashDebts.clear();
        pendingBacklashDebtCount = 0;
        int players = 0;
        for (Map.Entry<UUID, List<PendingBacklashDebt>> entry : source.entrySet()) {
            if (players >= MAX_PERSISTED_PENDING_BACKLASH_PLAYERS
                || pendingBacklashDebtCount >= MAX_PERSISTED_PENDING_BACKLASH_DEBTS) break;
            UUID playerId = entry.getKey();
            List<PendingBacklashDebt> debts = entry.getValue();
            if (playerId == null || debts == null || debts.isEmpty()) continue;
            int available = MAX_PERSISTED_PENDING_BACKLASH_DEBTS - pendingBacklashDebtCount;
            int limit = Math.min(
                Math.min(debts.size(), PendingBacklashRegistry.ABSOLUTE_MAX_DEBTS_PER_PLAYER),
                available);
            List<PendingBacklashDebt> copied = new ArrayList<>(limit);
            double total = 0.0D;
            for (int i = 0; i < limit; i++) {
                PendingBacklashDebt debt = debts.get(i);
                if (debt == null) continue;
                double remaining = PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER - total;
                if (remaining <= 0.0D) break;
                double amount = Math.min(debt.amount(), remaining);
                copied.add(amount == debt.amount() ? debt : debt.withAmount(amount));
                total += amount;
            }
            if (copied.isEmpty()) continue;
            pendingBacklashDebts.put(playerId, List.copyOf(copied));
            pendingBacklashDebtCount += copied.size();
            players++;
        }
    }

    private static Map<UUID, List<PendingBacklashDebt>> copyPendingBacklashDebts(
        Map<UUID, List<PendingBacklashDebt>> source
    ) {
        LinkedHashMap<UUID, List<PendingBacklashDebt>> copy = new LinkedHashMap<>();
        source.forEach((playerId, debts) -> copy.put(playerId, List.copyOf(debts)));
        return Map.copyOf(copy);
    }

    private static int countPendingDebts(Map<UUID, List<PendingBacklashDebt>> source) {
        int count = 0;
        for (List<PendingBacklashDebt> debts : source.values()) {
            if (debts == null) continue;
            if (count >= MAX_PERSISTED_PENDING_BACKLASH_DEBTS - debts.size()) {
                return MAX_PERSISTED_PENDING_BACKLASH_DEBTS;
            }
            count += debts.size();
        }
        return count;
    }

    private static ListTag writePendingBacklashDebts(Map<UUID, List<PendingBacklashDebt>> entries) {
        ListTag list = new ListTag();
        int written = 0;
        for (Map.Entry<UUID, List<PendingBacklashDebt>> entry : entries.entrySet()) {
            if (written >= MAX_PERSISTED_PENDING_BACKLASH_DEBTS) break;
            UUID playerId = entry.getKey();
            if (playerId == null || entry.getValue() == null) continue;
            int perPlayer = 0;
            for (PendingBacklashDebt debt : entry.getValue()) {
                if (written >= MAX_PERSISTED_PENDING_BACKLASH_DEBTS
                    || perPlayer >= PendingBacklashRegistry.ABSOLUTE_MAX_DEBTS_PER_PLAYER) break;
                if (debt == null) continue;
                CompoundTag tag = new CompoundTag();
                tag.putUUID("player", playerId);
                tag.putDouble("amount", debt.amount());
                if (debt.damageInstanceId().isPresent()) {
                    tag.putBoolean("contextual", true);
                    tag.putUUID("damage", debt.damageInstanceId().orElseThrow().value());
                    tag.putBoolean("protection_allowed", debt.protectionAllowed());
                    tag.put("emergency_candidates", writeEmergencyCandidates(debt.emergencyProtectionSnapshot()));
                }
                list.add(tag);
                written++;
                perPlayer++;
            }
        }
        return list;
    }

    private static Map<UUID, List<PendingBacklashDebt>> readPendingBacklashDebts(
        ListTag list,
        int maxPlayers,
        int maxDebts
    ) {
        LinkedHashMap<UUID, List<PendingBacklashDebt>> mutable = new LinkedHashMap<>();
        int count = Math.min(list.size(), maxDebts);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                UUID playerId = tag.getUUID("player");
                double rawAmount = tag.getDouble("amount");
                if (!Double.isFinite(rawAmount) || rawAmount <= 0.0D) continue;
                if (!mutable.containsKey(playerId) && mutable.size() >= maxPlayers) continue;
                List<PendingBacklashDebt> debts = mutable.computeIfAbsent(playerId, ignored -> new ArrayList<>());
                if (debts.size() >= PendingBacklashRegistry.ABSOLUTE_MAX_DEBTS_PER_PLAYER) continue;
                double currentTotal = 0.0D;
                for (PendingBacklashDebt debt : debts) currentTotal += debt.amount();
                double remaining = PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER - currentTotal;
                if (remaining <= 0.0D) continue;
                double amount = Math.min(rawAmount, remaining);

                PendingBacklashDebt debt;
                if (tag.getBoolean("contextual")) {
                    try {
                        ArcanaDamageInstanceId damageInstanceId = new ArcanaDamageInstanceId(tag.getUUID("damage"));
                        ArcaneEmergencyProtectionSnapshot emergency = readEmergencyCandidates(
                            tag.getList("emergency_candidates", Tag.TAG_COMPOUND));
                        debt = PendingBacklashDebt.contextual(
                            amount,
                            damageInstanceId,
                            tag.getBoolean("protection_allowed"),
                            emergency);
                    } catch (RuntimeException malformedContext) {
                        debt = PendingBacklashDebt.legacy(amount);
                    }
                } else {
                    debt = PendingBacklashDebt.legacy(amount);
                }
                debts.add(debt);
            } catch (RuntimeException ignored) { }
        }

        LinkedHashMap<UUID, List<PendingBacklashDebt>> result = new LinkedHashMap<>();
        mutable.forEach((playerId, debts) -> {
            if (!debts.isEmpty()) result.put(playerId, List.copyOf(debts));
        });
        return Map.copyOf(result);
    }

    private static ListTag writeEmergencyCandidates(ArcaneEmergencyProtectionSnapshot snapshot) {
        ListTag list = new ListTag();
        int count = Math.min(snapshot.candidates().size(), ArcaneEmergencyProtectionSnapshot.MAX_CANDIDATES);
        for (int i = 0; i < count; i++) {
            ArcaneEmergencyProtectionSnapshot.Candidate candidate = snapshot.candidates().get(i);
            CompoundTag tag = new CompoundTag();
            tag.putString("source", candidate.sourceId());
            tag.putString("resource", candidate.resourceId());
            tag.putDouble("absorption", candidate.absorption());
            tag.putLong("cooldown", candidate.cooldownTicks());
            list.add(tag);
        }
        return list;
    }

    private static ArcaneEmergencyProtectionSnapshot readEmergencyCandidates(ListTag list) {
        List<ArcaneEmergencyProtectionSnapshot.Candidate> candidates = new ArrayList<>();
        Set<String> resources = new HashSet<>();
        int count = Math.min(list.size(), ArcaneEmergencyProtectionSnapshot.MAX_CANDIDATES);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                ArcaneEmergencyProtectionSnapshot.Candidate candidate =
                    new ArcaneEmergencyProtectionSnapshot.Candidate(
                        tag.getString("source"),
                        tag.getString("resource"),
                        tag.getDouble("absorption"),
                        tag.getLong("cooldown"));
                if (resources.add(candidate.resourceId())) candidates.add(candidate);
            } catch (RuntimeException ignored) { }
        }
        return new ArcaneEmergencyProtectionSnapshot(candidates);
    }

    private static Map<UUID, Double> aggregatePendingBacklash(
        Map<UUID, List<PendingBacklashDebt>> entries
    ) {
        LinkedHashMap<UUID, Double> aggregate = new LinkedHashMap<>();
        int players = 0;
        for (Map.Entry<UUID, List<PendingBacklashDebt>> entry : entries.entrySet()) {
            if (players >= MAX_PERSISTED_PENDING_BACKLASH_PLAYERS) break;
            if (entry.getKey() == null || entry.getValue() == null) continue;
            double total = 0.0D;
            for (PendingBacklashDebt debt : entry.getValue()) {
                if (debt == null) continue;
                total = Math.min(
                    PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER,
                    total + debt.amount());
            }
            if (total <= 0.0D) continue;
            aggregate.put(entry.getKey(), total);
            players++;
        }
        return Map.copyOf(aggregate);
    }

    private static ListTag writePendingBacklash(Map<UUID, Double> entries) {
        ListTag list = new ListTag();
        int written = 0;
        for (Map.Entry<UUID, Double> entry : entries.entrySet()) {
            if (written >= MAX_PERSISTED_PENDING_BACKLASH_PLAYERS) break;
            Double amount = entry.getValue();
            if (entry.getKey() == null || amount == null || !Double.isFinite(amount) || amount <= 0.0D) continue;
            CompoundTag tag = new CompoundTag();
            tag.putUUID("player", entry.getKey());
            tag.putDouble("amount", Math.min(amount, PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER));
            list.add(tag);
            written++;
        }
        return list;
    }

    private static Map<UUID, Double> readPendingBacklash(ListTag list, int maxPlayers) {
        Map<UUID, Double> result = new LinkedHashMap<>();
        int count = Math.min(list.size(), maxPlayers);
        for (int i = 0; i < count; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                UUID player = tag.getUUID("player");
                double amount = tag.getDouble("amount");
                if (!Double.isFinite(amount) || amount <= 0.0D) continue;
                result.put(player, Math.min(amount, PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER));
            } catch (RuntimeException ignored) { }
        }
        return Map.copyOf(result);
    }
}
