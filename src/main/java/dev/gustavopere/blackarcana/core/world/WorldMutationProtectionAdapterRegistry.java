package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/** Separate provider-neutral protection authority for exact block/world mutation cells. */
public final class WorldMutationProtectionAdapterRegistry {
    private final int maxAdapters;
    private final Map<String, WorldMutationProtectionAdapter> adapters = new LinkedHashMap<>();

    public WorldMutationProtectionAdapterRegistry(int maxAdapters) {
        if (maxAdapters <= 0 || maxAdapters > 32) {
            throw new IllegalArgumentException("maxAdapters must be between 1 and 32");
        }
        this.maxAdapters = maxAdapters;
    }

    public synchronized void register(String id, WorldMutationProtectionAdapter adapter) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(adapter, "adapter");
        if (id.isBlank() || id.length() > 64) {
            throw new IllegalArgumentException("adapter id must be non-blank and bounded");
        }
        if (adapters.containsKey(id)) {
            throw new IllegalStateException("duplicate world-mutation protection adapter: " + id);
        }
        if (adapters.size() >= maxAdapters) {
            throw new IllegalStateException("world-mutation protection adapter registry is full");
        }
        adapters.put(id, adapter);
    }

    public synchronized ArcanaDecision authorize(WorldMutationProtectionQuery query) {
        Objects.requireNonNull(query, "query");
        for (Map.Entry<String, WorldMutationProtectionAdapter> entry : adapters.entrySet()) {
            final ArcanaDecision decision;
            try {
                decision = Objects.requireNonNull(entry.getValue().authorize(query), "protection decision");
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny(
                    "world_mutation_protection_adapter_failed",
                    "World-mutation protection adapter failed closed: " + entry.getKey());
            }
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }

    public synchronized int size() {
        return adapters.size();
    }

    @FunctionalInterface
    public interface WorldMutationProtectionAdapter {
        ArcanaDecision authorize(WorldMutationProtectionQuery query);
    }
}
