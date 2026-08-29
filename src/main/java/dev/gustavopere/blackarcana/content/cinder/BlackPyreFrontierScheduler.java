package dev.gustavopere.blackarcana.content.cinder;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;
import java.util.function.Predicate;

/** Bounded frontier only; it never loads chunks and never invokes vanilla fire spread. */
public final class BlackPyreFrontierScheduler {
    private final int maxFrontiers;
    private final int maxCellsPerFrontier;
    private final int spreadPerTick;
    private final Map<UUID, Frontier> frontiers = new LinkedHashMap<>();

    public BlackPyreFrontierScheduler(int maxFrontiers, int maxCellsPerFrontier, int spreadPerTick) {
        if (maxFrontiers <= 0 || maxFrontiers > BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS) {
            throw new IllegalArgumentException("maxFrontiers outside safety ceiling");
        }
        if (maxCellsPerFrontier <= 0 || maxCellsPerFrontier > BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER) {
            throw new IllegalArgumentException("maxCellsPerFrontier outside safety ceiling");
        }
        if (spreadPerTick <= 0 || spreadPerTick > BlackPyreSafetyCeilings.MAX_SPREAD_PER_TICK) {
            throw new IllegalArgumentException("spreadPerTick outside safety ceiling");
        }
        this.maxFrontiers = maxFrontiers;
        this.maxCellsPerFrontier = maxCellsPerFrontier;
        this.spreadPerTick = spreadPerTick;
    }

    public synchronized boolean start(UUID frontierId, BlackPyreCell seed) {
        Objects.requireNonNull(frontierId, "frontierId");
        Objects.requireNonNull(seed, "seed");
        if (frontiers.containsKey(frontierId) || frontiers.size() >= maxFrontiers) return false;
        Frontier frontier = new Frontier();
        frontier.seen.add(seed);
        frontier.pending.add(seed);
        frontiers.put(frontierId, frontier);
        return true;
    }

    public synchronized int offer(UUID frontierId, Collection<BlackPyreCell> candidates) {
        Objects.requireNonNull(frontierId, "frontierId");
        Objects.requireNonNull(candidates, "candidates");
        Frontier frontier = frontiers.get(frontierId);
        if (frontier == null) return 0;
        int accepted = 0;
        for (BlackPyreCell cell : candidates) {
            Objects.requireNonNull(cell, "candidate");
            if (frontier.seen.size() >= maxCellsPerFrontier) break;
            if (frontier.seen.add(cell)) {
                frontier.pending.add(cell);
                accepted++;
            }
        }
        return accepted;
    }

    /** Processes at most spreadPerTick candidates. Unloaded cells are dropped, never retained as chunk-load requests. */
    public synchronized List<BlackPyreCell> tick(UUID frontierId, Predicate<BlackPyreCell> loaded) {
        Objects.requireNonNull(frontierId, "frontierId");
        Objects.requireNonNull(loaded, "loaded");
        Frontier frontier = frontiers.get(frontierId);
        if (frontier == null) return List.of();
        List<BlackPyreCell> admitted = new ArrayList<>(spreadPerTick);
        int processed = 0;
        while (!frontier.pending.isEmpty() && processed < spreadPerTick) {
            BlackPyreCell cell = frontier.pending.removeFirst();
            processed++;
            if (loaded.test(cell)) admitted.add(cell);
        }
        return List.copyOf(admitted);
    }

    public synchronized void finish(UUID frontierId) {
        frontiers.remove(Objects.requireNonNull(frontierId, "frontierId"));
    }

    public synchronized int activeFrontiers() { return frontiers.size(); }
    public synchronized int seenCells(UUID frontierId) {
        Frontier frontier = frontiers.get(frontierId);
        return frontier == null ? 0 : frontier.seen.size();
    }

    private static final class Frontier {
        final LinkedHashSet<BlackPyreCell> seen = new LinkedHashSet<>();
        final ArrayDeque<BlackPyreCell> pending = new ArrayDeque<>();
    }
}
