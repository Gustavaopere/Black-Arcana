package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;

import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Bounded identity tracker for short-lived platform damage-source tokens.
 * Identity semantics are intentional: provenance belongs to one exact damage attempt/source object.
 */
public final class ArcaneDamageProvenanceTracker<T> {
    public static final int ABSOLUTE_MAX_TRACKED = 65_536;

    private final int maxTracked;
    private final Map<T, ArcanaDamageProvenance> tracked = new IdentityHashMap<>();

    public ArcaneDamageProvenanceTracker(int maxTracked) {
        if (maxTracked <= 0 || maxTracked > ABSOLUTE_MAX_TRACKED) {
            throw new IllegalArgumentException("maxTracked outside absolute bounds");
        }
        this.maxTracked = maxTracked;
    }

    public synchronized boolean register(T token, ArcanaDamageProvenance provenance) {
        Objects.requireNonNull(token, "token");
        Objects.requireNonNull(provenance, "provenance");
        if (tracked.containsKey(token) || tracked.size() >= maxTracked) return false;
        tracked.put(token, provenance);
        return true;
    }

    public synchronized Optional<ArcanaDamageProvenance> find(T token) {
        return Optional.ofNullable(tracked.get(Objects.requireNonNull(token, "token")));
    }

    public synchronized Optional<ArcanaDamageProvenance> release(T token) {
        return Optional.ofNullable(tracked.remove(Objects.requireNonNull(token, "token")));
    }

    public synchronized int size() {
        return tracked.size();
    }
}
