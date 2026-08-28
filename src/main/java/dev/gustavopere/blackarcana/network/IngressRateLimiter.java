package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

public final class IngressRateLimiter {
    private final int maxRequestsPerWindow;
    private final long windowTicks;
    private final int maxTrackedCasters;
    private final Map<UUID, ArrayDeque<Long>> requests = new HashMap<>();

    public IngressRateLimiter(int maxRequestsPerWindow, long windowTicks, int maxTrackedCasters) {
        if (maxRequestsPerWindow <= 0) throw new IllegalArgumentException("maxRequestsPerWindow must be positive");
        if (windowTicks <= 0L) throw new IllegalArgumentException("windowTicks must be positive");
        if (maxTrackedCasters <= 0) throw new IllegalArgumentException("maxTrackedCasters must be positive");
        this.maxRequestsPerWindow = maxRequestsPerWindow;
        this.windowTicks = windowTicks;
        this.maxTrackedCasters = maxTrackedCasters;
    }

    public synchronized ArcanaDecision claim(UUID casterId, long serverTick) {
        Objects.requireNonNull(casterId, "casterId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        prune(serverTick);

        ArrayDeque<Long> history = requests.get(casterId);
        if (history == null) {
            if (requests.size() >= maxTrackedCasters) {
                return ArcanaDecision.deny("ingress_limiter_saturated", "too many active caster rate-limit buckets");
            }
            history = new ArrayDeque<>();
            requests.put(casterId, history);
        }

        Long last = history.peekLast();
        if (last != null && serverTick < last) {
            return ArcanaDecision.deny("clock_regression", "server tick moved backwards for caster rate limit");
        }
        if (history.size() >= maxRequestsPerWindow) {
            return ArcanaDecision.deny("rate_limited", "too many cast intents in the current window");
        }

        history.addLast(serverTick);
        return ArcanaDecision.allow();
    }

    public synchronized int trackedCasters() {
        return requests.size();
    }

    private void prune(long now) {
        Iterator<Map.Entry<UUID, ArrayDeque<Long>>> iterator = requests.entrySet().iterator();
        while (iterator.hasNext()) {
            ArrayDeque<Long> history = iterator.next().getValue();
            while (!history.isEmpty()) {
                long tick = history.peekFirst();
                if (now >= tick && now - tick >= windowTicks) history.removeFirst();
                else break;
            }
            if (history.isEmpty()) iterator.remove();
        }
    }
}
