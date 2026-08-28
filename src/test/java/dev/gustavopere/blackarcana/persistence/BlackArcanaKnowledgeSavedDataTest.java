package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.progression.ArcanaKnowledgeLedger;
import dev.gustavopere.blackarcana.core.progression.KnowledgeMigrationTable;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BlackArcanaKnowledgeSavedDataTest {
    private static final UUID CASTER = UUID.fromString("11111111-2222-3333-4444-555555555555");
    private static final ArcanaSpellId OLD = ArcanaSpellId.parse("black_arcana:old_name");
    private static final ArcanaSpellId CURRENT = ArcanaSpellId.parse("black_arcana:current_name");

    @Test
    void roundTripRestoresAndMigratesKnownSpellIds() {
        ArcanaKnowledgeLedger source = new ArcanaKnowledgeLedger(16, 16);
        source.unlock(CASTER, OLD);
        BlackArcanaKnowledgeSavedData saved = new BlackArcanaKnowledgeSavedData();
        saved.capture(source);

        CompoundTag encoded = saved.save(new CompoundTag(), null);
        BlackArcanaKnowledgeSavedData decoded = BlackArcanaKnowledgeSavedData.load(encoded, null);
        ArcanaKnowledgeLedger target = new ArcanaKnowledgeLedger(16, 16);
        KnowledgeMigrationTable migrations = new KnowledgeMigrationTable();
        migrations.replace(OLD, CURRENT, "renamed by Stage 08 migration test");

        ArcanaKnowledgeLedger.RestoreResult result = decoded.restore(target, Set.of(CURRENT), migrations);

        assertEquals(1, result.castersRestored());
        assertEquals(1, result.spellsRestored());
        assertEquals(1, result.migrated());
        assertTrue(target.knows(CASTER, CURRENT));
        assertFalse(target.knows(CASTER, OLD));
    }

    @Test
    void oldOrUnknownSchemaFailsSafeToEmptyKnowledge() {
        CompoundTag encoded = new CompoundTag();
        encoded.putInt("schema", 999);
        BlackArcanaKnowledgeSavedData decoded = BlackArcanaKnowledgeSavedData.load(encoded, null);
        ArcanaKnowledgeLedger target = new ArcanaKnowledgeLedger(16, 16);

        ArcanaKnowledgeLedger.RestoreResult result = decoded.restore(target, Set.of(CURRENT), KnowledgeMigrationTable.none());

        assertEquals(0, result.spellsRestored());
        assertTrue(target.knownSpells(CASTER).isEmpty());
    }
}
