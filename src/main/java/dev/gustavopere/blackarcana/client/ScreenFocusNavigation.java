package dev.gustavopere.blackarcana.client;

import java.util.List;
import java.util.Objects;

/** Pure client-local focus traversal for bounded Stage 05 screens. */
final class ScreenFocusNavigation {
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
}
