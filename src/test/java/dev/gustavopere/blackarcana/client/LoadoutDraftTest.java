package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

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

    @Test
    void movingFirstSpellToLastPreservesDenseOrderedIdentitySet() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        assertTrue(move(draft, 0, 2));

        assertEquals(List.of(b, c, a), draft.snapshot());
    }

    @Test
    void movingLastSpellToFirstPreservesDenseOrderedIdentitySet() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        assertTrue(move(draft, 2, 0));

        assertEquals(List.of(c, a, b), draft.snapshot());
    }

    @Test
    void movingMiddleSpellPreservesSizeAndUniqueness() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        ArcanaSpellId d = spell("d");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c, d));

        assertTrue(move(draft, 1, 2));

        assertEquals(List.of(a, c, b, d), draft.snapshot());
        assertEquals(4, draft.snapshot().size());
        assertEquals(4, draft.snapshot().stream().distinct().count());
    }

    @Test
    void invalidMoveIndexesFailSafelyWithoutMutatingDraft() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));
        List<ArcanaSpellId> baseline = draft.snapshot();

        assertFalse(move(draft, -1, 1));
        assertFalse(move(draft, 0, 3));
        assertFalse(move(draft, 3, 0));

        assertEquals(baseline, draft.snapshot());
    }

    @Test
    void removingCompactsAndAddingAppendsAtTrailingPosition() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        ArcanaSpellId d = spell("d");
        LoadoutDraft draft = new LoadoutDraft(List.of(a, b, c));

        assertTrue(draft.toggle(b));
        assertEquals(List.of(a, c), draft.snapshot());

        assertTrue(draft.toggle(d));
        assertEquals(List.of(a, c, d), draft.snapshot());
    }

    private static ArcanaSpellId spell(String path) {
        return ArcanaSpellId.parse("black_arcana:" + path);
    }

    private static boolean move(LoadoutDraft draft, int fromIndex, int toIndex) {
        try {
            Method move = LoadoutDraft.class.getDeclaredMethod("move", int.class, int.class);
            return (boolean) move.invoke(draft, fromIndex, toIndex);
        } catch (NoSuchMethodException exception) {
            return fail("LoadoutDraft.move(int,int) is missing", exception);
        } catch (ReflectiveOperationException exception) {
            return fail("LoadoutDraft.move(int,int) could not be invoked", exception);
        }
    }
}
