package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ArcanaKnowledgeLedgerTest {
    private static final ArcanaSpellId OLD = ArcanaSpellId.parse("black_arcana:old_name");
    private static final ArcanaSpellId CURRENT = ArcanaSpellId.parse("black_arcana:current_name");
    private static final ArcanaSpellId UNKNOWN = ArcanaSpellId.parse("black_arcana:missing_definition");

    @Test void unlockIsIdempotentAndIndependentFromLoadoutState() {
        var ledger = new ArcanaKnowledgeLedger(4, 2);
        UUID caster = UUID.randomUUID();
        assertEquals(ArcanaKnowledgeLedger.UnlockResult.UNLOCKED, ledger.unlock(caster, CURRENT));
        assertEquals(ArcanaKnowledgeLedger.UnlockResult.ALREADY_KNOWN, ledger.unlock(caster, CURRENT));
        assertTrue(ledger.knows(caster, CURRENT));
        assertEquals(Set.of(CURRENT), ledger.knownSpells(caster));
    }

    @Test void restoreMigratesExplicitlyAndNeverSilentlyUnlocksUnknownIds() {
        UUID caster = UUID.randomUUID();
        var migrations = new KnowledgeMigrationTable();
        migrations.replace(OLD, CURRENT, "renamed during clean-room naming freeze");
        var ledger = new ArcanaKnowledgeLedger(4, 4);
        var result = ledger.restore(Map.of(caster, List.of(OLD, UNKNOWN)), Set.of(CURRENT), migrations);
        assertEquals(1, result.spellsRestored());
        assertEquals(1, result.migrated());
        assertEquals(1, result.dropped());
        assertTrue(ledger.knows(caster, CURRENT));
        assertFalse(ledger.knows(caster, UNKNOWN));
    }

    @Test void capacityFailsClosed() {
        var ledger = new ArcanaKnowledgeLedger(1, 1);
        UUID first = UUID.randomUUID(); UUID second = UUID.randomUUID();
        assertEquals(ArcanaKnowledgeLedger.UnlockResult.UNLOCKED, ledger.unlock(first, CURRENT));
        assertEquals(ArcanaKnowledgeLedger.UnlockResult.KNOWLEDGE_CAPACITY, ledger.unlock(first, UNKNOWN));
        assertEquals(ArcanaKnowledgeLedger.UnlockResult.CASTER_CAPACITY, ledger.unlock(second, CURRENT));
    }
}
