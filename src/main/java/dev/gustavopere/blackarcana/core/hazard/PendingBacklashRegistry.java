package dev.gustavopere.blackarcana.core.hazard;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Bounded debt for delayed backlash whose caster is temporarily offline. */
public final class PendingBacklashRegistry {
    public static final int ABSOLUTE_MAX_PLAYERS = 65_536;
    public static final int ABSOLUTE_MAX_DEBTS_PER_PLAYER = 1_024;
    public static final double ABSOLUTE_MAX_PENDING_PER_PLAYER = 100_000_000.0D;

    private static final class DebtQueue {
        private final List<PendingBacklashDebt> debts = new ArrayList<>();
        private double total;
    }

    private final int maxPlayers;
    private final double maxPendingPerPlayer;
    private final Map<UUID, DebtQueue> pending = new LinkedHashMap<>();

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

    /** Backward-compatible aggregate debt path. Legacy debt is intentionally unprotected. */
    public synchronized boolean accrue(UUID playerId, double amount) {
        Objects.requireNonNull(playerId, "playerId");
        if (!Double.isFinite(amount) || amount < 0.0D) {
            throw new IllegalArgumentException("amount must be finite and non-negative");
        }
        if (amount == 0.0D) return true;
        return accrue(playerId, PendingBacklashDebt.legacy(
            Math.min(amount, ABSOLUTE_MAX_PENDING_PER_PLAYER)))
            && amount <= ABSOLUTE_MAX_PENDING_PER_PLAYER;
    }

    /**
     * Records one causal debt without aggregating it with debts from other damage identities.
     * If the amount ceiling is crossed, the final debt is clamped but retains its own context.
     */
    public synchronized boolean accrue(UUID playerId, PendingBacklashDebt debt) {
        Objects.requireNonNull(playerId, "playerId");
        Objects.requireNonNull(debt, "debt");

        DebtQueue queue = pending.get(playerId);
        if (queue == null) {
            if (pending.size() >= maxPlayers) return false;
            queue = new DebtQueue();
            pending.put(playerId, queue);
        }
        if (queue.debts.size() >= ABSOLUTE_MAX_DEBTS_PER_PLAYER) return false;

        double remaining = Math.max(0.0D, maxPendingPerPlayer - queue.total);
        if (remaining <= 0.0D) return false;
        double recordedAmount = Math.min(debt.amount(), remaining);
        queue.debts.add(debt.withAmount(recordedAmount));
        queue.total += recordedAmount;
        return debt.amount() <= remaining;
    }

    /** Legacy aggregate drain retained for callers that do not understand causal debt. */
    public synchronized double drain(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        DebtQueue removed = pending.remove(playerId);
        return removed == null ? 0.0D : removed.total;
    }

    /** Removes and returns each causal debt in deterministic insertion order. */
    public synchronized List<PendingBacklashDebt> drainDebts(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        DebtQueue removed = pending.remove(playerId);
        return removed == null ? List.of() : List.copyOf(removed.debts);
    }

    public synchronized double pending(UUID playerId) {
        DebtQueue queue = pending.get(Objects.requireNonNull(playerId, "playerId"));
        return queue == null ? 0.0D : queue.total;
    }

    /**
     * Backward-compatible aggregate snapshot. New persistence should use
     * {@link #persistentDebtsSnapshot()} so causal emergency context is not lost.
     */
    public synchronized Map<UUID, Double> persistentSnapshot() {
        LinkedHashMap<UUID, Double> snapshot = new LinkedHashMap<>();
        pending.forEach((playerId, queue) -> snapshot.put(playerId, queue.total));
        return Map.copyOf(snapshot);
    }

    /** Deep immutable snapshot preserving causal debt entries. */
    public synchronized Map<UUID, List<PendingBacklashDebt>> persistentDebtsSnapshot() {
        LinkedHashMap<UUID, List<PendingBacklashDebt>> snapshot = new LinkedHashMap<>();
        pending.forEach((playerId, queue) -> snapshot.put(playerId, List.copyOf(queue.debts)));
        return Map.copyOf(snapshot);
    }

    /** Restores legacy aggregate saves as explicitly unprotected debt. */
    public synchronized void restoreSnapshot(Map<UUID, Double> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        pending.clear();
        for (Map.Entry<UUID, Double> entry : snapshot.entrySet()) {
            if (pending.size() >= maxPlayers) break;
            UUID playerId = entry.getKey();
            Double amount = entry.getValue();
            if (playerId == null || amount == null || !Double.isFinite(amount) || amount <= 0.0D) continue;
            double bounded = Math.min(amount, Math.min(maxPendingPerPlayer, ABSOLUTE_MAX_PENDING_PER_PLAYER));
            accrue(playerId, PendingBacklashDebt.legacy(bounded));
        }
    }

    /** Restores structured saves while honoring all runtime safety ceilings. */
    public synchronized void restoreDebtsSnapshot(Map<UUID, List<PendingBacklashDebt>> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        pending.clear();
        for (Map.Entry<UUID, List<PendingBacklashDebt>> entry : snapshot.entrySet()) {
            if (pending.size() >= maxPlayers) break;
            UUID playerId = entry.getKey();
            List<PendingBacklashDebt> debts = entry.getValue();
            if (playerId == null || debts == null) continue;
            int count = Math.min(debts.size(), ABSOLUTE_MAX_DEBTS_PER_PLAYER);
            for (int i = 0; i < count; i++) {
                PendingBacklashDebt debt = debts.get(i);
                if (debt == null) continue;
                double remaining = maxPendingPerPlayer - pending(playerId);
                if (remaining <= 0.0D) break;
                accrue(playerId, debt);
            }
        }
    }

    public synchronized int size() {
        return pending.size();
    }
}
