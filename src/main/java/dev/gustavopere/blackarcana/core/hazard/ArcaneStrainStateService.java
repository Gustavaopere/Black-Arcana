package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoverySnapshot;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Lazy/event-driven short-term arcane load state. No global player tick scan is required. */
public final class ArcaneStrainStateService {
    public static final int STATE_SCHEMA_VERSION = 1;
    public static final int ABSOLUTE_MAX_TRACKED_PLAYERS = 65_536;
    public static final double CANONICAL_MAX_STRAIN_UNITS = 1_000.0D;
    public static final double ABSOLUTE_MAX_STRAIN_UNITS = 1_000_000.0D;
    public static final double CANONICAL_BASE_RECOVERY_PER_TICK = 0.05D;
    public static final double ABSOLUTE_MAX_BASE_RECOVERY_PER_TICK = 100.0D;
    public static final long MAX_TELEMETRY_EVENTS = 1_000_000_000L;

    private final int maxTrackedPlayers;
    private final double maxStrainUnits;
    private final double baseRecoveryPerTick;
    private final ArcaneStrainRecoveryProviderRegistry recoveryProviders;
    private final Map<UUID, MutableState> states = new LinkedHashMap<>();

    public ArcaneStrainStateService(
        int maxTrackedPlayers,
        double maxStrainUnits,
        double baseRecoveryPerTick,
        ArcaneStrainRecoveryProviderRegistry recoveryProviders
    ) {
        if (maxTrackedPlayers <= 0 || maxTrackedPlayers > ABSOLUTE_MAX_TRACKED_PLAYERS) {
            throw new IllegalArgumentException("maxTrackedPlayers outside absolute bounds");
        }
        if (!Double.isFinite(maxStrainUnits) || maxStrainUnits <= 0.0D
            || maxStrainUnits > ABSOLUTE_MAX_STRAIN_UNITS) {
            throw new IllegalArgumentException("maxStrainUnits outside absolute bounds");
        }
        if (!Double.isFinite(baseRecoveryPerTick) || baseRecoveryPerTick < 0.0D
            || baseRecoveryPerTick > ABSOLUTE_MAX_BASE_RECOVERY_PER_TICK) {
            throw new IllegalArgumentException("baseRecoveryPerTick outside absolute bounds");
        }
        this.maxTrackedPlayers = maxTrackedPlayers;
        this.maxStrainUnits = maxStrainUnits;
        this.baseRecoveryPerTick = baseRecoveryPerTick;
        this.recoveryProviders = Objects.requireNonNull(recoveryProviders, "recoveryProviders");
    }

    public static ArcaneStrainStateService canonical(int maxTrackedPlayers) {
        return new ArcaneStrainStateService(
            maxTrackedPlayers,
            CANONICAL_MAX_STRAIN_UNITS,
            CANONICAL_BASE_RECOVERY_PER_TICK,
            ArcaneStrainRecoveryProviderRegistry.canonical());
    }

    public synchronized StrainSnapshot snapshot(UUID playerId, long serverTick) {
        validatePlayerTick(playerId, serverTick);
        MutableState state = states.get(playerId);
        if (state == null) return emptySnapshot(serverTick);
        return effectiveSnapshot(playerId, state, serverTick).snapshot();
    }

    public synchronized StrainPreflight preflight(
        UUID playerId,
        long serverTick,
        ArcaneStrainProfile profile,
        double avoidableResidualMultiplier,
        double confirmedDamage,
        long channelTicks
    ) {
        validatePlayerTick(playerId, serverTick);
        Objects.requireNonNull(profile, "profile");
        EffectiveState effective = effectiveState(playerId, serverTick);
        double added = profile.appliedStrain(confirmedDamage, channelTicks, avoidableResidualMultiplier);
        double predicted = Math.min(maxStrainUnits, effective.snapshot().units() + added);
        return new StrainPreflight(
            effective.snapshot(),
            predicted,
            Math.max(0.0D, predicted - effective.snapshot().units()),
            profile.backlashMultiplier(effective.snapshot().units(), maxStrainUnits),
            profile.corruptionMultiplier(effective.snapshot().units(), maxStrainUnits),
            profile.hardGateActive(effective.snapshot().units()),
            profile.hardGateActive(predicted),
            effective.recovery());
    }

    public synchronized StrainUpdate commitCast(
        UUID playerId,
        long serverTick,
        ArcaneStrainProfile profile,
        double avoidableResidualMultiplier,
        double confirmedDamage,
        long channelTicks
    ) {
        StrainPreflight preflight = preflight(
            playerId, serverTick, profile, avoidableResidualMultiplier, confirmedDamage, channelTicks);
        if (preflight.appliedStrain() == 0.0D) {
            return new StrainUpdate(preflight.current(), preflight.current(), 0.0D, preflight);
        }
        MutableState state = states.get(playerId);
        if (state == null) {
            if (states.size() >= maxTrackedPlayers) throw new IllegalStateException("strain state registry is full");
            state = new MutableState(0.0D, serverTick, 0L, 0L);
            states.put(playerId, state);
        }
        state.units = preflight.predictedUnits();
        state.lastUpdateTick = serverTick;
        state.acquisitionEvents = saturatingIncrement(state.acquisitionEvents);
        StrainSnapshot after = snapshotOf(state, serverTick);
        return new StrainUpdate(preflight.current(), after, preflight.appliedStrain(), preflight);
    }

    /** Explicit rest/ritual/buff recovery hook layered on top of lazy natural recovery. */
    public synchronized StrainUpdate recover(UUID playerId, long serverTick, double requestedUnits) {
        validatePlayerTick(playerId, serverTick);
        if (!Double.isFinite(requestedUnits) || requestedUnits < 0.0D) {
            throw new IllegalArgumentException("requestedUnits must be finite and non-negative");
        }
        MutableState state = states.get(playerId);
        if (state == null) {
            StrainSnapshot empty = emptySnapshot(serverTick);
            return new StrainUpdate(empty, empty, 0.0D, null);
        }
        EffectiveState effective = effectiveSnapshot(playerId, state, serverTick);
        StrainSnapshot before = effective.snapshot();
        double remaining = Math.max(0.0D, before.units() - requestedUnits);
        double recovered = before.units() - remaining;
        if (remaining == 0.0D) {
            states.remove(playerId);
            StrainSnapshot after = emptySnapshot(serverTick);
            return new StrainUpdate(before, after, -recovered, null);
        }
        state.units = remaining;
        state.lastUpdateTick = serverTick;
        state.recoveryEvents = saturatingIncrement(state.recoveryEvents);
        StrainSnapshot after = snapshotOf(state, serverTick);
        return new StrainUpdate(before, after, -recovered, null);
    }

    public synchronized Map<UUID, PersistedState> persistentSnapshot() {
        Map<UUID, PersistedState> result = new LinkedHashMap<>();
        states.forEach((playerId, state) -> result.put(playerId, state.persisted()));
        return Map.copyOf(result);
    }

    public synchronized void restoreSnapshot(Map<UUID, PersistedState> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        if (snapshot.size() > maxTrackedPlayers) {
            throw new IllegalArgumentException("strain snapshot exceeds tracked-player ceiling");
        }
        Map<UUID, MutableState> restored = new LinkedHashMap<>();
        snapshot.forEach((playerId, persisted) -> {
            if (playerId == null || persisted == null) return;
            PersistedState safe = PersistedState.sanitize(
                persisted.units(), persisted.lastUpdateTick(), persisted.acquisitionEvents(), persisted.recoveryEvents());
            double units = Math.min(maxStrainUnits, safe.units());
            if (units == 0.0D) return;
            restored.put(playerId, new MutableState(
                units, safe.lastUpdateTick(), safe.acquisitionEvents(), safe.recoveryEvents()));
        });
        states.clear();
        states.putAll(restored);
    }

    public synchronized int size() {
        return states.size();
    }

    public ArcaneStrainRecoveryProviderRegistry recoveryProviders() {
        return recoveryProviders;
    }

    public double maxStrainUnits() {
        return maxStrainUnits;
    }

    public double baseRecoveryPerTick() {
        return baseRecoveryPerTick;
    }

    private EffectiveState effectiveState(UUID playerId, long serverTick) {
        MutableState state = states.get(playerId);
        return state == null
            ? new EffectiveState(emptySnapshot(serverTick), recoverySnapshot(playerId, serverTick, 0.0D))
            : effectiveSnapshot(playerId, state, serverTick);
    }

    private EffectiveState effectiveSnapshot(UUID playerId, MutableState state, long serverTick) {
        ArcaneStrainRecoverySnapshot recovery = recoverySnapshot(playerId, serverTick, state.units);
        long elapsed = Math.max(0L, serverTick - state.lastUpdateTick);
        double recovered = saturatingMultiply((double) elapsed, recovery.totalUnitsPerTick());
        double effectiveUnits = Math.max(0.0D, state.units - recovered);
        return new EffectiveState(
            new StrainSnapshot(
                effectiveUnits,
                state.lastUpdateTick,
                state.acquisitionEvents,
                state.recoveryEvents,
                STATE_SCHEMA_VERSION),
            recovery);
    }

    private ArcaneStrainRecoverySnapshot recoverySnapshot(UUID playerId, long serverTick, double storedUnits) {
        return recoveryProviders.snapshot(
            new ArcaneStrainRecoveryQuery(playerId, serverTick, storedUnits),
            baseRecoveryPerTick);
    }

    private static StrainSnapshot snapshotOf(MutableState state, long visibleTick) {
        return new StrainSnapshot(
            state.units,
            Math.min(state.lastUpdateTick, visibleTick),
            state.acquisitionEvents,
            state.recoveryEvents,
            STATE_SCHEMA_VERSION);
    }

    private static StrainSnapshot emptySnapshot(long serverTick) {
        return new StrainSnapshot(0.0D, serverTick, 0L, 0L, STATE_SCHEMA_VERSION);
    }

    private static void validatePlayerTick(UUID playerId, long serverTick) {
        Objects.requireNonNull(playerId, "playerId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
    }

    private static double saturatingMultiply(double first, double second) {
        double result = first * second;
        return Double.isFinite(result) ? result : ABSOLUTE_MAX_STRAIN_UNITS;
    }

    private static long saturatingIncrement(long value) {
        return value >= MAX_TELEMETRY_EVENTS ? MAX_TELEMETRY_EVENTS : value + 1L;
    }

    private static final class MutableState {
        double units;
        long lastUpdateTick;
        long acquisitionEvents;
        long recoveryEvents;

        MutableState(double units, long lastUpdateTick, long acquisitionEvents, long recoveryEvents) {
            this.units = units;
            this.lastUpdateTick = lastUpdateTick;
            this.acquisitionEvents = acquisitionEvents;
            this.recoveryEvents = recoveryEvents;
        }

        PersistedState persisted() {
            return new PersistedState(units, lastUpdateTick, acquisitionEvents, recoveryEvents, STATE_SCHEMA_VERSION);
        }
    }

    private record EffectiveState(StrainSnapshot snapshot, ArcaneStrainRecoverySnapshot recovery) { }

    public record StrainSnapshot(
        double units,
        long lastUpdateTick,
        long acquisitionEvents,
        long recoveryEvents,
        int schemaVersion
    ) {
        public StrainSnapshot {
            if (!Double.isFinite(units) || units < 0.0D || units > ABSOLUTE_MAX_STRAIN_UNITS) {
                throw new IllegalArgumentException("strain units outside absolute bounds");
            }
            if (lastUpdateTick < 0L) throw new IllegalArgumentException("lastUpdateTick cannot be negative");
            if (acquisitionEvents < 0L || acquisitionEvents > MAX_TELEMETRY_EVENTS
                || recoveryEvents < 0L || recoveryEvents > MAX_TELEMETRY_EVENTS) {
                throw new IllegalArgumentException("strain telemetry outside bounds");
            }
            if (schemaVersion != STATE_SCHEMA_VERSION) throw new IllegalArgumentException("unsupported strain state schema");
        }
    }

    public record PersistedState(
        double units,
        long lastUpdateTick,
        long acquisitionEvents,
        long recoveryEvents,
        int schemaVersion
    ) {
        public PersistedState {
            if (!Double.isFinite(units) || units < 0.0D || units > ABSOLUTE_MAX_STRAIN_UNITS) {
                throw new IllegalArgumentException("persisted strain units outside absolute bounds");
            }
            if (lastUpdateTick < 0L) throw new IllegalArgumentException("persisted strain tick cannot be negative");
            if (acquisitionEvents < 0L || acquisitionEvents > MAX_TELEMETRY_EVENTS
                || recoveryEvents < 0L || recoveryEvents > MAX_TELEMETRY_EVENTS) {
                throw new IllegalArgumentException("persisted strain telemetry outside bounds");
            }
            if (schemaVersion != STATE_SCHEMA_VERSION) throw new IllegalArgumentException("unsupported strain state schema");
        }

        public static PersistedState sanitize(double units, long lastUpdateTick, long acquisitionEvents, long recoveryEvents) {
            double safeUnits = Double.isFinite(units)
                ? Math.max(0.0D, Math.min(ABSOLUTE_MAX_STRAIN_UNITS, units))
                : 0.0D;
            long safeTick = Math.max(0L, lastUpdateTick);
            long safeAcquisitions = Math.max(0L, Math.min(MAX_TELEMETRY_EVENTS, acquisitionEvents));
            long safeRecoveries = Math.max(0L, Math.min(MAX_TELEMETRY_EVENTS, recoveryEvents));
            return new PersistedState(safeUnits, safeTick, safeAcquisitions, safeRecoveries, STATE_SCHEMA_VERSION);
        }
    }

    public record StrainPreflight(
        StrainSnapshot current,
        double predictedUnits,
        double appliedStrain,
        double backlashMultiplier,
        double corruptionMultiplier,
        boolean hardGateActive,
        boolean predictedHardGate,
        ArcaneStrainRecoverySnapshot recovery
    ) {
        public StrainPreflight {
            Objects.requireNonNull(current, "current");
            Objects.requireNonNull(recovery, "recovery");
            if (!Double.isFinite(predictedUnits) || predictedUnits < 0.0D || predictedUnits > ABSOLUTE_MAX_STRAIN_UNITS
                || !Double.isFinite(appliedStrain) || appliedStrain < 0.0D
                || !Double.isFinite(backlashMultiplier) || backlashMultiplier < 1.0D
                || !Double.isFinite(corruptionMultiplier) || corruptionMultiplier < 1.0D) {
                throw new IllegalArgumentException("invalid strain preflight values");
            }
        }
    }

    public record StrainUpdate(
        StrainSnapshot before,
        StrainSnapshot after,
        double appliedDelta,
        StrainPreflight preflight
    ) {
        public StrainUpdate {
            Objects.requireNonNull(before, "before");
            Objects.requireNonNull(after, "after");
            if (!Double.isFinite(appliedDelta)) throw new IllegalArgumentException("appliedDelta must be finite");
        }
    }
}
