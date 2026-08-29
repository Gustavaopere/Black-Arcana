package dev.gustavopere.blackarcana.core.hazard;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Bounded debt for delayed backlash whose caster is temporarily offline. */
public final class PendingBacklashRegistry {
    public static final int ABSOLUTE_MAX_PLAYERS = 65_536;
    public static final double ABSOLUTE_MAX_PENDING_PER_PLAYER = 100_000_000.0D;

    private final int maxPlayers;
    private final double maxPendingPerPlayer;
    private final Map<UUID, Double> pending = new LinkedHashMap<>();

    public PendingBacklashRegistry(int maxPlayers, double maxPendingPerPlayer) {
        if (maxPlayers <= 0 || maxPlayers > ABSOLUTE_MAX_PLAYERS) {
            throw new IllegalArgumentException("maxPlayers outside absolute bounds");
        }
        if (!Double.isFinite(maxPendingPerPlayer) || maxPendingPerPlayer <= 0.0D
            || maxPendingPerPlayer > ABSOLUTE_MAX_PENDING_PER_PLAYER) {
            throw new IllegalArgumentException("maxPendingPerPlayer outside absolute bounds");
        }
        this.maxPlayers = maxPlayers;
        this.maxPendingPerPlayer = maxPendingPerPlayer;
    }

    public synchronized boolean accrue(UUID playerId, double amount) {
        Objects.requireNonNull(playerId, "playerId");
        if (!Double.isFinite(amount) || amount < 0.0D) {
            throw new IllegalArgumentException("amount must be finite and non-negative");
        }
        if (amount == 0.0D) return true;
        Double current = pending.get(playerId);
        if (current == null && pending.size() >= maxPlayers) return false;
        double base = current == null ? 0.0D : current;
        double remaining = Math.max(0.0D, maxPendingPerPlayer - base);
        pending.put(playerId, base + Math.min(amount, remaining));
        return amount <= remaining;
    }

    public synchronized double drain(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        return pending.getOrDefault(playerId, 0.0D) == 0.0D
            ? removeZero(playerId)
            : pending.remove(playerId);
    }

    private double removeZero(UUID playerId) {
        pending.remove(playerId);
        return 0.0D;
    }

    public synchronized double pending(UUID playerId) {
        return pending.getOrDefault(Objects.requireNonNull(playerId, "playerId"), 0.0D);
    }

    public synchronized Map<UUID, Double> persistentSnapshot() {
        return Map.copyOf(pending);
    }

    public synchronized void restoreSnapshot(Map<UUID, Double> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        pending.clear();
        for (Map.Entry<UUID, Double> entry : snapshot.entrySet()) {
            if (pending.size() >= maxPlayers) break;
            UUID playerId = entry.getKey();
            Double amount = entry.getValue();
            if (playerId == null || amount == null || !Double.isFinite(amount) || amount <= 0.0D) continue;
            pending.put(playerId, Math.min(amount, maxPendingPerPlayer));
        }
    }

    public synchronized int size() {
        return pending.size();
    }
}
