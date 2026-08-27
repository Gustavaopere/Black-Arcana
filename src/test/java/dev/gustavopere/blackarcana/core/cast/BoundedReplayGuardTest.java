package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BoundedReplayGuardTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:test_spell"),
            "spell.black_arcana.test_spell",
            "black_arcana:textures/spell/test_spell.png",
            new ArcanaCost("black_arcana:test_resource", 1.0),
            false);

    private static ArcanaCastRequest request(String id, long tick) {
        return new ArcanaCastRequest(ArcanaCastId.parse(id), SPELL, new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    @Test
    void duplicateCastIdIsRejectedWithinRetentionWindow() {
        BoundedReplayGuard guard = new BoundedReplayGuard(4, 20);
        ArcanaCastRequest request = request("11111111-1111-1111-1111-111111111111", 100);

        assertTrue(guard.claim(request).allowed());
        assertFalse(guard.claim(request("11111111-1111-1111-1111-111111111111", 101)).allowed());
        assertEquals(1, guard.size());
    }

    @Test
    void expiredClaimCanBeReusedAfterRetentionWindow() {
        BoundedReplayGuard guard = new BoundedReplayGuard(4, 20);
        assertTrue(guard.claim(request("11111111-1111-1111-1111-111111111111", 100)).allowed());
        assertTrue(guard.claim(request("11111111-1111-1111-1111-111111111111", 121)).allowed());
        assertEquals(1, guard.size());
    }

    @Test
    void capacityFailsClosedWithoutEvictingLiveClaims() {
        BoundedReplayGuard guard = new BoundedReplayGuard(2, 100);
        assertTrue(guard.claim(request("11111111-1111-1111-1111-111111111111", 10)).allowed());
        assertTrue(guard.claim(request("22222222-2222-2222-2222-222222222222", 11)).allowed());
        var denied = guard.claim(request("33333333-3333-3333-3333-333333333333", 12));
        assertFalse(denied.allowed());
        assertEquals("replay_guard_saturated", denied.code());
        assertEquals(2, guard.size());
    }
}
