package dev.gustavopere.blackarcana.client;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Pure client-local focus traversal for bounded Stage 05 screens. */
final class ScreenFocusNavigation {
    enum InputModality {
        POINTER,
        KEYBOARD
    }

    private ScreenFocusNavigation() { }

    static int initialFocus(List<Integer> visible, int preferred) {
        Objects.requireNonNull(visible, "visible");
        if (visible.isEmpty()) return -1;
        return visible.contains(preferred) ? preferred : visible.get(0);
    }

    static int moveWrapped(List<Integer> visible, int current, int direction) {
        Objects.requireNonNull(visible, "visible");
        if (visible.isEmpty()) return -1;
        int position = visible.indexOf(current);
        if (position < 0) position = 0;
        int delta = Integer.compare(direction, 0);
        return visible.get(Math.floorMod(position + delta, visible.size()));
    }

    static int moveClamped(List<Integer> visible, int current, int direction) {
        Objects.requireNonNull(visible, "visible");
        if (visible.isEmpty()) return -1;
        int position = visible.indexOf(current);
        if (position < 0) position = 0;
        int delta = Integer.compare(direction, 0);
        int destination = Math.max(0, Math.min(visible.size() - 1, position + delta));
        return visible.get(destination);
    }

    static int transitionFocus(
            List<Integer> source,
            List<Integer> destination,
            int current,
            int preferredDestination
    ) {
        Objects.requireNonNull(source, "source");
        Objects.requireNonNull(destination, "destination");
        if (destination.isEmpty()) return -1;
        if (destination.contains(preferredDestination)) return preferredDestination;

        int relativePosition = source.indexOf(current);
        if (relativePosition < 0) relativePosition = 0;
        relativePosition = Math.min(relativePosition, destination.size() - 1);
        return destination.get(relativePosition);
    }

    static List<Integer> pageIndices(int totalEntries, int page, int pageSize) {
        if (totalEntries < 0) throw new IllegalArgumentException("totalEntries cannot be negative");
        if (page < 0) throw new IllegalArgumentException("page cannot be negative");
        if (pageSize <= 0) throw new IllegalArgumentException("pageSize must be positive");
        int start = Math.min(totalEntries, page * pageSize);
        int end = Math.min(totalEntries, start + pageSize);
        List<Integer> indices = new ArrayList<>(Math.max(0, end - start));
        for (int index = start; index < end; index++) indices.add(index);
        return List.copyOf(indices);
    }

    static int presentationFocus(InputModality modality, int hovered, int keyboardFocused, int fallback) {
        Objects.requireNonNull(modality, "modality");
        int primary = modality == InputModality.KEYBOARD ? keyboardFocused : hovered;
        return primary >= 0 ? primary : fallback;
    }
}
