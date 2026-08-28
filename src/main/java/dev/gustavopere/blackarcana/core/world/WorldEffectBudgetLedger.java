package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Objects;

/** Bounded per-cast work ledger layered on top of the global per-tick scheduler. */
public final class WorldEffectBudgetLedger {
    private final int maxTrackedCasts;
    private final int maxUnitsPerCast;
    private final long maxIdleTicks;
    private final Map<ArcanaCastId, Entry> entries = new HashMap<>();

    public WorldEffectBudgetLedger(int maxTrackedCasts, int maxUnitsPerCast, long maxIdleTicks) {
        if (maxTrackedCasts <= 0) throw new IllegalArgumentException("maxTrackedCasts must be positive");
        if (maxUnitsPerCast <= 0 || maxUnitsPerCast > WorldEffectProfile.ABSOLUTE_MAX_AFFECTED_UNITS) {
            throw new IllegalArgumentException("maxUnitsPerCast outside absolute safety bounds");
        }
        if (maxIdleTicks <= 0) throw new IllegalArgumentException("maxIdleTicks must be positive");
        this.maxTrackedCasts = maxTrackedCasts;
        this.maxUnitsPerCast = maxUnitsPerCast;
        this.maxIdleTicks = maxIdleTicks;
    }

    public synchronized ArcanaDecision tryConsume(ArcanaCastId castId, int units, long nowTick) {
        Objects.requireNonNull(castId, "castId");
        if (units <= 0) return ArcanaDecision.deny("world_budget_units", "World work units must be positive");
        pruneIdle(nowTick);

        Entry current = entries.get(castId);
        if (current == null && entries.size() >= maxTrackedCasts) {
            return ArcanaDecision.deny("world_budget_capacity", "Too many active world-effect casts");
        }
        int used = current == null ? 0 : current.usedUnits();
        if ((long) used + units > maxUnitsPerCast) {
            return ArcanaDecision.deny("world_budget_exhausted", "World-effect cast exceeded its total work budget");
        }
        entries.put(castId, new Entry(used + units, nowTick));
        return ArcanaDecision.allow();
    }

    public synchronized void finish(ArcanaCastId castId) {
        entries.remove(Objects.requireNonNull(castId, "castId"));
    }

    public synchronized int trackedCasts() {
        return entries.size();
    }

    public synchronized int usedUnits(ArcanaCastId castId) {
        Entry entry = entries.get(Objects.requireNonNull(castId, "castId"));
        return entry == null ? 0 : entry.usedUnits();
    }

    public synchronized int pruneIdle(long nowTick) {
        int removed = 0;
        Iterator<Map.Entry<ArcanaCastId, Entry>> iterator = entries.entrySet().iterator();
        while (iterator.hasNext()) {
            Entry entry = iterator.next().getValue();
            if (nowTick - entry.lastTouchedTick() > maxIdleTicks) {
                iterator.remove();
                removed++;
            }
        }
        return removed;
    }

    private record Entry(int usedUnits, long lastTouchedTick) { }
}
