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

/**
 * Bounded Black Arcana-owned propagation frontier. It never loads chunks and never invokes
 * vanilla fire/random-tick propagation.
 */
public final class BlackPyreFrontierScheduler {
    private final int maxFrontiers;
    private final int maxCellsPerFrontier;
    private final int spreadPerTick;
    private final int radiusBlocks;
    private final long lifetimeTicks;
    private final Map<UUID, Frontier> frontiers = new LinkedHashMap<>();

    public BlackPyreFrontierScheduler(
        int maxFrontiers,
        int maxCellsPerFrontier,
        int spreadPerTick,
        int radiusBlocks,
        long lifetimeTicks
    ) {
        if (maxFrontiers <= 0 || maxFrontiers > BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS) {
            throw new IllegalArgumentException("maxFrontiers outside safety ceiling");
        }
        if (maxCellsPerFrontier <= 0 || maxCellsPerFrontier > BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER) {
            throw new IllegalArgumentException("maxCellsPerFrontier outside safety ceiling");
        }
        if (spreadPerTick <= 0 || spreadPerTick > BlackPyreSafetyCeilings.MAX_SPREAD_PER_TICK) {
            throw new IllegalArgumentException("spreadPerTick outside safety ceiling");
        }
        if (radiusBlocks <= 0 || radiusBlocks > BlackPyreSafetyCeilings.MAX_RADIUS_BLOCKS) {
            throw new IllegalArgumentException("radiusBlocks outside safety ceiling");
        }
        if (lifetimeTicks <= 0 || lifetimeTicks > BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS) {
            throw new IllegalArgumentException("lifetimeTicks outside safety ceiling");
        }
        this.maxFrontiers = maxFrontiers;
        this.maxCellsPerFrontier = maxCellsPerFrontier;
        this.spreadPerTick = spreadPerTick;
        this.radiusBlocks = radiusBlocks;
        this.lifetimeTicks = lifetimeTicks;
    }

    public synchronized boolean start(UUID frontierId, BlackPyreCell seed, long startedAtTick) {
        Objects.requireNonNull(frontierId, "frontierId");
        Objects.requireNonNull(seed, "seed");
        if (startedAtTick < 0L) throw new IllegalArgumentException("startedAtTick cannot be negative");
        if (frontiers.containsKey(frontierId) || frontiers.size() >= maxFrontiers) return false;
        Frontier frontier = new Frontier(seed, startedAtTick);
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
            if (!eligible(frontier.seed, cell)) continue;
            if (frontier.seen.add(cell)) {
                frontier.pending.addLast(cell);
                accepted++;
            }
        }
        return accepted;
    }

    /**
     * Processes at most the configured per-tick candidate budget. Unloaded cells are removed from
     * the pending queue and intentionally dropped, never retained as deferred chunk-load work.
     */
    public synchronized List<BlackPyreCell> tick(
        UUID frontierId,
        long nowTick,
        Predicate<BlackPyreCell> loaded
    ) {
        Objects.requireNonNull(frontierId, "frontierId");
        Objects.requireNonNull(loaded, "loaded");
        Frontier frontier = frontiers.get(frontierId);
        if (frontier == null) return List.of();
        if (nowTick < frontier.startedAtTick || nowTick - frontier.startedAtTick >= lifetimeTicks) {
            frontiers.remove(frontierId);
            return List.of();
        }

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

    public synchronized void clear() {
        frontiers.clear();
    }

    public synchronized int activeFrontiers() {
        return frontiers.size();
    }

    /** Read-only queue visibility for lifecycle cleanup; absent frontiers report zero. */
    public synchronized int pendingCells(UUID frontierId) {
        Objects.requireNonNull(frontierId, "frontierId");
        Frontier frontier = frontiers.get(frontierId);
        return frontier == null ? 0 : frontier.pending.size();
    }

    public synchronized int seenCells(UUID frontierId) {
        Frontier frontier = frontiers.get(frontierId);
        return frontier == null ? 0 : frontier.seen.size();
    }

    private boolean eligible(BlackPyreCell seed, BlackPyreCell candidate) {
        if (!seed.dimensionId().equals(candidate.dimensionId())) return false;
        long dx = (long) candidate.x() - seed.x();
        long dy = (long) candidate.y() - seed.y();
        long dz = (long) candidate.z() - seed.z();
        if (Math.abs(dx) > radiusBlocks || Math.abs(dy) > radiusBlocks || Math.abs(dz) > radiusBlocks) {
            return false;
        }
        long radiusSquared = (long) radiusBlocks * radiusBlocks;
        return dx * dx + dy * dy + dz * dz <= radiusSquared;
    }

    private static final class Frontier {
        final BlackPyreCell seed;
        final long startedAtTick;
        final LinkedHashSet<BlackPyreCell> seen = new LinkedHashSet<>();
        final ArrayDeque<BlackPyreCell> pending = new ArrayDeque<>();

        Frontier(BlackPyreCell seed, long startedAtTick) {
            this.seed = seed;
            this.startedAtTick = startedAtTick;
        }
    }
}
