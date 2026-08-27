package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConfigContractTest {
    @Test
    void onlyServerScopeCanAuthorGameplayOutcomes() {
        assertTrue(ConfigScope.SERVER.isGameplayAuthority());
        assertFalse(ConfigScope.COMMON.isGameplayAuthority());
        assertFalse(ConfigScope.CLIENT.isGameplayAuthority());
        assertTrue(ConfigScope.CLIENT.isClientOnly());
    }

    @Test
    void malformedSpellDataProducesDeterministicDiagnostics() {
        SpellDataDefinition malformed = new SpellDataDefinition(99, "Bad Id", "", "");
        assertEquals(4, malformed.validate().size());
        assertTrue(malformed.validate().get(0).contains("schemaVersion"));
    }

    @Test
    void oldIdsCanBeReplacedOrSafelyRemoved() {
        ArcanaSpellId oldId = ArcanaSpellId.parse("black_arcana:old_spell");
        ArcanaSpellId middleId = ArcanaSpellId.parse("black_arcana:middle_spell");
        ArcanaSpellId newId = ArcanaSpellId.parse("black_arcana:new_spell");
        ArcanaSpellId removed = ArcanaSpellId.parse("black_arcana:removed_spell");
        SpellIdMigrations migrations = new SpellIdMigrations(
                Map.of(oldId, middleId, middleId, newId),
                Map.of(removed, "retired"));

        assertEquals(newId, migrations.resolve(oldId).orElseThrow());
        assertTrue(migrations.resolve(removed).isEmpty());
        assertEquals("retired", migrations.removalReason(removed).orElseThrow());
    }

    @Test
    void replacementChainsCanTerminateInExplicitRemoval() {
        ArcanaSpellId oldId = ArcanaSpellId.parse("black_arcana:legacy_spell");
        ArcanaSpellId retiredId = ArcanaSpellId.parse("black_arcana:retired_spell");
        SpellIdMigrations migrations = new SpellIdMigrations(
                Map.of(oldId, retiredId),
                Map.of(retiredId, "removed after redesign"));

        assertTrue(migrations.resolve(oldId).isEmpty());
        assertEquals("removed after redesign", migrations.removalReason(oldId).orElseThrow());
    }

    @Test
    void migrationCyclesAndConflictsAreRejectedAtConstruction() {
        ArcanaSpellId a = ArcanaSpellId.parse("black_arcana:a");
        ArcanaSpellId b = ArcanaSpellId.parse("black_arcana:b");

        assertThrows(IllegalArgumentException.class, () -> new SpellIdMigrations(Map.of(a, b, b, a), Map.of()));
        assertThrows(IllegalArgumentException.class, () -> new SpellIdMigrations(Map.of(a, b), Map.of(a, "also removed")));
        assertThrows(IllegalArgumentException.class, () -> new SpellIdMigrations(Map.of(), Map.of(a, "")));
    }
}
