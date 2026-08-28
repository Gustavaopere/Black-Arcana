package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

public final class PersistentCooldownService implements CooldownService {
    private final Function<ArcanaCastRequest, ArcanaCooldownSpec> policy;
    private final Map<CooldownKey, Entry> entries = new HashMap<>();

    public PersistentCooldownService(Function<ArcanaCastRequest, ArcanaCooldownSpec> policy) {
        this.policy = Objects.requireNonNull(policy, "policy");
    }

    @Override
    public synchronized ArcanaDecision check(ArcanaCastRequest request) {
        ArcanaCooldownSpec spec = requireSpec(request);
        if (spec.durationTicks() == 0L) return ArcanaDecision.allow();

        CooldownKey key = key(request, spec);
        Entry entry = entries.get(key);
        if (entry == null) return ArcanaDecision.allow();

        long configuredReadyAt = safeAdd(entry.startedAtTick(), spec.durationTicks());
        long effectiveReadyAt = Math.min(entry.readyAtTick(), configuredReadyAt);
        if (effectiveReadyAt != entry.readyAtTick()) {
            entry = new Entry(entry.startedAtTick(), effectiveReadyAt, spec.persistent());
            entries.put(key, entry);
        }

        long now = request.context().serverTick();
        if (now >= effectiveReadyAt) {
            entries.remove(key);
            return ArcanaDecision.allow();
        }

        return ArcanaDecision.deny("cooldown", "remaining_ticks=" + (effectiveReadyAt - now));
    }

    @Override
    public synchronized void start(ArcanaCastRequest request) {
        ArcanaCooldownSpec spec = requireSpec(request);
        if (spec.durationTicks() == 0L) return;

        long now = request.context().serverTick();
        entries.put(key(request, spec), new Entry(now, safeAdd(now, spec.durationTicks()), spec.persistent()));
    }

    public synchronized Map<CooldownKey, SnapshotEntry> persistentSnapshot(long now) {
        Map<CooldownKey, SnapshotEntry> snapshot = new HashMap<>();
        entries.forEach((key, entry) -> {
            if (entry.persistent() && entry.readyAtTick() > now) {
                snapshot.put(key, new SnapshotEntry(entry.startedAtTick(), entry.readyAtTick()));
            }
        });
        return Map.copyOf(snapshot);
    }

    /**
     * Returns a deterministic, bounded UI snapshot for one caster. Expired entries
     * for that caster are pruned as part of the read.
     */
    public synchronized Map<String, Long> remainingSnapshot(UUID casterId, long now, int maxEntries) {
        Objects.requireNonNull(casterId, "casterId");
        if (now < 0L) throw new IllegalArgumentException("now cannot be negative");
        if (maxEntries < 0) throw new IllegalArgumentException("maxEntries cannot be negative");

        entries.entrySet().removeIf(item -> item.getKey().casterId().equals(casterId) && item.getValue().readyAtTick() <= now);

        Map<String, Long> result = new LinkedHashMap<>();
        entries.entrySet().stream()
                .filter(item -> item.getKey().casterId().equals(casterId))
                .sorted(Map.Entry.comparingByKey(Comparator.comparing(CooldownKey::groupId)))
                .limit(maxEntries)
                .forEach(item -> result.put(
                        item.getKey().groupId(),
                        item.getValue().readyAtTick() - now));
        return Map.copyOf(result);
    }

    public synchronized void restorePersistentSnapshot(Map<CooldownKey, SnapshotEntry> snapshot, long now) {
        Objects.requireNonNull(snapshot, "snapshot");
        for (Map.Entry<CooldownKey, SnapshotEntry> item : snapshot.entrySet()) {
            CooldownKey key = Objects.requireNonNull(item.getKey(), "cooldown key");
            SnapshotEntry value = Objects.requireNonNull(item.getValue(), "cooldown entry");
            if (value.readyAtTick() > now) {
                entries.put(key, new Entry(value.startedAtTick(), value.readyAtTick(), true));
            }
        }
    }

    /** Renames active/restored groups before pruning removed groups. */
    public synchronized int migrateGroups(RuntimeGroupMigrations migrations) {
        Objects.requireNonNull(migrations, "migrations");
        if (migrations.isEmpty() || entries.isEmpty()) return 0;

        Map<CooldownKey, Entry> migrated = new HashMap<>();
        int renamed = 0;
        for (Map.Entry<CooldownKey, Entry> item : entries.entrySet()) {
            CooldownKey oldKey = item.getKey();
            String resolvedGroup = migrations.resolve(oldKey.groupId());
            if (!resolvedGroup.equals(oldKey.groupId())) renamed++;

            CooldownKey newKey = new CooldownKey(oldKey.casterId(), resolvedGroup);
            migrated.merge(newKey, item.getValue(), PersistentCooldownService::mergeRestrictively);
        }
        entries.clear();
        entries.putAll(migrated);
        return renamed;
    }

    /**
     * Removes persisted/runtime cooldown groups that no longer have an active server policy.
     * This is intentionally called only after all server initializers have registered policies.
     */
    public synchronized int pruneGroups(Set<String> activeGroupIds) {
        Set<String> active = validateGroups(activeGroupIds);
        int before = entries.size();
        entries.keySet().removeIf(key -> !active.contains(key.groupId()));
        return before - entries.size();
    }

    public synchronized int size() {
        return entries.size();
    }

    private ArcanaCooldownSpec requireSpec(ArcanaCastRequest request) {
        return Objects.requireNonNull(policy.apply(request), "cooldown spec");
    }

    private static CooldownKey key(ArcanaCastRequest request, ArcanaCooldownSpec spec) {
        return new CooldownKey(request.context().casterId(), spec.groupId());
    }

    private static Entry mergeRestrictively(Entry left, Entry right) {
        Entry later = left.readyAtTick() > right.readyAtTick()
                || (left.readyAtTick() == right.readyAtTick() && left.startedAtTick() >= right.startedAtTick())
                ? left
                : right;
        return new Entry(later.startedAtTick(), Math.max(left.readyAtTick(), right.readyAtTick()),
                left.persistent() || right.persistent());
    }

    private static Set<String> validateGroups(Set<String> groupIds) {
        Objects.requireNonNull(groupIds, "groupIds");
        Set<String> copy = Set.copyOf(groupIds);
        copy.forEach(ArcanaSpellId::parse);
        return copy;
    }

    private static long safeAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    public record CooldownKey(UUID casterId, String groupId) {
        public CooldownKey {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(groupId, "groupId");
            ArcanaSpellId.parse(groupId);
        }
    }

    public record SnapshotEntry(long startedAtTick, long readyAtTick) {
        public SnapshotEntry {
            if (startedAtTick < 0L) throw new IllegalArgumentException("startedAtTick cannot be negative");
            if (readyAtTick < startedAtTick) throw new IllegalArgumentException("readyAtTick cannot precede startedAtTick");
        }
    }

    private record Entry(long startedAtTick, long readyAtTick, boolean persistent) { }
}
