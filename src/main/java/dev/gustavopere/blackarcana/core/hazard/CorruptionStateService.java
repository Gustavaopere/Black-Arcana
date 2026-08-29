package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.CorruptionAcquisitionProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionBand;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSnapshot;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.regex.Pattern;

/** Event-driven, bounded persistent corruption state. No global tick scan is required. */
public final class CorruptionStateService {
    public static final int STATE_SCHEMA_VERSION = 1;
    public static final int ABSOLUTE_MAX_TRACKED_PLAYERS = 65_536;
    public static final int ABSOLUTE_MAX_LISTENERS = 32;
    public static final double CANONICAL_MAX_CORRUPTION_UNITS = 1_000.0D;
    public static final double ABSOLUTE_MAX_CORRUPTION_UNITS = 1_000_000.0D;
    public static final long MAX_TELEMETRY_EVENTS = 1_000_000_000L;
    private static final Pattern LISTENER_ID = Pattern.compile("[a-z0-9_.:-]{1,64}");

    private final int maxTrackedPlayers;
    private final int maxListeners;
    private final double maxCorruptionUnits;
    private final CorruptionThresholds thresholds;
    private final Map<UUID, MutableState> states = new LinkedHashMap<>();
    private final Set<UUID> reservations = new LinkedHashSet<>();
    private final Map<String, CorruptionThresholdListener> listeners = new LinkedHashMap<>();

    public CorruptionStateService(
        int maxTrackedPlayers,
        double maxCorruptionUnits,
        CorruptionThresholds thresholds,
        int maxListeners
    ) {
        if (maxTrackedPlayers <= 0 || maxTrackedPlayers > ABSOLUTE_MAX_TRACKED_PLAYERS) {
            throw new IllegalArgumentException("maxTrackedPlayers outside absolute bounds");
        }
        if (!Double.isFinite(maxCorruptionUnits) || maxCorruptionUnits <= 0.0D
            || maxCorruptionUnits > ABSOLUTE_MAX_CORRUPTION_UNITS) {
            throw new IllegalArgumentException("maxCorruptionUnits outside absolute bounds");
        }
        if (maxListeners <= 0 || maxListeners > ABSOLUTE_MAX_LISTENERS) {
            throw new IllegalArgumentException("maxListeners outside absolute bounds");
        }
        this.maxTrackedPlayers = maxTrackedPlayers;
        this.maxCorruptionUnits = maxCorruptionUnits;
        this.thresholds = Objects.requireNonNull(thresholds, "thresholds");
        if (thresholds.critical() > maxCorruptionUnits) {
            throw new IllegalArgumentException("critical threshold cannot exceed max corruption units");
        }
        this.maxListeners = maxListeners;
    }

    public static CorruptionStateService canonical(int maxTrackedPlayers) {
        return new CorruptionStateService(
            maxTrackedPlayers,
            CANONICAL_MAX_CORRUPTION_UNITS,
            CorruptionThresholds.canonical(),
            ABSOLUTE_MAX_LISTENERS);
    }

    public synchronized void registerThresholdListener(String id, CorruptionThresholdListener listener) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(listener, "listener");
        if (!LISTENER_ID.matcher(id).matches()) throw new IllegalArgumentException("invalid corruption listener id: " + id);
        if (listeners.containsKey(id)) throw new IllegalArgumentException("duplicate corruption listener: " + id);
        if (listeners.size() >= maxListeners) throw new IllegalStateException("corruption listener registry is full");
        listeners.put(id, listener);
    }

    public synchronized CorruptionPreflight preflightCommittedCast(
        UUID playerId,
        long serverTick,
        CorruptionAcquisitionProfile profile,
        CorruptionResistanceSnapshot resistance
    ) {
        validatePlayerTick(playerId, serverTick);
        Objects.requireNonNull(profile, "profile");
        Objects.requireNonNull(resistance, "resistance");
        CorruptionSnapshot current = snapshotOf(states.get(playerId));
        double applied = appliedCorruption(
            current.units(),
            profile.baseCorruptionPerCommittedCast(),
            profile,
            resistance);
        return new CorruptionPreflight(current, applied);
    }

    /** Commits the immutable cast-time corruption snapshot without allowing post-preflight recovery to evade it. */
    public synchronized CorruptionUpdate commitPrepared(
        UUID playerId,
        long serverTick,
        CorruptionPreflight preflight
    ) {
        validatePlayerTick(playerId, serverTick);
        Objects.requireNonNull(preflight, "preflight");

        CorruptionSnapshot liveBefore = snapshotOf(states.get(playerId));
        double frozenFloor = preflight.current().units();
        double targetUnits = Math.min(
            maxCorruptionUnits,
            Math.max(liveBefore.units(), frozenFloor) + preflight.appliedCorruption());
        if (targetUnits <= liveBefore.units()) {
            return new CorruptionUpdate(liveBefore, liveBefore, 0.0D, List.of());
        }

        MutableState state = states.get(playerId);
        if (state == null) {
            ensureCapacityFor(playerId, "corruption state registry is full");
            state = new MutableState(0.0D, 0L, -1L, 0L, 0L);
            states.put(playerId, state);
        }
        state.units = targetUnits;
        state.lastMeaningfulUpdateTick = serverTick;
        if (preflight.appliedCorruption() > 0.0D) {
            state.acquisitionEvents = saturatingIncrement(Math.max(
                state.acquisitionEvents,
                preflight.current().acquisitionEvents()));
        }
        CorruptionSnapshot after = snapshotOf(state);
        List<CorruptionTransition> transitions = transitions(playerId, liveBefore, after, serverTick);
        publish(transitions);
        return new CorruptionUpdate(liveBefore, after, targetUnits - liveBefore.units(), transitions);
    }

    public synchronized CorruptionUpdate acquireFromCommittedCast(
        UUID playerId,
        long serverTick,
        CorruptionAcquisitionProfile profile,
        CorruptionResistanceSnapshot resistance
    ) {
        Objects.requireNonNull(profile, "profile");
        return acquire(playerId, serverTick, profile.baseCorruptionPerCommittedCast(), profile, resistance);
    }

    public synchronized CorruptionUpdate acquireFromEligibleDamage(
        UUID playerId,
        long serverTick,
        double confirmedDamage,
        CorruptionAcquisitionProfile profile,
        CorruptionResistanceSnapshot resistance
    ) {
        if (!Double.isFinite(confirmedDamage) || confirmedDamage < 0.0D) {
            throw new IllegalArgumentException("confirmedDamage must be finite and non-negative");
        }
        Objects.requireNonNull(profile, "profile");
        double raw = saturatingMultiply(confirmedDamage, profile.corruptionPerEligibleDamage());
        return acquire(playerId, serverTick, raw, profile, resistance);
    }

    public synchronized CorruptionUpdate recover(UUID playerId, long serverTick, double requestedUnits) {
        validatePlayerTick(playerId, serverTick);
        if (!Double.isFinite(requestedUnits) || requestedUnits < 0.0D) {
            throw new IllegalArgumentException("requestedUnits must be finite and non-negative");
        }
        MutableState state = states.get(playerId);
        CorruptionSnapshot before = snapshotOf(state);
        if (state == null || requestedUnits == 0.0D || before.units() == 0.0D) {
            return new CorruptionUpdate(before, before, 0.0D, List.of());
        }

        double recovered = Math.min(requestedUnits, state.units);
        state.units -= recovered;
        state.lastMeaningfulUpdateTick = serverTick;
        state.lastRecoveryTick = serverTick;
        state.recoveryEvents = saturatingIncrement(state.recoveryEvents);
        CorruptionSnapshot after = snapshotOf(state);
        List<CorruptionTransition> transitions = transitions(playerId, before, after, serverTick);
        publish(transitions);
        return new CorruptionUpdate(before, after, -recovered, transitions);
    }

    public synchronized CorruptionSnapshot snapshot(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        return snapshotOf(states.get(playerId));
    }

    /** Side-effect-free O(1) capacity probe used by cast preflight. */
    public synchronized boolean canReserve(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        return states.containsKey(playerId)
            || reservations.contains(playerId)
            || occupiedSlots() < maxTrackedPlayers;
    }

    /** Claims capacity for a terminal cast commit. Existing state consumes no additional slot. */
    public synchronized boolean reserve(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        if (reservations.contains(playerId)) return true;
        if (!states.containsKey(playerId) && occupiedSlots() >= maxTrackedPlayers) return false;
        reservations.add(playerId);
        return true;
    }

    public synchronized void releaseReservation(UUID playerId) {
        reservations.remove(Objects.requireNonNull(playerId, "playerId"));
    }

    public synchronized boolean contains(UUID playerId) {
        return states.containsKey(Objects.requireNonNull(playerId, "playerId"));
    }

    public synchronized Map<UUID, PersistedState> persistentSnapshot() {
        Map<UUID, PersistedState> result = new LinkedHashMap<>();
        states.forEach((playerId, state) -> result.put(playerId, state.persisted()));
        return Map.copyOf(result);
    }

    public synchronized void restoreSnapshot(Map<UUID, PersistedState> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        if (snapshot.size() > maxTrackedPlayers) {
            throw new IllegalArgumentException("corruption snapshot exceeds tracked-player ceiling");
        }
        Map<UUID, MutableState> restored = new LinkedHashMap<>();
        snapshot.forEach((playerId, persisted) -> {
            if (playerId == null || persisted == null) return;
            PersistedState sanitized = PersistedState.sanitize(
                persisted.units(),
                persisted.lastMeaningfulUpdateTick(),
                persisted.lastRecoveryTick(),
                persisted.acquisitionEvents(),
                persisted.recoveryEvents());
            double units = Math.min(sanitized.units(), maxCorruptionUnits);
            if (units == 0.0D && sanitized.acquisitionEvents() == 0L && sanitized.recoveryEvents() == 0L) return;
            restored.put(playerId, new MutableState(
                units,
                sanitized.lastMeaningfulUpdateTick(),
                sanitized.lastRecoveryTick(),
                sanitized.acquisitionEvents(),
                sanitized.recoveryEvents()));
        });
        states.clear();
        states.putAll(restored);
        reservations.clear();
    }

    public synchronized int size() {
        return states.size();
    }

    public CorruptionThresholds thresholds() {
        return thresholds;
    }

    public double maxCorruptionUnits() {
        return maxCorruptionUnits;
    }

    private CorruptionUpdate acquire(
        UUID playerId,
        long serverTick,
        double rawUnits,
        CorruptionAcquisitionProfile profile,
        CorruptionResistanceSnapshot resistance
    ) {
        validatePlayerTick(playerId, serverTick);
        Objects.requireNonNull(profile, "profile");
        Objects.requireNonNull(resistance, "resistance");
        if (!Double.isFinite(rawUnits) || rawUnits < 0.0D) {
            throw new IllegalArgumentException("raw corruption units must be finite and non-negative");
        }
        CorruptionSnapshot before = snapshotOf(states.get(playerId));
        if (rawUnits == 0.0D || before.units() >= maxCorruptionUnits) {
            return new CorruptionUpdate(before, before, 0.0D, List.of());
        }

        double applied = appliedCorruption(before.units(), rawUnits, profile, resistance);
        if (applied <= 0.0D) return new CorruptionUpdate(before, before, 0.0D, List.of());

        MutableState state = states.get(playerId);
        if (state == null) {
            ensureCapacityFor(playerId, "corruption state registry is full");
            state = new MutableState(0.0D, 0L, -1L, 0L, 0L);
            states.put(playerId, state);
        }
        state.units = Math.min(maxCorruptionUnits, state.units + applied);
        state.lastMeaningfulUpdateTick = serverTick;
        state.acquisitionEvents = saturatingIncrement(state.acquisitionEvents);
        CorruptionSnapshot after = snapshotOf(state);
        List<CorruptionTransition> transitions = transitions(playerId, before, after, serverTick);
        publish(transitions);
        return new CorruptionUpdate(before, after, applied, transitions);
    }

    private double appliedCorruption(
        double currentUnits,
        double rawUnits,
        CorruptionAcquisitionProfile profile,
        CorruptionResistanceSnapshot resistance
    ) {
        if (!Double.isFinite(rawUnits) || rawUnits < 0.0D) {
            throw new IllegalArgumentException("raw corruption units must be finite and non-negative");
        }
        if (rawUnits == 0.0D || currentUnits >= maxCorruptionUnits) return 0.0D;
        double boundedRaw = Math.min(rawUnits, maxCorruptionUnits);
        return Math.min(
            maxCorruptionUnits - currentUnits,
            boundedRaw * resistance.residualMultiplier(profile));
    }

    private int occupiedSlots() {
        int reservedWithoutState = 0;
        for (UUID playerId : reservations) {
            if (!states.containsKey(playerId)) reservedWithoutState++;
        }
        return states.size() + reservedWithoutState;
    }

    private void ensureCapacityFor(UUID playerId, String message) {
        if (states.containsKey(playerId)) return;
        if (!reservations.contains(playerId) && occupiedSlots() >= maxTrackedPlayers) {
            throw new IllegalStateException(message);
        }
    }

    private CorruptionSnapshot snapshotOf(MutableState state) {
        if (state == null) return new CorruptionSnapshot(0.0D, CorruptionBand.CLEAR, 0L, -1L, 0L, 0L, STATE_SCHEMA_VERSION);
        return new CorruptionSnapshot(
            state.units,
            thresholds.bandFor(state.units),
            state.lastMeaningfulUpdateTick,
            state.lastRecoveryTick,
            state.acquisitionEvents,
            state.recoveryEvents,
            STATE_SCHEMA_VERSION);
    }

    private List<CorruptionTransition> transitions(
        UUID playerId,
        CorruptionSnapshot before,
        CorruptionSnapshot after,
        long serverTick
    ) {
        int from = before.band().ordinal();
        int to = after.band().ordinal();
        if (from == to) return List.of();
        int step = Integer.compare(to, from);
        List<CorruptionTransition> result = new ArrayList<>();
        CorruptionBand cursor = before.band();
        for (int index = from + step; ; index += step) {
            CorruptionBand next = CorruptionBand.values()[index];
            result.add(new CorruptionTransition(
                playerId, cursor, next, before.units(), after.units(), serverTick));
            cursor = next;
            if (index == to) break;
        }
        return List.copyOf(result);
    }

    private void publish(List<CorruptionTransition> transitions) {
        if (transitions.isEmpty() || listeners.isEmpty()) return;
        for (CorruptionTransition transition : transitions) {
            for (CorruptionThresholdListener listener : listeners.values()) {
                try {
                    listener.onTransition(transition);
                } catch (RuntimeException | LinkageError ignored) {
                    // Consequence integrations are isolated; corruption state is already authoritative.
                }
            }
        }
    }

    private static void validatePlayerTick(UUID playerId, long serverTick) {
        Objects.requireNonNull(playerId, "playerId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
    }

    private static double saturatingMultiply(double first, double second) {
        double product = first * second;
        return Double.isFinite(product) ? product : ABSOLUTE_MAX_CORRUPTION_UNITS;
    }

    private static long saturatingIncrement(long value) {
        return value >= MAX_TELEMETRY_EVENTS ? MAX_TELEMETRY_EVENTS : value + 1L;
    }

    private static final class MutableState {
        double units;
        long lastMeaningfulUpdateTick;
        long lastRecoveryTick;
        long acquisitionEvents;
        long recoveryEvents;

        MutableState(double units, long lastMeaningfulUpdateTick, long lastRecoveryTick, long acquisitionEvents, long recoveryEvents) {
            this.units = units;
            this.lastMeaningfulUpdateTick = lastMeaningfulUpdateTick;
            this.lastRecoveryTick = lastRecoveryTick;
            this.acquisitionEvents = acquisitionEvents;
            this.recoveryEvents = recoveryEvents;
        }

        PersistedState persisted() {
            return new PersistedState(
                units,
                lastMeaningfulUpdateTick,
                lastRecoveryTick,
                acquisitionEvents,
                recoveryEvents,
                STATE_SCHEMA_VERSION);
        }
    }

    public record CorruptionSnapshot(
        double units,
        CorruptionBand band,
        long lastMeaningfulUpdateTick,
        long lastRecoveryTick,
        long acquisitionEvents,
        long recoveryEvents,
        int schemaVersion
    ) {
        public CorruptionSnapshot {
            if (!Double.isFinite(units) || units < 0.0D || units > ABSOLUTE_MAX_CORRUPTION_UNITS) {
                throw new IllegalArgumentException("corruption units outside absolute bounds");
            }
            Objects.requireNonNull(band, "band");
            if (lastMeaningfulUpdateTick < 0L || lastRecoveryTick < -1L) {
                throw new IllegalArgumentException("corruption update metadata outside bounds");
            }
            if (acquisitionEvents < 0L || acquisitionEvents > MAX_TELEMETRY_EVENTS
                || recoveryEvents < 0L || recoveryEvents > MAX_TELEMETRY_EVENTS) {
                throw new IllegalArgumentException("corruption telemetry outside bounds");
            }
            if (schemaVersion != STATE_SCHEMA_VERSION) throw new IllegalArgumentException("unsupported corruption state schema");
        }
    }

    public record CorruptionPreflight(CorruptionSnapshot current, double appliedCorruption) {
        public CorruptionPreflight {
            Objects.requireNonNull(current, "current");
            if (!Double.isFinite(appliedCorruption) || appliedCorruption < 0.0D
                || appliedCorruption > ABSOLUTE_MAX_CORRUPTION_UNITS) {
                throw new IllegalArgumentException("preflight corruption outside absolute bounds");
            }
        }
    }

    public record PersistedState(
        double units,
        long lastMeaningfulUpdateTick,
        long lastRecoveryTick,
        long acquisitionEvents,
        long recoveryEvents,
        int schemaVersion
    ) {
        public PersistedState {
            if (!Double.isFinite(units) || units < 0.0D || units > ABSOLUTE_MAX_CORRUPTION_UNITS) {
                throw new IllegalArgumentException("persisted corruption units outside absolute bounds");
            }
            if (lastMeaningfulUpdateTick < 0L || lastRecoveryTick < -1L) {
                throw new IllegalArgumentException("persisted corruption metadata outside bounds");
            }
            if (acquisitionEvents < 0L || acquisitionEvents > MAX_TELEMETRY_EVENTS
                || recoveryEvents < 0L || recoveryEvents > MAX_TELEMETRY_EVENTS) {
                throw new IllegalArgumentException("persisted corruption telemetry outside bounds");
            }
            if (schemaVersion != STATE_SCHEMA_VERSION) throw new IllegalArgumentException("unsupported corruption state schema");
        }

        public static PersistedState sanitize(
            double units,
            long lastMeaningfulUpdateTick,
            long lastRecoveryTick,
            long acquisitionEvents,
            long recoveryEvents
        ) {
            double safeUnits = Double.isFinite(units)
                ? Math.max(0.0D, Math.min(ABSOLUTE_MAX_CORRUPTION_UNITS, units))
                : 0.0D;
            long safeUpdated = Math.max(0L, lastMeaningfulUpdateTick);
            long safeRecovery = Math.max(-1L, lastRecoveryTick);
            long safeAcquisitions = Math.max(0L, Math.min(MAX_TELEMETRY_EVENTS, acquisitionEvents));
            long safeRecoveries = Math.max(0L, Math.min(MAX_TELEMETRY_EVENTS, recoveryEvents));
            return new PersistedState(
                safeUnits,
                safeUpdated,
                safeRecovery,
                safeAcquisitions,
                safeRecoveries,
                STATE_SCHEMA_VERSION);
        }
    }

    public record CorruptionTransition(
        UUID playerId,
        CorruptionBand from,
        CorruptionBand to,
        double previousUnits,
        double newUnits,
        long serverTick
    ) {
        public CorruptionTransition {
            Objects.requireNonNull(playerId, "playerId");
            Objects.requireNonNull(from, "from");
            Objects.requireNonNull(to, "to");
            if (from == to) throw new IllegalArgumentException("transition bands must differ");
            if (!Double.isFinite(previousUnits) || !Double.isFinite(newUnits)
                || previousUnits < 0.0D || newUnits < 0.0D) {
                throw new IllegalArgumentException("transition units must be finite and non-negative");
            }
            if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        }
    }

    public record CorruptionUpdate(
        CorruptionSnapshot before,
        CorruptionSnapshot after,
        double appliedDelta,
        List<CorruptionTransition> transitions
    ) {
        public CorruptionUpdate {
            Objects.requireNonNull(before, "before");
            Objects.requireNonNull(after, "after");
            if (!Double.isFinite(appliedDelta)) throw new IllegalArgumentException("appliedDelta must be finite");
            transitions = List.copyOf(Objects.requireNonNull(transitions, "transitions"));
        }
    }

    @FunctionalInterface
    public interface CorruptionThresholdListener {
        void onTransition(CorruptionTransition transition);
    }
}
