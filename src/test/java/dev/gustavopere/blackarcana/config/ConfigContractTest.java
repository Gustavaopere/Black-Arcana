package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
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
        ArcanaSpellId newId = ArcanaSpellId.parse("black_arcana:new_spell");
        ArcanaSpellId removed = ArcanaSpellId.parse("black_arcana:removed_spell");
        SpellIdMigrations migrations = new SpellIdMigrations(Map.of(oldId, newId), Map.of(removed, "retired"));

        assertEquals(newId, migrations.resolve(oldId).orElseThrow());
        assertTrue(migrations.resolve(removed).isEmpty());
        assertEquals("retired", migrations.removalReason(removed).orElseThrow());
    }
}
