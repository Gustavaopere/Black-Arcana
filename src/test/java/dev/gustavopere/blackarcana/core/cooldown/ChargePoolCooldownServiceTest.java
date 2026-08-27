package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChargeSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ChargePoolCooldownServiceTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:test"),
            "spell.black_arcana.test",
            "black_arcana:test",
            new ArcanaCost("black_arcana:test", 1.0), false);

    private static ArcanaCastRequest request(long tick) {
        return new ArcanaCastRequest(SPELL, new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    @Test
    void chargesDepleteAndRechargeOverTime() {
        ChargePoolCooldownService service = new ChargePoolCooldownService(req -> new ArcanaChargeSpec("black_arcana:blink", 2, 20, true));

        assertEquals(2, service.charges(request(100)));
        service.start(request(100));
        assertEquals(1, service.charges(request(100)));
        service.start(request(101));
        assertEquals(0, service.charges(request(101)));
        assertFalse(service.check(request(119)).allowed());
        assertTrue(service.check(request(120)).allowed());
        assertEquals(1, service.charges(request(120)));
        assertEquals(2, service.charges(request(140)));
    }

    @Test
    void persistentSnapshotRestoresDepletedPool() {
        ChargePoolCooldownService first = new ChargePoolCooldownService(req -> new ArcanaChargeSpec("black_arcana:blink", 2, 20, true));
        first.start(request(100));
        first.start(request(101));
        var snapshot = first.persistentSnapshot();

        ChargePoolCooldownService restored = new ChargePoolCooldownService(req -> new ArcanaChargeSpec("black_arcana:blink", 2, 20, true));
        restored.restorePersistentSnapshot(snapshot);
        assertEquals(0, restored.charges(request(101)));
        assertEquals(1, restored.charges(request(120)));
    }
}
