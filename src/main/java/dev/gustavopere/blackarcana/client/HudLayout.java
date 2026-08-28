package dev.gustavopere.blackarcana.client;

/** Pure geometry/visibility policy for the contextual HUD. */
public final class HudLayout {
    public enum Anchor { TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM_CENTER }

    public record Point(int x, int y) { }

    private HudLayout() { }

    public static Point origin(
            Anchor anchor,
            int width,
            int height,
            int panelWidth,
            int panelHeight,
            int margin
    ) {
        if (width < 0 || height < 0 || panelWidth < 0 || panelHeight < 0 || margin < 0) {
            throw new IllegalArgumentException("HUD dimensions cannot be negative");
        }
        int left = margin;
        int right = Math.max(margin, width - panelWidth - margin);
        int top = margin;
        int bottom = Math.max(margin, height - panelHeight - margin);
        return switch (anchor) {
            case TOP_LEFT -> new Point(left, top);
            case TOP_RIGHT -> new Point(right, top);
            case BOTTOM_LEFT -> new Point(left, bottom);
            case BOTTOM_RIGHT -> new Point(right, bottom);
            case BOTTOM_CENTER -> new Point(Math.max(margin, (width - panelWidth) / 2), bottom);
        };
    }

    public static boolean isRecent(long now, long eventTick, int durationTicks) {
        if (durationTicks <= 0 || eventTick == Long.MIN_VALUE || now < eventTick) return false;
        return now - eventTick <= durationTicks;
    }
}
