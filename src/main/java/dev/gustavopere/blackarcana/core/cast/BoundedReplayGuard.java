package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.ReplayGuard;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

public final class BoundedReplayGuard implements ReplayGuard {
    private final int maxEntries;
    private final long retentionTicks;
    private final LinkedHashMap<ArcanaCastId, Long> claimed = new LinkedHashMap<>();

    public BoundedReplayGuard(int maxEntries, long retentionTicks) {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries must be positive");
        if (retentionTicks <= 0L) throw new IllegalArgumentException("retentionTicks must be positive");
        this.maxEntries = maxEntries;
        this.retentionTicks = retentionTicks;
    }

    @Override
    public synchronized ArcanaDecision claim(ArcanaCastRequest request) {
        long now = request.context().serverTick();
        prune(now);

        if (claimed.containsKey(request.castId())) {
            return ArcanaDecision.deny("duplicate_cast", "cast id has already been claimed");
        }
        if (claimed.size() >= maxEntries) {
            return ArcanaDecision.deny("replay_guard_saturated", "replay guard reached its bounded capacity");
        }

        claimed.put(request.castId(), now);
        return ArcanaDecision.allow();
    }

    public synchronized int size() {
        return claimed.size();
    }

    private void prune(long now) {
        Iterator<Map.Entry<ArcanaCastId, Long>> iterator = claimed.entrySet().iterator();
        while (iterator.hasNext()) {
            long claimedAt = iterator.next().getValue();
            if (now >= claimedAt && now - claimedAt > retentionTicks) {
                iterator.remove();
            }
        }
    }
}
