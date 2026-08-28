package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoadoutDraftTest {
    @Test
    void togglingAddsAndRemovesWithoutDuplicates() {
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:test");
        LoadoutDraft draft = new LoadoutDraft(List.of());
        assertTrue(draft.toggle(spell));
        assertEquals(List.of(spell), draft.snapshot());
        assertTrue(draft.toggle(spell));
        assertTrue(draft.snapshot().isEmpty());
    }

    @Test
    void draftCannotExceedServerSlotBound() {
        List<ArcanaSpellId> initial = new ArrayList<>();
        for (int i = 0; i < ArcanaCastRequest.MAX_LOADOUT_SLOTS; i++) {
            initial.add(ArcanaSpellId.parse("black_arcana:spell_" + i));
        }
        LoadoutDraft draft = new LoadoutDraft(initial);
        assertFalse(draft.toggle(ArcanaSpellId.parse("black_arcana:overflow")));
        assertEquals(ArcanaCastRequest.MAX_LOADOUT_SLOTS, draft.snapshot().size());
    }
}
