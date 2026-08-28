package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Bounded, server-tick based mastery award admission.
 *
 * <p>The cast itself is never denied here. Only repetitive progression rewards are
 * suppressed. Repeating the same spell against the same meaningful target set in
 * the same dimension inside the configured window yields no additional mastery.</p>
 */
public final class MeaningfulMasteryAwardThrottle {
    public static final long DEFAULT_REPEAT_WINDOW_TICKS = 40L;
    public static final int DEFAULT_MAX_ENTRIES = 4_096;

    private final long repeatWindowTicks;
    private final int maxEntries;
    private final Map<Key, Long> lastAwards = new LinkedHashMap<>();

    public MeaningfulMasteryAwardThrottle() {
        this(DEFAULT_REPEAT_WINDOW_TICKS, DEFAULT_MAX_ENTRIES);
    }

    public MeaningfulMasteryAwardThrottle(long repeatWindowTicks, int maxEntries) {
        if (repeatWindowTicks < 0L || repeatWindowTicks > 20L * 60L * 60L) {
            throw new IllegalArgumentException("repeatWindowTicks outside bounded range");
        }
        if (maxEntries <= 0 || maxEntries > 65_536) {
            throw new IllegalArgumentException("maxEntries outside bounded range");
        }
        this.repeatWindowTicks = repeatWindowTicks;
        this.maxEntries = maxEntries;
    }

    public synchronized boolean allow(ArcanaCastRequest request, TargetResolution target) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        if (!target.resolved()) return false;

        long now = request.context().gameTick();
        prune(now);
        Key key = new Key(
            request.context().casterId(),
            request.spell().id().canonical(),
            request.context().dimensionId(),
            targetFingerprint(target));

        Long previous = lastAwards.get(key);
        if (previous != null && now >= previous && now - previous < repeatWindowTicks) {
            return false;
        }
        // A world/session tick reset must not lock progression forever.
        if (previous != null && now < previous) {
            lastAwards.remove(key);
        }
        if (!lastAwards.containsKey(key) && lastAwards.size() >= maxEntries) {
            return false;
        }
        lastAwards.put(key, now);
        return true;
    }

    public synchronized int size() {
        return lastAwards.size();
    }

    private void prune(long now) {
        if (repeatWindowTicks == 0L) {
            lastAwards.clear();
            return;
        }
        lastAwards.entrySet().removeIf(entry -> {
            long tick = entry.getValue();
            return now < tick || now - tick >= repeatWindowTicks;
        });
    }

    private static String targetFingerprint(TargetResolution target) {
        List<String> ids = new ArrayList<>(target.targetIds());
        ids.sort(Comparator.naturalOrder());
        return String.join("\u001f", ids);
    }

    private record Key(UUID casterId, String spellId, String dimensionId, String targetFingerprint) {
        private Key {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(dimensionId, "dimensionId");
            Objects.requireNonNull(targetFingerprint, "targetFingerprint");
        }
    }
}
