package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

public final class RitualActivationGuard {
    private final int maxTrackedActivations;
    private final long retentionTicks;
    private final Map<RitualActivationId, Long> claimed = new LinkedHashMap<>();

    public RitualActivationGuard(int maxTrackedActivations, long retentionTicks) {
        if (maxTrackedActivations <= 0 || maxTrackedActivations > 65_536) {
            throw new IllegalArgumentException("maxTrackedActivations outside bounds");
        }
        if (retentionTicks <= 0L) throw new IllegalArgumentException("retentionTicks must be positive");
        this.maxTrackedActivations = maxTrackedActivations;
        this.retentionTicks = retentionTicks;
    }

    public synchronized ArcanaDecision claim(RitualActivationId activationId, long nowTick) {
        Objects.requireNonNull(activationId, "activationId");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        prune(nowTick);
        if (claimed.containsKey(activationId)) {
            return ArcanaDecision.deny("ritual_activation_replay", "ritual activation id was already claimed");
        }
        if (claimed.size() >= maxTrackedActivations) {
            return ArcanaDecision.deny("ritual_activation_guard_saturated", "ritual activation guard is full");
        }
        claimed.put(activationId, nowTick);
        return ArcanaDecision.allow();
    }

    public synchronized boolean remember(RitualActivationId activationId, long claimedAtTick, long nowTick) {
        Objects.requireNonNull(activationId, "activationId");
        if (claimedAtTick < 0L || nowTick < 0L) return false;
        prune(nowTick);
        Long existing = claimed.get(activationId);
        if (existing != null) return existing == claimedAtTick;
        if (claimed.size() >= maxTrackedActivations) return false;
        claimed.put(activationId, claimedAtTick);
        return true;
    }

    private void prune(long nowTick) {
        Iterator<Map.Entry<RitualActivationId, Long>> iterator = claimed.entrySet().iterator();
        while (iterator.hasNext()) {
            long tick = iterator.next().getValue();
            if (nowTick >= tick && nowTick - tick >= retentionTicks) iterator.remove();
        }
    }
}
