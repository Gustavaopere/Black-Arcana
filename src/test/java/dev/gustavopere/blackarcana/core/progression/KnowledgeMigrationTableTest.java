package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class KnowledgeMigrationTableTest {
    @Test void chainedRenameAndRemovalResolveTransitively() {
        var a = ArcanaSpellId.parse("black_arcana:a");
        var b = ArcanaSpellId.parse("black_arcana:b");
        var c = ArcanaSpellId.parse("black_arcana:c");
        var table = new KnowledgeMigrationTable();
        table.replace(a, b, "rename one");
        table.replace(b, c, "rename two");
        assertEquals(c, table.resolve(a).orElseThrow());
        table.remove(c, "removed intentionally");
        assertTrue(table.resolve(a).isEmpty());
    }

    @Test void cycleIsRejectedWithoutPoisoningTable() {
        var a = ArcanaSpellId.parse("black_arcana:a");
        var b = ArcanaSpellId.parse("black_arcana:b");
        var table = new KnowledgeMigrationTable();
        table.replace(a, b, "rename");
        assertThrows(IllegalStateException.class, () -> table.replace(b, a, "bad cycle"));
        assertEquals(b, table.resolve(a).orElseThrow());
        assertEquals(b, table.resolve(b).orElseThrow());
    }
}
