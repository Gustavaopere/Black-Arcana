package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ClientLoadoutSelectionTest {
    private static final ArcanaSpellId A = ArcanaSpellId.parse("black_arcana:a");
    private static final ArcanaSpellId B = ArcanaSpellId.parse("black_arcana:b");

    @Test
    void selectionNeverEscapesServerConfirmedSnapshot() {
        var selection = new ClientLoadoutSelection();
        assertTrue(selection.select(1, List.of(A, B)));
        assertEquals(B, selection.selected(List.of(A, B)).orElseThrow());
        assertFalse(selection.select(2, List.of(A, B)));
        assertEquals(1, selection.selectedSlot());
    }

    @Test
    void selectedCastCanReachLastCanonicalSlotBeyondQuickCastRange() {
        List<ArcanaSpellId> loadout = IntStream.range(0, ArcanaCastRequest.MAX_LOADOUT_SLOTS)
                .mapToObj(index -> ArcanaSpellId.parse("black_arcana:slot_" + index))
                .toList();
        var selection = new ClientLoadoutSelection();
        int lastSlot = ArcanaCastRequest.MAX_LOADOUT_SLOTS - 1;

        assertTrue(selection.select(lastSlot, loadout));
        assertEquals(lastSlot, selection.selectedSlot());
        assertEquals(loadout.get(lastSlot), selection.selected(loadout).orElseThrow());
    }

    @Test
    void staleSelectionIsClampedAfterServerLoadoutShrinks() {
        var selection = new ClientLoadoutSelection();
        assertTrue(selection.select(1, List.of(A, B)));
        selection.reconcile(List.of(A));
        assertEquals(0, selection.selectedSlot());
        assertEquals(A, selection.selected(List.of(A)).orElseThrow());
    }

    @Test
    void emptySnapshotClearsSelectionSafely() {
        var selection = new ClientLoadoutSelection();
        selection.select(1, List.of(A, B));
        selection.reconcile(List.of());
        assertEquals(0, selection.selectedSlot());
        assertTrue(selection.selected(List.of()).isEmpty());
    }
}
