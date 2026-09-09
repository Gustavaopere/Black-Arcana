package dev.gustavopere.blackarcana.client;

import java.util.List;

/**
 * Pure client-local focus navigation for Stage 05 screens.
 *
 * <p>This helper owns no gameplay authority, persistence or networking. It only maps bounded
 * snapshotted list/page facts to a canonical focused index.</p>
 */
public final class KeyboardFocusNavigation {
    public enum InputModality {
        POINTER,
        KEYBOARD
    }

    private KeyboardFocusNavigation() { }

    public static int radialInitialFocus(int totalSlots, int page, int selectedSlot) {
        List<Integer> visible = RadialLayout.visibleSlots(totalSlots, page);
        if (visible.isEmpty()) return -1;
        return visible.contains(selectedSlot) ? selectedSlot : visible.getFirst();
    }

    public static int radialTraverse(int totalSlots, int page, int focusedSlot, int direction) {
        List<Integer> visible = RadialLayout.visibleSlots(totalSlots, page);
        if (visible.isEmpty()) return -1;

        int current = visible.indexOf(focusedSlot);
        if (current < 0) return direction < 0 ? visible.getLast() : visible.getFirst();
        int step = Integer.compare(direction, 0);
        if (step == 0) return focusedSlot;
        return visible.get(Math.floorMod(current + step, visible.size()));
    }

    public static int radialFocusAfterPageChange(
            int totalSlots,
            int sourcePage,
            int destinationPage,
            int selectedSlot,
            int focusedSlot
    ) {
        List<Integer> destination = RadialLayout.visibleSlots(totalSlots, destinationPage);
        if (destination.isEmpty()) return -1;
        if (destination.contains(selectedSlot)) return selectedSlot;

        List<Integer> source = RadialLayout.visibleSlots(totalSlots, sourcePage);
        int relative = source.indexOf(focusedSlot);
        if (relative < 0) relative = 0;
        return destination.get(Math.min(relative, destination.size() - 1));
    }

    public static int loadoutInitialFocus(
            int totalEntries,
            int page,
            int rowsPerPage,
            int preferredIndex
    ) {
        PageRange range = pageRange(totalEntries, page, rowsPerPage);
        if (range.empty()) return -1;
        if (preferredIndex >= range.start() && preferredIndex < range.endExclusive()) return preferredIndex;
        return range.start();
    }

    public static int loadoutMoveRow(
            int totalEntries,
            int page,
            int rowsPerPage,
            int focusedIndex,
            int direction
    ) {
        PageRange range = pageRange(totalEntries, page, rowsPerPage);
        if (range.empty()) return -1;
        if (focusedIndex < range.start() || focusedIndex >= range.endExclusive()) return range.start();

        int step = Integer.compare(direction, 0);
        return Math.max(range.start(), Math.min(focusedIndex + step, range.endExclusive() - 1));
    }

    public static int loadoutFocusAfterPageChange(
            int totalEntries,
            int sourcePage,
            int destinationPage,
            int rowsPerPage,
            int focusedIndex
    ) {
        PageRange source = pageRange(totalEntries, sourcePage, rowsPerPage);
        PageRange destination = pageRange(totalEntries, destinationPage, rowsPerPage);
        if (destination.empty()) return -1;

        int relative = focusedIndex >= source.start() && focusedIndex < source.endExclusive()
                ? focusedIndex - source.start()
                : 0;
        return destination.start() + Math.min(relative, destination.size() - 1);
    }

    private static PageRange pageRange(int totalEntries, int page, int rowsPerPage) {
        if (totalEntries < 0) throw new IllegalArgumentException("totalEntries cannot be negative");
        if (rowsPerPage <= 0) throw new IllegalArgumentException("rowsPerPage must be positive");
        int pages = Math.max(1, (totalEntries + rowsPerPage - 1) / rowsPerPage);
        int safePage = Math.max(0, Math.min(page, pages - 1));
        int start = safePage * rowsPerPage;
        int end = Math.min(totalEntries, start + rowsPerPage);
        return new PageRange(start, end);
    }

    private record PageRange(int start, int endExclusive) {
        int size() {
            return endExclusive - start;
        }

        boolean empty() {
            return size() == 0;
        }
    }
}
