package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.progression.ArcanaKnowledgeLedger;
import dev.gustavopere.blackarcana.core.progression.KnowledgeMigrationTable;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.saveddata.SavedData;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Versioned global persistence for permanent Black Arcana knowledge.
 * Kept separate from volatile runtime recovery state so spell-id migrations can
 * evolve without coupling to cooldown/ritual persistence.
 */
public final class BlackArcanaKnowledgeSavedData extends SavedData {
    private static final String DATA_NAME = "black_arcana_knowledge";
    private static final int SCHEMA_VERSION = 1;
    public static final int MAX_PERSISTED_CASTERS = ArcanaKnowledgeLedger.ABSOLUTE_MAX_CASTERS;
    public static final int MAX_PERSISTED_SPELLS_PER_CASTER = ArcanaKnowledgeLedger.ABSOLUTE_MAX_KNOWN_PER_CASTER;

    private Map<UUID, List<ArcanaSpellId>> knowledge = Map.of();

    public static BlackArcanaKnowledgeSavedData get(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        return server.overworld().getDataStorage().computeIfAbsent(
            new SavedData.Factory<>(BlackArcanaKnowledgeSavedData::new, BlackArcanaKnowledgeSavedData::load),
            DATA_NAME);
    }

    public static BlackArcanaKnowledgeSavedData load(CompoundTag root, HolderLookup.Provider registries) {
        BlackArcanaKnowledgeSavedData data = new BlackArcanaKnowledgeSavedData();
        if (root.getInt("schema") != SCHEMA_VERSION) return data;
        data.knowledge = readKnowledge(root.getList("knowledge", Tag.TAG_COMPOUND));
        return data;
    }

    public void capture(ArcanaKnowledgeLedger ledger) {
        knowledge = Objects.requireNonNull(ledger, "ledger").snapshot();
        setDirty();
    }

    public ArcanaKnowledgeLedger.RestoreResult restore(
        ArcanaKnowledgeLedger ledger,
        Set<ArcanaSpellId> activeDefinitions,
        KnowledgeMigrationTable migrations
    ) {
        return Objects.requireNonNull(ledger, "ledger").restore(
            knowledge,
            Set.copyOf(Objects.requireNonNull(activeDefinitions, "activeDefinitions")),
            Objects.requireNonNull(migrations, "migrations"));
    }

    @Override
    public CompoundTag save(CompoundTag root, HolderLookup.Provider registries) {
        root.putInt("schema", SCHEMA_VERSION);
        root.put("knowledge", writeKnowledge(knowledge));
        return root;
    }

    private static ListTag writeKnowledge(Map<UUID, List<ArcanaSpellId>> entries) {
        ListTag list = new ListTag();
        int casterCount = 0;
        for (Map.Entry<UUID, List<ArcanaSpellId>> entry : entries.entrySet()) {
            if (casterCount >= MAX_PERSISTED_CASTERS) break;
            UUID caster = entry.getKey();
            List<ArcanaSpellId> spells = entry.getValue();
            if (caster == null || spells == null) continue;
            CompoundTag tag = new CompoundTag();
            tag.putUUID("caster", caster);
            ListTag spellList = new ListTag();
            int spellCount = Math.min(spells.size(), MAX_PERSISTED_SPELLS_PER_CASTER);
            for (int i = 0; i < spellCount; i++) {
                ArcanaSpellId spell = spells.get(i);
                if (spell != null) spellList.add(StringTag.valueOf(spell.canonical()));
            }
            tag.put("spells", spellList);
            list.add(tag);
            casterCount++;
        }
        return list;
    }

    private static Map<UUID, List<ArcanaSpellId>> readKnowledge(ListTag list) {
        Map<UUID, List<ArcanaSpellId>> result = new LinkedHashMap<>();
        int casterCount = Math.min(list.size(), MAX_PERSISTED_CASTERS);
        for (int i = 0; i < casterCount; i++) {
            CompoundTag tag = list.getCompound(i);
            try {
                UUID caster = tag.getUUID("caster");
                ListTag spellTags = tag.getList("spells", Tag.TAG_STRING);
                int spellCount = Math.min(spellTags.size(), MAX_PERSISTED_SPELLS_PER_CASTER);
                List<ArcanaSpellId> spells = new ArrayList<>(spellCount);
                for (int j = 0; j < spellCount; j++) {
                    try {
                        spells.add(ArcanaSpellId.parse(spellTags.getString(j)));
                    } catch (RuntimeException ignored) {
                        // Drop only the malformed spell id; retain the rest of this caster's knowledge.
                    }
                }
                if (!spells.isEmpty()) result.put(caster, List.copyOf(spells));
            } catch (RuntimeException ignored) {
                // A malformed player record must never poison the entire knowledge save.
            }
        }
        return Map.copyOf(result);
    }
}
