package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/** Extension point for claim/protection mods without embedding any provider in core. */
public final class ProtectionAdapterRegistry {
    private final int maxAdapters;
    private final Map<String, ProtectionAdapter> adapters = new LinkedHashMap<>();

    public ProtectionAdapterRegistry(int maxAdapters) {
        if (maxAdapters <= 0 || maxAdapters > 32) throw new IllegalArgumentException("maxAdapters must be between 1 and 32");
        this.maxAdapters = maxAdapters;
    }

    public synchronized void register(String id, ProtectionAdapter adapter) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(adapter, "adapter");
        if (id.isBlank() || id.length() > 64) throw new IllegalArgumentException("adapter id must be non-blank and bounded");
        if (adapters.containsKey(id)) throw new IllegalStateException("duplicate protection adapter: " + id);
        if (adapters.size() >= maxAdapters) throw new IllegalStateException("protection adapter registry is full");
        adapters.put(id, adapter);
    }

    public synchronized ArcanaDecision authorize(ProtectionQuery query) {
        Objects.requireNonNull(query, "query");
        for (Map.Entry<String, ProtectionAdapter> entry : adapters.entrySet()) {
            final ArcanaDecision decision;
            try {
                decision = Objects.requireNonNull(entry.getValue().authorize(query), "protection decision");
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny(
                    "protection_adapter_failed",
                    "Protection adapter failed closed: " + entry.getKey());
            }
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }

    @FunctionalInterface
    public interface ProtectionAdapter {
        ArcanaDecision authorize(ProtectionQuery query);
    }
}
