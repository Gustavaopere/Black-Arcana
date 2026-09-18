package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataDefinition;
import dev.gustavopere.blackarcana.config.SpellIdMigrations;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneDangerProfileRuntimeStoreTest {
    @AfterEach
    void resetGlobalState() {
        ArcaneDangerProfileRuntimeStore.configureMigrations(new SpellIdMigrations(Map.of(), Map.of()));
        ArcaneDangerProfileRuntimeStore.reload(Map.of());
    }

    @Test
    void reloadPublishesToExistingAndFutureRuntimeRegistries() {
        ArcanaSpellId id = ArcanaSpellId.parse("black_arcana:store_probe");
        ArcanaServerRuntime first = ArcanaServerRuntime.createDefault();
        ArcanaServerRuntime second = null;
        try {
            var firstRegistry = ArcaneDangerProfileRuntimeStore.forRuntime(first);
            ArcaneDangerProfileRuntimeStore.reload(Map.of(id, definition(id)));

            assertEquals(ArcaneDangerTier.DANGEROUS, firstRegistry.resolve(id).orElseThrow().tier());
            second = ArcanaServerRuntime.createDefault();
            assertEquals(
                ArcaneDangerTier.DANGEROUS,
                ArcaneDangerProfileRuntimeStore.forRuntime(second).resolve(id).orElseThrow().tier());
        } finally {
            ArcaneDangerProfileRuntimeStore.remove(first);
            if (second != null) ArcaneDangerProfileRuntimeStore.remove(second);
        }
    }

    @Test
    void explicitSpellIdMigrationRewritesHazardProfileIdentityBeforePublication() {
        ArcanaSpellId oldId = ArcanaSpellId.parse("black_arcana:old_hazard");
        ArcanaSpellId intermediate = ArcanaSpellId.parse("black_arcana:middle_hazard");
        ArcanaSpellId current = ArcanaSpellId.parse("black_arcana:current_hazard");
        ArcaneDangerProfileRuntimeStore.configureMigrations(new SpellIdMigrations(
            Map.of(oldId, intermediate, intermediate, current),
            Map.of()));

        Map<ArcanaSpellId, ArcaneDangerDataDefinition> migrated =
            ArcaneDangerProfileRuntimeStore.migrateDefinitions(Map.of(oldId, definition(oldId)));

        assertFalse(migrated.containsKey(oldId));
        assertTrue(migrated.containsKey(current));
        assertEquals(current.canonical(), migrated.get(current).id());

        ArcaneDangerProfileRuntimeStore.reload(Map.of(oldId, definition(oldId)));
        assertFalse(ArcaneDangerProfileRuntimeStore.currentSnapshot().containsKey(oldId));
        assertTrue(ArcaneDangerProfileRuntimeStore.currentSnapshot().containsKey(current));
    }

    @Test
    void explicitRemovalDropsRetiredHazardProfile() {
        ArcanaSpellId retired = ArcanaSpellId.parse("black_arcana:retired_hazard");
        ArcaneDangerProfileRuntimeStore.configureMigrations(new SpellIdMigrations(
            Map.of(),
            Map.of(retired, "removed from the canonical spell catalog")));

        assertTrue(ArcaneDangerProfileRuntimeStore
            .migrateDefinitions(Map.of(retired, definition(retired)))
            .isEmpty());
    }

    @Test
    void convergingMigrationsFailClosedInsteadOfSilentlyOverwritingProfiles() {
        ArcanaSpellId first = ArcanaSpellId.parse("black_arcana:first_old_hazard");
        ArcanaSpellId second = ArcanaSpellId.parse("black_arcana:second_old_hazard");
        ArcanaSpellId current = ArcanaSpellId.parse("black_arcana:current_hazard");
        ArcaneDangerProfileRuntimeStore.configureMigrations(new SpellIdMigrations(
            Map.of(first, current, second, current),
            Map.of()));

        assertThrows(IllegalArgumentException.class, () ->
            ArcaneDangerProfileRuntimeStore.migrateDefinitions(Map.of(
                first, definition(first),
                second, definition(second))));
    }

    @Test
    void invalidReloadPreservesPreviouslyPublishedSnapshot() {
        ArcanaSpellId valid = ArcanaSpellId.parse("black_arcana:stable_hazard");
        ArcaneDangerProfileRuntimeStore.reload(Map.of(valid, definition(valid)));
        Map<ArcanaSpellId, ?> before = ArcaneDangerProfileRuntimeStore.currentSnapshot();

        LinkedHashMap<ArcanaSpellId, ArcaneDangerDataDefinition> invalid = new LinkedHashMap<>();
        invalid.put(ArcanaSpellId.parse("black_arcana:broken_hazard"), null);

        assertThrows(NullPointerException.class, () -> ArcaneDangerProfileRuntimeStore.reload(invalid));
        assertEquals(before, ArcaneDangerProfileRuntimeStore.currentSnapshot());
    }

    private static ArcaneDangerDataDefinition definition(ArcanaSpellId id) {
        return new ArcaneDangerDataDefinition(
            1, 1, id.canonical(), ArcaneDangerTier.DANGEROUS,
            1.0D, 1.0D, 1.0D, 100L, 8, 20.0D, 40.0D, true);
    }
}
