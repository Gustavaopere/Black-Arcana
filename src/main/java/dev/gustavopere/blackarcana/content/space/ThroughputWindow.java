package dev.gustavopere.blackarcana.content.space;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Fixed-window limiter for Threshold Gate or paired transposition automation. */
public final class ThroughputWindow {
    private final int maxPerSecond;
    private final Map<UUID, Window> windows = new HashMap<>();

    public ThroughputWindow(int maxPerSecond) {
        if (maxPerSecond <= 0 || maxPerSecond > LiminalSafetyCeilings.MAX_GATE_THROUGHPUT_PER_SECOND) {
            throw new IllegalArgumentException("maxPerSecond outside hard ceiling");
        }
        this.maxPerSecond = maxPerSecond;
    }

    public synchronized boolean tryAcquire(UUID ownerId, long nowTick) {
        Objects.requireNonNull(ownerId, "ownerId");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        long windowIndex = nowTick / 20L;
        Window window = windows.get(ownerId);
        if (window == null || window.windowIndex != windowIndex) {
            windows.put(ownerId, new Window(windowIndex, 1));
            return true;
        }
        if (window.count >= maxPerSecond) return false;
        window.count++;
        return true;
    }

    private static final class Window {
        private final long windowIndex;
        private int count;
        private Window(long windowIndex, int count) { this.windowIndex = windowIndex; this.count = count; }
    }
}
