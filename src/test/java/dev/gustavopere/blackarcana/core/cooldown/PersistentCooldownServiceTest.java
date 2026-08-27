package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicLong;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PersistentCooldownServiceTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:test_spell"),
            "spell.black_arcana.test_spell",
            "black_arcana:textures/spell/test_spell.png",
            new ArcanaCost("black_arcana:test", 1.0), false);

    private static ArcanaCastRequest request(long tick) {
        return new ArcanaCastRequest(
                ArcanaCastId.random(), SPELL,
                new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    @Test
    void sharedGroupBlocksUntilReadyTick() {
        PersistentCooldownService service = new PersistentCooldownService(req -> new ArcanaCooldownSpec("black_arcana:shared", 20, true));
        service.start(request(100));

        var denied = service.check(request(119));
        assertFalse(denied.allowed());
        assertEquals("remaining_ticks=1", denied.detail());
        assertTrue(service.check(request(120)).allowed());
        assertEquals(0, service.size());
    }

    @Test
    void persistentSnapshotSurvivesServiceRecreation() {
        PersistentCooldownService first = new PersistentCooldownService(req -> new ArcanaCooldownSpec("black_arcana:shared", 40, true));
        first.start(request(100));
        Map<PersistentCooldownService.CooldownKey, PersistentCooldownService.SnapshotEntry> snapshot = first.persistentSnapshot(110);

        PersistentCooldownService restored = new PersistentCooldownService(req -> new ArcanaCooldownSpec("black_arcana:shared", 40, true));
        restored.restorePersistentSnapshot(snapshot, 110);
        assertFalse(restored.check(request(120)).allowed());
        assertTrue(restored.check(request(140)).allowed());
    }

    @Test
    void sessionOnlyCooldownIsNotPersisted() {
        PersistentCooldownService service = new PersistentCooldownService(req -> new ArcanaCooldownSpec("black_arcana:session", 20, false));
        service.start(request(100));
        assertTrue(service.persistentSnapshot(101).isEmpty());
        assertFalse(service.check(request(101)).allowed());
    }

    @Test
    void reducedConfigClampsExistingCooldownWithoutExtendingIt() {
        AtomicLong duration = new AtomicLong(100);
        PersistentCooldownService service = new PersistentCooldownService(req -> new ArcanaCooldownSpec("black_arcana:shared", duration.get(), true));
        service.start(request(100));

        duration.set(20);
        assertFalse(service.check(request(119)).allowed());
        assertTrue(service.check(request(120)).allowed());

        service.start(request(200));
        duration.set(80);
        assertTrue(service.check(request(220)).allowed());
    }
}
