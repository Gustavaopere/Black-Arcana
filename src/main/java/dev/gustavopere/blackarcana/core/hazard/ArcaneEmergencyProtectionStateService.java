package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.regex.Pattern;

/**
 * Bounded server-owned state for emergency protection resources.
 * Reservations are transient; only committed ready-at timestamps persist.
 */
public final class ArcaneEmergencyProtectionStateService {
    public static final int ABSOLUTE_MAX_STATES = 65_536;
    private static final Pattern RESOURCE_ID = Pattern.compile("[a-z0-9_.:/-]{1,128}");

    public record ResourceKey(UUID playerId, String resourceId) {
        public ResourceKey {
            Objects.requireNonNull(playerId, "playerId");
            requireResourceId(resourceId);
        }
    }

    public record PersistedState(long readyAtTick) {
        public PersistedState {
            if (readyAtTick < 0L) throw new IllegalArgumentException("readyAtTick cannot be negative");
        }
    }

    public interface Reservation {
        ArcanaDecision decision();
        void commit();
        void refund();
    }

    private final int maxStates;
    private final Map<ResourceKey, PersistedState> states = new LinkedHashMap<>();
    private final Set<ResourceKey> reservations = new HashSet<>();

    public ArcaneEmergencyProtectionStateService(int maxStates) {
        if (maxStates <= 0 || maxStates > ABSOLUTE_MAX_STATES) {
            throw new IllegalArgumentException("maxStates outside absolute bounds");
        }
        this.maxStates = maxStates;
    }

    public static ArcaneEmergencyProtectionStateService canonical(int maxStates) {
        return new ArcaneEmergencyProtectionStateService(maxStates);
    }

    public synchronized Reservation reserve(
        UUID playerId,
        String resourceId,
        long nowTick,
        long cooldownTicks
    ) {
        Objects.requireNonNull(playerId, "playerId");
        requireResourceId(resourceId);
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        if (cooldownTicks < 0L || cooldownTicks > ArcaneEmergencyProtectionSnapshot.ABSOLUTE_MAX_COOLDOWN_TICKS) {
            throw new IllegalArgumentException("cooldownTicks outside absolute bounds");
        }

        pruneReady(nowTick);
        ResourceKey key = new ResourceKey(playerId, resourceId);
        if (reservations.contains(key)) {
            return denied("emergency_resource_busy", "emergency protection resource is already reserved");
        }
        PersistedState current = states.get(key);
        if (current != null && current.readyAtTick() > nowTick) {
            return denied("emergency_resource_cooldown", "emergency protection resource is on cooldown");
        }
        if (!states.containsKey(key) && occupiedSlots() >= maxStates) {
            return denied("emergency_state_capacity", "emergency protection state capacity is exhausted");
        }
        reservations.add(key);
        return new ActiveReservation(key, nowTick, cooldownTicks);
    }

    public synchronized long readyAtTick(UUID playerId, String resourceId) {
        ResourceKey key = new ResourceKey(playerId, resourceId);
        PersistedState state = states.get(key);
        return state == null ? 0L : state.readyAtTick();
    }

    public synchronized Map<ResourceKey, PersistedState> persistentSnapshot() {
        return Map.copyOf(states);
    }

    public synchronized void restoreSnapshot(Map<ResourceKey, PersistedState> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        if (snapshot.size() > maxStates) throw new IllegalArgumentException("emergency snapshot exceeds capacity");
        Map<ResourceKey, PersistedState> validated = new HashMap<>();
        snapshot.forEach((key, value) -> {
            Objects.requireNonNull(key, "emergency resource key");
            Objects.requireNonNull(value, "emergency persisted state");
            if (validated.putIfAbsent(key, value) != null) {
                throw new IllegalArgumentException("duplicate emergency resource key");
            }
        });
        states.clear();
        states.putAll(validated);
        reservations.clear();
    }

    public synchronized int size() {
        return states.size();
    }

    private int occupiedSlots() {
        int occupied = states.size();
        for (ResourceKey key : reservations) {
            if (!states.containsKey(key)) occupied++;
        }
        return occupied;
    }

    private void pruneReady(long nowTick) {
        states.entrySet().removeIf(entry -> entry.getValue().readyAtTick() <= nowTick);
    }

    private static Reservation denied(String code, String detail) {
        ArcanaDecision decision = ArcanaDecision.deny(code, detail);
        return new Reservation() {
            @Override public ArcanaDecision decision() { return decision; }
            @Override public void commit() { }
            @Override public void refund() { }
        };
    }

    private final class ActiveReservation implements Reservation {
        private final ResourceKey key;
        private final long reservedAtTick;
        private final long cooldownTicks;
        private boolean terminal;

        private ActiveReservation(ResourceKey key, long reservedAtTick, long cooldownTicks) {
            this.key = key;
            this.reservedAtTick = reservedAtTick;
            this.cooldownTicks = cooldownTicks;
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public void commit() {
            synchronized (ArcaneEmergencyProtectionStateService.this) {
                if (terminal) return;
                terminal = true;
                reservations.remove(key);
                if (cooldownTicks == 0L) {
                    states.remove(key);
                    return;
                }
                states.put(key, new PersistedState(saturatingAdd(reservedAtTick, cooldownTicks)));
            }
        }

        @Override
        public void refund() {
            synchronized (ArcaneEmergencyProtectionStateService.this) {
                if (terminal) return;
                terminal = true;
                reservations.remove(key);
            }
        }
    }

    private static long saturatingAdd(long left, long right) {
        if (right > Long.MAX_VALUE - left) return Long.MAX_VALUE;
        return left + right;
    }

    private static void requireResourceId(String resourceId) {
        Objects.requireNonNull(resourceId, "resourceId");
        if (!RESOURCE_ID.matcher(resourceId).matches()) {
            throw new IllegalArgumentException("invalid emergency resource id: " + resourceId);
        }
    }
}
