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

    public record Point(double x, double y) { }
}
