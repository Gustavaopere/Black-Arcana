package dev.gustavopere.blackarcana.content.souls;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-owned Mortal Ledger / Soul Anchor state. Credits and anchor consumption are synchronized
 * so one death transaction can consume at most one anchor.
 */
public final class SoulAnchorLedger {
    private final Policy policy;
    private final Map<UUID, State> states = new HashMap<>();

    public SoulAnchorLedger(Policy policy) {
        this.policy = Objects.requireNonNull(policy, "policy");
    }

    public synchronized CreditResult creditDeath(UUID ownerId, DeathCredit credit) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(credit, "credit");
        State state = stateFor(ownerId);
        if (!credit.eligible() || credit.antiFarmWeight() <= 0.0D || credit.baseSpiritValue() <= 0.0D) {
            return new CreditResult(false, 0.0D, state.storedSpiritValue);
        }
        if (state.recentDeathEvents.contains(credit.deathEventId())) {
            return new CreditResult(false, 0.0D, state.storedSpiritValue);
        }
        rememberEvent(state, credit.deathEventId());
        double awarded = credit.baseSpiritValue() * credit.antiFarmWeight();
        double before = state.storedSpiritValue;
        state.storedSpiritValue = Math.min(policy.maxStoredSpiritValue(), before + awarded);
        return new CreditResult(true, state.storedSpiritValue - before, state.storedSpiritValue);
    }

    public synchronized boolean formAnchor(UUID ownerId) {
        State state = stateFor(Objects.requireNonNull(ownerId, "ownerId"));
        if (state.anchors >= policy.maxAnchors() || state.storedSpiritValue < policy.spiritValuePerAnchor()) {
            return false;
        }
        state.storedSpiritValue -= policy.spiritValuePerAnchor();
        state.anchors++;
        return true;
    }

    public synchronized AnchorConsumeResult consumeForDeath(UUID ownerId, UUID deathEventId, long nowTick) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(deathEventId, "deathEventId");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        State state = states.get(ownerId);
        if (state == null || state.anchors <= 0) return AnchorConsumeResult.noAnchor();
        if (nowTick < state.recoveryUntilTick) return AnchorConsumeResult.locked(state.anchors, state.recoveryUntilTick);
        if (state.lastPreventedDeathEvent != null && state.lastPreventedDeathEvent.equals(deathEventId)) {
            return AnchorConsumeResult.duplicate(state.anchors, state.recoveryUntilTick);
        }
        state.anchors--;
        state.lastPreventedDeathEvent = deathEventId;
        state.recoveryUntilTick = saturatingAdd(nowTick, policy.recoveryLockoutTicks());
        return AnchorConsumeResult.consumed(state.anchors, state.recoveryUntilTick);
    }

    public synchronized Snapshot snapshot(UUID ownerId) {
        State state = states.get(Objects.requireNonNull(ownerId, "ownerId"));
        if (state == null) return new Snapshot(ownerId, 0.0D, 0, 0L);
        return new Snapshot(ownerId, state.storedSpiritValue, state.anchors, state.recoveryUntilTick);
    }

    public synchronized List<Snapshot> snapshotAll() {
        return states.entrySet().stream()
            .map(entry -> new Snapshot(entry.getKey(), entry.getValue().storedSpiritValue,
                entry.getValue().anchors, entry.getValue().recoveryUntilTick))
            .toList();
    }

    public synchronized void restore(List<Snapshot> snapshots) {
        Objects.requireNonNull(snapshots, "snapshots");
        if (snapshots.size() > policy.maxTrackedOwners()) {
            throw new IllegalArgumentException("soul anchor snapshot exceeds owner ceiling");
        }
        Map<UUID, State> replacement = new HashMap<>();
        for (Snapshot snapshot : snapshots) {
            Objects.requireNonNull(snapshot, "snapshot");
            if (replacement.containsKey(snapshot.ownerId())) {
                throw new IllegalArgumentException("duplicate soul anchor owner snapshot");
            }
            if (snapshot.anchors() > policy.maxAnchors() || snapshot.storedSpiritValue() > policy.maxStoredSpiritValue()) {
                throw new IllegalArgumentException("soul anchor snapshot exceeds configured bounds");
            }
            State state = new State();
            state.storedSpiritValue = snapshot.storedSpiritValue();
            state.anchors = snapshot.anchors();
            state.recoveryUntilTick = snapshot.recoveryUntilTick();
            replacement.put(snapshot.ownerId(), state);
        }
        states.clear();
        states.putAll(replacement);
    }

    private State stateFor(UUID ownerId) {
        State existing = states.get(ownerId);
        if (existing != null) return existing;
        if (states.size() >= policy.maxTrackedOwners()) {
            throw new IllegalStateException("soul anchor owner registry is full");
        }
        State created = new State();
        states.put(ownerId, created);
        return created;
    }

    private static void rememberEvent(State state, UUID eventId) {
        if (!state.recentDeathEvents.add(eventId)) return;
        state.deathEventOrder.addLast(eventId);
        while (state.deathEventOrder.size() > SoulSafetyCeilings.MAX_RECENT_DEATH_EVENTS_PER_OWNER) {
            UUID removed = state.deathEventOrder.removeFirst();
            state.recentDeathEvents.remove(removed);
        }
    }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    public record Policy(
        int maxAnchors,
        double spiritValuePerAnchor,
        double maxStoredSpiritValue,
        long recoveryLockoutTicks,
        int maxTrackedOwners
    ) {
        public Policy {
            if (maxAnchors <= 0 || maxAnchors > SoulSafetyCeilings.MAX_SOUL_ANCHORS) {
                throw new IllegalArgumentException("maxAnchors outside hard ceiling");
            }
            if (!Double.isFinite(spiritValuePerAnchor) || spiritValuePerAnchor <= 0.0D) {
                throw new IllegalArgumentException("spiritValuePerAnchor must be finite and positive");
            }
            if (!Double.isFinite(maxStoredSpiritValue) || maxStoredSpiritValue < spiritValuePerAnchor
                || maxStoredSpiritValue > 1_000_000.0D) {
                throw new IllegalArgumentException("maxStoredSpiritValue outside technical bounds");
            }
            if (recoveryLockoutTicks < SoulSafetyCeilings.MIN_RECOVERY_LOCKOUT_TICKS
                || recoveryLockoutTicks > 20L * 60L * 60L) {
                throw new IllegalArgumentException("recoveryLockoutTicks outside hard bounds");
            }
            if (maxTrackedOwners <= 0 || maxTrackedOwners > SoulSafetyCeilings.MAX_TRACKED_OWNERS) {
                throw new IllegalArgumentException("maxTrackedOwners outside hard ceiling");
            }
        }
    }

    public record DeathCredit(UUID deathEventId, double baseSpiritValue, double antiFarmWeight, boolean eligible) {
        public DeathCredit {
            Objects.requireNonNull(deathEventId, "deathEventId");
            if (!Double.isFinite(baseSpiritValue) || baseSpiritValue < 0.0D) throw new IllegalArgumentException("baseSpiritValue invalid");
            if (!Double.isFinite(antiFarmWeight) || antiFarmWeight < 0.0D || antiFarmWeight > 1.0D) {
                throw new IllegalArgumentException("antiFarmWeight must be in [0,1]");
            }
        }
    }

    public record CreditResult(boolean credited, double awarded, double storedAfter) { }

    public record Snapshot(UUID ownerId, double storedSpiritValue, int anchors, long recoveryUntilTick) {
        public Snapshot {
            Objects.requireNonNull(ownerId, "ownerId");
            if (!Double.isFinite(storedSpiritValue) || storedSpiritValue < 0.0D) throw new IllegalArgumentException("storedSpiritValue invalid");
            if (anchors < 0 || anchors > SoulSafetyCeilings.MAX_SOUL_ANCHORS) throw new IllegalArgumentException("anchors invalid");
            if (recoveryUntilTick < 0L) throw new IllegalArgumentException("recoveryUntilTick invalid");
        }
    }

    public record AnchorConsumeResult(Status status, int anchorsRemaining, long recoveryUntilTick) {
        public enum Status { CONSUMED, NO_ANCHOR, RECOVERY_LOCKED, DUPLICATE_EVENT }
        public boolean consumed() { return status == Status.CONSUMED; }
        static AnchorConsumeResult consumed(int anchors, long recovery) { return new AnchorConsumeResult(Status.CONSUMED, anchors, recovery); }
        static AnchorConsumeResult noAnchor() { return new AnchorConsumeResult(Status.NO_ANCHOR, 0, 0L); }
        static AnchorConsumeResult locked(int anchors, long recovery) { return new AnchorConsumeResult(Status.RECOVERY_LOCKED, anchors, recovery); }
        static AnchorConsumeResult duplicate(int anchors, long recovery) { return new AnchorConsumeResult(Status.DUPLICATE_EVENT, anchors, recovery); }
    }

    private static final class State {
        private double storedSpiritValue;
        private int anchors;
        private long recoveryUntilTick;
        private UUID lastPreventedDeathEvent;
        private final Set<UUID> recentDeathEvents = new HashSet<>();
        private final Deque<UUID> deathEventOrder = new ArrayDeque<>();
    }
}
