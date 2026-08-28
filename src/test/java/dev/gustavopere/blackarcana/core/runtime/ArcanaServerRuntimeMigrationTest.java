package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChargeSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.RuntimeGroupMigrations;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class ArcanaServerRuntimeMigrationTest {
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
    void renamedCooldownAndChargeGroupsSurviveCanonicalPrune() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.cooldownPolicies().replaceAll(
                Map.of(SPELL.id(), new ArcanaCooldownSpec("black_arcana:new_cd", 100L, true)),
                Map.of(SPELL.id(), new ArcanaChargeSpec("black_arcana:new_charge", 3, 20L, true)));
        runtime.setRuntimeGroupMigrations(new RuntimeGroupMigrations(Map.of(
                "black_arcana:old_cd", "black_arcana:new_cd",
                "black_arcana:old_charge", "black_arcana:new_charge")));

        runtime.cooldowns().restorePersistentSnapshot(Map.of(
                new PersistentCooldownService.CooldownKey(CASTER, "black_arcana:old_cd"),
                new PersistentCooldownService.SnapshotEntry(100L, 200L)
        ), 150L);
        runtime.charges().restorePersistentSnapshot(Map.of(
                new ChargePoolCooldownService.ChargeKey(CASTER, "black_arcana:old_charge"),
                new ChargePoolCooldownService.SnapshotEntry(1, 190L)
        ));

        ArcanaServerRuntime.MigrationResult migrated = runtime.migrateRestoredPersistentState();
        ArcanaServerRuntime.PruneResult pruned = runtime.pruneOrphanedPersistentState();

        assertEquals(1, migrated.cooldownsRenamed());
        assertEquals(1, migrated.chargePoolsRenamed());
        assertEquals(0, pruned.cooldownsRemoved());
        assertEquals(0, pruned.chargePoolsRemoved());
        assertFalse(runtime.cooldowns().check(request(160L)).allowed());
        assertEquals(1, runtime.charges().charges(request(160L)));
    }
}
