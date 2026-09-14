package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaChannelLifecycleCancellationTest {
    private static final UUID CASTER = UUID.fromString("e37cf51d-e1aa-482a-af60-f0abaea47f6d");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("33333333-3333-3333-3333-333333333333");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:lifecycle_channel_probe");
    private static final ArcanaChannelSpec SPEC = new ArcanaChannelSpec(5L, 40L);

    @Test
    void trustedCasterLifecycleCancellationRemovesSessionWithoutClientCastId() {
        ArcanaChannelManager manager = new ArcanaChannelManager(4);
        assertTrue(manager.begin(CASTER, CAST, SPELL, 2, 100L, SPEC).allowed());
        assertEquals(1, manager.activeSessions());

        assertTrue(manager.cancelCaster(CASTER));
        assertEquals(0, manager.activeSessions());
        assertFalse(manager.cancelCaster(CASTER), "lifecycle cancellation must be idempotent");
    }
}
