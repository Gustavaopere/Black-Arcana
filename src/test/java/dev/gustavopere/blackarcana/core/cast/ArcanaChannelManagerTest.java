package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaChannelManagerTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:charged_spell");
    private static final ArcanaChannelSpec SPEC = new ArcanaChannelSpec(10, 40);

    @Test
    void releaseBeforeMinimumKeepsSessionActiveThenValidReleaseConsumesIt() {
        ArcanaChannelManager manager = new ArcanaChannelManager(4);
        assertTrue(manager.begin(CASTER, CAST, SPELL, 100, SPEC).allowed());

        var early = manager.release(CASTER, CAST, 105);
        assertFalse(early.decision().allowed());
        assertEquals("channel_too_short", early.decision().code());
        assertEquals(1, manager.activeSessions());

        var released = manager.release(CASTER, CAST, 110);
        assertTrue(released.decision().allowed());
        assertEquals(10, released.released().orElseThrow().channelTicks());
        assertEquals(0, manager.activeSessions());
    }

    @Test
    void wrongIdCannotReleaseSomeoneElsesSession() {
        ArcanaChannelManager manager = new ArcanaChannelManager(4);
        manager.begin(CASTER, CAST, SPELL, 100, SPEC);
        var result = manager.release(CASTER, ArcanaCastId.parse("22222222-2222-2222-2222-222222222222"), 120);
        assertEquals("channel_id_mismatch", result.decision().code());
        assertEquals(1, manager.activeSessions());
    }

    @Test
    void expiredSessionIsRemovedAndCannotExecute() {
        ArcanaChannelManager manager = new ArcanaChannelManager(4);
        manager.begin(CASTER, CAST, SPELL, 100, SPEC);
        var result = manager.release(CASTER, CAST, 141);
        assertEquals("channel_expired", result.decision().code());
        assertEquals(0, manager.activeSessions());
    }
}
