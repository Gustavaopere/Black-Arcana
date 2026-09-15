package dev.gustavopere.blackarcana.core.cost;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Server-owned bounded registry for exact provider-native cost authorities. */
public final class ResourceCostProviderRegistry {
    private final int capacity;
    private final Map<String, ResourceCostProvider> providers = new LinkedHashMap<>();

    public ResourceCostProviderRegistry(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be positive");
        this.capacity = capacity;
    }

    public synchronized void register(ResourceCostProvider provider) {
        ResourceCostProvider checked = Objects.requireNonNull(provider, "provider");
        String resourceId = ResourceCostProvider.requireResourceId(checked.resourceId());
        if (providers.containsKey(resourceId)) {
            throw new IllegalArgumentException("duplicate resource cost provider: " + resourceId);
        }
        if (providers.size() >= capacity) {
            throw new IllegalStateException("resource cost provider registry capacity exceeded");
        }
        providers.put(resourceId, checked);
    }

    public synchronized Optional<ResourceCostProvider> resolve(String resourceId) {
        return Optional.ofNullable(providers.get(ResourceCostProvider.requireResourceId(resourceId)));
    }

    public synchronized int size() {
        return providers.size();
    }
}
