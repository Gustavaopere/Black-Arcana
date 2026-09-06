package dev.gustavopere.blackarcana.client;

import java.util.ArrayList;
import java.util.List;

/** Pure radial geometry shared by rendering and tests. */
public final class RadialLayout {
    public static final int SLOTS_PER_PAGE = 8;

    private RadialLayout() { }

    public static int pageCount(int totalSlots) {
        if (totalSlots < 0) throw new IllegalArgumentException("totalSlots cannot be negative");
        return Math.max(1, (totalSlots + SLOTS_PER_PAGE - 1) / SLOTS_PER_PAGE);
    }

    public static int clampPage(int totalSlots, int page) {
        int pages = pageCount(totalSlots);
        return Math.max(0, Math.min(page, pages - 1));
    }

    public static List<Integer> visibleSlots(int totalSlots, int page) {
        if (totalSlots < 0) throw new IllegalArgumentException("totalSlots cannot be negative");
        int safePage = clampPage(totalSlots, page);
        int start = safePage * SLOTS_PER_PAGE;
        int end = Math.min(totalSlots, start + SLOTS_PER_PAGE);
        List<Integer> slots = new ArrayList<>(Math.max(0, end - start));
        for (int slot = start; slot < end; slot++) slots.add(slot);
        return List.copyOf(slots);
    }

    public static CardMetrics cardMetricsForViewport(int width, int height) {
        if (width <= 0 || height <= 0) {
            throw new IllegalArgumentException("viewport dimensions must be positive");
        }
        boolean compact = width < 300 || height < 180;
        return compact
                ? new CardMetrics(15, 7, true)
                : new CardMetrics(34, 10, false);
    }

    public static double radiusForViewport(
            int width,
            int height,
            int slotHalfWidth,
            int slotHalfHeight,
            double preferredRadius,
            int margin
    ) {
        if (width <= 0 || height <= 0 || slotHalfWidth < 0 || slotHalfHeight < 0 || margin < 0) {
            throw new IllegalArgumentException("invalid radial viewport geometry");
        }
        if (!Double.isFinite(preferredRadius) || preferredRadius <= 0.0D) {
            throw new IllegalArgumentException("preferredRadius must be finite and positive");
        }
        double horizontal = width / 2.0D - slotHalfWidth - margin;
        double vertical = height / 2.0D - slotHalfHeight - margin;
        return Math.max(1.0D, Math.min(preferredRadius, Math.min(horizontal, vertical)));
    }

    public static Point slotCenter(int visibleIndex, int visibleCount, double centerX, double centerY, double radius) {
        if (visibleCount <= 0 || visibleCount > SLOTS_PER_PAGE) {
            throw new IllegalArgumentException("visibleCount outside radial bounds");
        }
        if (visibleIndex < 0 || visibleIndex >= visibleCount) {
            throw new IllegalArgumentException("visibleIndex outside visible range");
        }
        if (!Double.isFinite(radius) || radius <= 0.0D) throw new IllegalArgumentException("radius must be finite and positive");
        double angle = -Math.PI / 2.0D + (Math.PI * 2.0D * visibleIndex / visibleCount);
        return new Point(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);
    }

    public static int hoveredSlot(
            int totalSlots,
            int page,
            double mouseX,
            double mouseY,
            double centerX,
            double centerY,
            double innerRadius,
            double outerRadius
    ) {
        if (innerRadius < 0.0D || outerRadius <= innerRadius) {
            throw new IllegalArgumentException("invalid radial hit radii");
        }
        List<Integer> visible = visibleSlots(totalSlots, page);
        if (visible.isEmpty()) return -1;
        double dx = mouseX - centerX;
        double dy = mouseY - centerY;
        double distanceSquared = dx * dx + dy * dy;
        if (distanceSquared < innerRadius * innerRadius || distanceSquared > outerRadius * outerRadius) return -1;

        double angle = Math.atan2(dy, dx) + Math.PI / 2.0D;
        if (angle < 0.0D) angle += Math.PI * 2.0D;
        double sector = Math.PI * 2.0D / visible.size();
        int visibleIndex = (int) Math.floor((angle + sector / 2.0D) / sector) % visible.size();
        return visible.get(visibleIndex);
    }

    public record CardMetrics(int halfWidth, int halfHeight, boolean compact) {
        public CardMetrics {
            if (halfWidth <= 0 || halfHeight <= 0) {
                throw new IllegalArgumentException("radial card dimensions must be positive");
            }
        }
    }

    public record Point(double x, double y) { }
}
