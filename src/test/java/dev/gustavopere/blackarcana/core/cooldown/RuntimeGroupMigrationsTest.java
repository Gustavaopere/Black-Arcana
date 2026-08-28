package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChargeSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RuntimeGroupMigrationsTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:test_spell"),
            "spell.black_arcana.test_spell",
            "black_arcana:textures/spell/test_spell.png",
            new ArcanaCost("black_arcana:test", 1.0), false);

    private static ArcanaCastRequest request(long tick) {
        return new ArcanaCastRequest(
                ArcanaCastId.random(),
                SPELL,
                new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    @Test
    void chainedRenamesResolveAndCyclesAreRejected() {
        RuntimeGroupMigrations migrations = new RuntimeGroupMigrations(Map.of(
                "black_arcana:old", "black_arcana:middle",
                "black_arcana:middle", "black_arcana:new"));

        assertEquals("black_arcana:new", migrations.resolve("black_arcana:old"));
        assertEquals("black_arcana:new", migrations.resolve("black_arcana:new"));

        assertThrows(IllegalArgumentException.class, () -> new RuntimeGroupMigrations(Map.of(
                "black_arcana:a", "black_arcana:b",
                "black_arcana:b", "black_arcana:a")));
        assertThrows(IllegalArgumentException.class, () -> new RuntimeGroupMigrations(Map.of(
                "black_arcana:a", "black_arcana:a")));
    }

    @Test
    void cooldownCollisionPreservesLaterReadyBoundary() {
        PersistentCooldownService service = new PersistentCooldownService(
                req -> new ArcanaCooldownSpec("black_arcana:new", 100L, true));
        service.restorePersistentSnapshot(Map.of(
                new PersistentCooldownService.CooldownKey(CASTER, "black_arcana:old"),
                new PersistentCooldownService.SnapshotEntry(100L, 200L),
                new PersistentCooldownService.CooldownKey(CASTER, "black_arcana:new"),
                new PersistentCooldownService.SnapshotEntry(150L, 180L)
        ), 160L);

        assertEquals(1, service.migrateGroups(new RuntimeGroupMigrations(Map.of(
                "black_arcana:old", "black_arcana:new"))));
        assertEquals(1, service.size());
        assertFalse(service.check(request(199L)).allowed());
        assertTrue(service.check(request(200L)).allowed());
    }

    @Test
    void chargeCollisionNeverGrantsExtraChargesOrEarlierRecharge() {
        ChargePoolCooldownService service = new ChargePoolCooldownService(
                req -> new ArcanaChargeSpec("black_arcana:new", 3, 20L, true));
        service.restorePersistentSnapshot(Map.of(
                new ChargePoolCooldownService.ChargeKey(CASTER, "black_arcana:old"),
                new ChargePoolCooldownService.SnapshotEntry(2, 170L),
                new ChargePoolCooldownService.ChargeKey(CASTER, "black_arcana:new"),
                new ChargePoolCooldownService.SnapshotEntry(1, 190L)
        ));

        assertEquals(1, service.migrateGroups(new RuntimeGroupMigrations(Map.of(
                "black_arcana:old", "black_arcana:new"))));
        assertEquals(Map.of(
                new ChargePoolCooldownService.ChargeKey(CASTER, "black_arcana:new"),
                new ChargePoolCooldownService.SnapshotEntry(1, 190L)
        ), service.persistentSnapshot());
    }
}
