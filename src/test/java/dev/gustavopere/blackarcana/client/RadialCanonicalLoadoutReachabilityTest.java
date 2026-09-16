package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RadialCanonicalLoadoutReachabilityTest {
    private static final double CENTER_X = 160.0D;
    private static final double CENTER_Y = 90.0D;
    private static final double RADIUS = 78.0D;

    @Test
    void everyCanonicalSlotIsKeyboardReachableThroughRadialPagingAndSelection() {
        List<ArcanaSpellId> loadout = fullCanonicalLoadout();

        for (int targetSlot = 0; targetSlot < ArcanaCastRequest.MAX_LOADOUT_SLOTS; targetSlot++) {
            ClientLoadoutSelection selection = new ClientLoadoutSelection();
            assertTrue(selection.select(0, loadout));

            int page = 0;
            int focusedSlot = KeyboardFocusNavigation.radialInitialFocus(
                    loadout.size(), page, selection.selectedSlot());
            int relativeSlot = targetSlot % RadialLayout.SLOTS_PER_PAGE;
            for (int step = 0; step < relativeSlot; step++) {
                focusedSlot = KeyboardFocusNavigation.radialTraverse(
                        loadout.size(), page, focusedSlot, 1);
            }

            if (targetSlot >= RadialLayout.SLOTS_PER_PAGE) {
                int destinationPage = RadialLayout.clampPage(loadout.size(), page + 1);
                focusedSlot = KeyboardFocusNavigation.radialFocusAfterPageChange(
                        loadout.size(), page, destinationPage,
                        selection.selectedSlot(), focusedSlot);
                page = destinationPage;
            }

            assertTrue(RadialLayout.visibleSlots(loadout.size(), page).contains(targetSlot));
            assertEquals(targetSlot, focusedSlot);
            assertTrue(BlackArcanaRadialScreen.selectFocusedSlot(focusedSlot, loadout, selection));
            assertEquals(targetSlot, selection.selectedSlot());
            assertEquals(loadout.get(targetSlot), selection.selected(loadout).orElseThrow());
        }
    }

    @Test
    void everyCanonicalSlotIsPointerReachableOnItsRadialPage() {
        List<ArcanaSpellId> loadout = fullCanonicalLoadout();
        ClientLoadoutSelection selection = new ClientLoadoutSelection();

        for (int targetSlot = 0; targetSlot < ArcanaCastRequest.MAX_LOADOUT_SLOTS; targetSlot++) {
            int page = targetSlot / RadialLayout.SLOTS_PER_PAGE;
            List<Integer> visible = RadialLayout.visibleSlots(loadout.size(), page);
            int visibleIndex = visible.indexOf(targetSlot);
            RadialLayout.Point point = RadialLayout.slotCenter(
                    visibleIndex, visible.size(), CENTER_X, CENTER_Y, RADIUS);

            int hoveredSlot = RadialLayout.hoveredSlot(
                    loadout.size(), page,
                    point.x(), point.y(), CENTER_X, CENTER_Y,
                    28.0D, RADIUS + 34.0D);

            assertEquals(targetSlot, hoveredSlot);
            assertTrue(BlackArcanaRadialScreen.selectFocusedSlot(hoveredSlot, loadout, selection));
            assertEquals(targetSlot, selection.selectedSlot());
        }
    }

    private static List<ArcanaSpellId> fullCanonicalLoadout() {
        return IntStream.range(0, ArcanaCastRequest.MAX_LOADOUT_SLOTS)
                .mapToObj(index -> ArcanaSpellId.parse("black_arcana:slot_" + index))
                .toList();
    }
}
