package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardObserver;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSettledEvent;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;

/** Deterministic, exception-isolating post-settlement observer registry. */
public final class ArcaneHazardObserverRegistry {
    public static final int MAX_OBSERVERS = 64;
    private static final Pattern ID = Pattern.compile("[a-z0-9_.:-]{1,64}");
    private final Map<String, ArcaneHazardObserver> observers = new LinkedHashMap<>();

    public synchronized void register(String id, ArcaneHazardObserver observer) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(observer, "observer");
        if (!ID.matcher(id).matches()) throw new IllegalArgumentException("invalid hazard observer id: " + id);
        if (observers.containsKey(id)) throw new IllegalArgumentException("duplicate hazard observer: " + id);
        if (observers.size() >= MAX_OBSERVERS) throw new IllegalStateException("hazard observer registry is full");
        observers.put(id, observer);
    }

    public synchronized DispatchResult publish(ArcaneHazardSettledEvent event) {
        Objects.requireNonNull(event, "event");
        int delivered = 0;
        List<String> failures = new ArrayList<>();
        for (Map.Entry<String, ArcaneHazardObserver> entry : observers.entrySet()) {
            try {
                entry.getValue().onSettled(event);
                delivered++;
            } catch (RuntimeException | LinkageError failure) {
                failures.add(entry.getKey());
            }
        }
        return new DispatchResult(delivered, List.copyOf(failures));
    }

    public synchronized int size() { return observers.size(); }

    public record DispatchResult(int delivered, List<String> failedObserverIds) {
        public DispatchResult {
            if (delivered < 0) throw new IllegalArgumentException("delivered cannot be negative");
            failedObserverIds = List.copyOf(Objects.requireNonNull(failedObserverIds, "failedObserverIds"));
        }
    }
}
