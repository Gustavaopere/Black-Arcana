package dev.gustavopere.blackarcana.content.blood;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SympatheticWoundServiceTest {
    @Test
    void mirrorIsCappedByFractionEventAndLifetimeAndCannotRecurse() {
        UUID caster = UUID.randomUUID();
        UUID target = UUID.randomUUID();
        UUID event = UUID.randomUUID();
        SympatheticWoundService service = new SympatheticWoundService(8);
        service.bind(new SympatheticWoundService.LinkSpec(caster, target, 100L, 0.50D, 10.0D, 12.0D));

        var mirrored = service.mirror(new SympatheticWoundService.DamageEvent(
            event, caster, 100.0D, SympatheticWoundService.DamageProvenance.DIRECT), 10L).orElseThrow();
        assertEquals(target, mirrored.victimId());
        assertEquals(10.0D, mirrored.amount(), 1.0E-9);
        assertEquals(SympatheticWoundService.DamageProvenance.SYMPATHETIC_WOUND, mirrored.provenance());
        assertEquals(2.0D, service.remainingBudget(caster), 1.0E-9);

        assertTrue(service.mirror(mirrored, 10L).isEmpty(), "propagated damage must never recursively mirror");
        var finalMirror = service.mirror(new SympatheticWoundService.DamageEvent(
            UUID.randomUUID(), caster, 8.0D, SympatheticWoundService.DamageProvenance.DIRECT), 11L).orElseThrow();
        assertEquals(2.0D, finalMirror.amount(), 1.0E-9);
        assertEquals(0.0D, service.remainingBudget(caster), 1.0E-9);
    }

    @Test
    void expiredLinkCleansItself() {
        UUID caster = UUID.randomUUID();
        SympatheticWoundService service = new SympatheticWoundService(8);
        service.bind(new SympatheticWoundService.LinkSpec(caster, UUID.randomUUID(), 20L, 0.25D, 10.0D, 40.0D));
        assertTrue(service.mirror(new SympatheticWoundService.DamageEvent(
            UUID.randomUUID(), caster, 4.0D, SympatheticWoundService.DamageProvenance.DIRECT), 20L).isEmpty());
        assertEquals(0.0D, service.remainingBudget(caster));
    }
}
