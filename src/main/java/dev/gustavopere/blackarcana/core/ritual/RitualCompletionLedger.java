package dev.gustavopere.blackarcana.core.ritual;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Bounded durable ledger used to make ritual rewards idempotent across retries/restarts. */
public final class RitualCompletionLedger {
    public static final int ABSOLUTE_MAX_COMPLETIONS = 65_536;

    private final int maxEntries;
    private final Map<RitualCompletionKey, Long> completedAt = new LinkedHashMap<>();

    public RitualCompletionLedger(int maxEntries) {
        if (maxEntries <= 0 || maxEntries > ABSOLUTE_MAX_COMPLETIONS) {
            throw new IllegalArgumentException("maxEntries outside ritual completion bounds");
        }
        this.maxEntries = maxEntries;
    }

    public synchronized CompletionResult complete(RitualCompletionKey key, long nowTick) {
        Objects.requireNonNull(key, "key");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        if (completedAt.containsKey(key)) return CompletionResult.ALREADY_COMPLETED;
        if (completedAt.size() >= maxEntries) return CompletionResult.CAPACITY_EXCEEDED;
        completedAt.put(key, nowTick);
        return CompletionResult.RECORDED;
    }

    public synchronized boolean contains(RitualCompletionKey key) {
        return completedAt.containsKey(Objects.requireNonNull(key, "key"));
    }

    public synchronized int size() {
        return completedAt.size();
    }

    public synchronized List<SnapshotEntry> snapshot(int limit) {
        if (limit <= 0) return List.of();
        int count = Math.min(Math.min(limit, maxEntries), completedAt.size());
        List<SnapshotEntry> result = new ArrayList<>(count);
        for (Map.Entry<RitualCompletionKey, Long> entry : completedAt.entrySet()) {
            if (result.size() >= count) break;
            result.add(new SnapshotEntry(entry.getKey(), entry.getValue()));
        }
        return List.copyOf(result);
    }

    public synchronized RestoreResult restore(List<SnapshotEntry> entries) {
        Objects.requireNonNull(entries, "entries");
        completedAt.clear();
        int restored = 0;
        int rejected = 0;
        for (SnapshotEntry entry : entries) {
            if (entry == null || entry.completedAtTick() < 0L) {
                rejected++;
                continue;
            }
            if (completedAt.containsKey(entry.key())) {
                rejected++;
                continue;
            }
            if (completedAt.size() >= maxEntries) {
                rejected += entries.size() - restored - rejected;
                break;
            }
            completedAt.put(entry.key(), entry.completedAtTick());
            restored++;
        }
        return new RestoreResult(restored, rejected);
    }

    public enum CompletionResult {
        RECORDED,
        ALREADY_COMPLETED,
        CAPACITY_EXCEEDED
    }

    public record SnapshotEntry(RitualCompletionKey key, long completedAtTick) {
        public SnapshotEntry {
            Objects.requireNonNull(key, "key");
            if (completedAtTick < 0L) throw new IllegalArgumentException("completedAtTick cannot be negative");
        }
    }

    public record RestoreResult(int restored, int rejected) {
        public RestoreResult {
            if (restored < 0 || rejected < 0) throw new IllegalArgumentException("restore counts cannot be negative");
        }
    }
}
