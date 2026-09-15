package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientChannelInvocationStateTest {
    @Test
    void onePhysicalInputOwnsOneExactClientChannelUntilRelease() {
        ClientChannelInvocationState state = new ClientChannelInvocationState();
        ArcanaCastId castId = ArcanaCastId.random();
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:astral_severance");

        assertTrue(state.begin(7, 3, spell, castId));
        assertFalse(state.begin(8, 4, spell, ArcanaCastId.random()),
                "client must not create a second local channel while the server permits one session per caster");
        assertTrue(state.releaseWhenUp(8, false).isEmpty(),
                "an unrelated key release must not release another input source's channel");
        assertTrue(state.releaseWhenUp(7, true).isEmpty(),
                "holding the owning key must preserve the active channel");
        assertEquals(castId, state.releaseWhenUp(7, false).orElseThrow());
        assertTrue(state.active().isEmpty());
    }

    @Test
    void staleBeginDenialCannotClearANewerLocalSession() {
        ClientChannelInvocationState state = new ClientChannelInvocationState();
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:astral_severance");
        ArcanaCastId first = ArcanaCastId.random();
        ArcanaCastId second = ArcanaCastId.random();

        assertTrue(state.begin(1, 0, spell, first));
        assertEquals(first, state.cancel().orElseThrow());
        assertTrue(state.begin(2, 1, spell, second));
        state.rejectBegin(first);

        assertEquals(second, state.active().orElseThrow().castId());
        assertEquals(1, state.active().orElseThrow().loadoutSlot());
    }
}
