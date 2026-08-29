package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public final class RitualEngine {
    public static final int MAX_SNAPSHOT_ENTRIES = 4_096;

    private final RitualSessionRegistry sessions;
    private final RitualActivationGuard activationGuard;
    private final RitualRequirementEvaluator requirements;
    private final RitualComponentProvider components;
    private final RitualOutcomeExecutor outcomes;

    public RitualEngine(
            RitualSessionRegistry sessions,
            RitualActivationGuard activationGuard,
            RitualRequirementEvaluator requirements,
            RitualComponentProvider components,
            RitualOutcomeExecutor outcomes
    ) {
        this.sessions = Objects.requireNonNull(sessions, "sessions");
        this.activationGuard = Objects.requireNonNull(activationGuard, "activationGuard");
        this.requirements = Objects.requireNonNull(requirements, "requirements");
        this.components = Objects.requireNonNull(components, "components");
        this.outcomes = Objects.requireNonNull(outcomes, "outcomes");
    }

    public synchronized RitualResult start(
            RitualDefinition definition,
            RitualActivationId activationId,
            RitualContext context,
            long nowTick
    ) {
        Objects.requireNonNull(definition, "definition");
        Objects.requireNonNull(activationId, "activationId");
        Objects.requireNonNull(context, "context");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");

        ArcanaDecision requirement = safeRequirement(definition, context, nowTick);
        if (!requirement.allowed()) {
            return RitualResult.denied(RitualResult.Status.DENIED_REQUIREMENT, requirement);
        }
        if (sessions.anchorBusy(context.anchor())) {
            return RitualResult.of(
                    RitualResult.Status.DENIED_ANCHOR_BUSY,
                    "ritual_anchor_busy",
                    "another ritual already owns this anchor");
        }
        if (!sessions.hasCapacity()) {
            return RitualResult.of(
                    RitualResult.Status.DENIED_CAPACITY,
                    "ritual_session_capacity",
                    "ritual session registry is full");
        }

        ArcanaDecision replay = activationGuard.claim(activationId, nowTick);
        if (!replay.allowed()) {
            RitualResult.Status status = "ritual_activation_replay".equals(replay.code())
                    ? RitualResult.Status.DENIED_REPLAY
                    : RitualResult.Status.DENIED_CAPACITY;
            return RitualResult.denied(status, replay);
        }

        long commitAtTick = safeAdd(nowTick, definition.commitDelayTicks());
        long completeAtTick = safeAdd(nowTick, definition.completionDelayTicks());
        RitualSessionRegistry.Session session = new RitualSessionRegistry.Session(
                definition,
                activationId,
                context,
                nowTick,
                commitAtTick,
                completeAtTick,
                RitualSessionState.PRECOMMIT);
        if (!sessions.add(session)) {
            return RitualResult.of(
                    RitualResult.Status.DENIED_ANCHOR_BUSY,
                    "ritual_anchor_busy",
                    "ritual session could not claim anchor");
        }
        return RitualResult.started();
    }

    public synchronized RitualResult interrupt(RitualActivationId activationId, String reason) {
        Objects.requireNonNull(activationId, "activationId");
        Objects.requireNonNull(reason, "reason");
        RitualSessionRegistry.Session session = sessions.get(activationId);
        if (session == null) {
            return RitualResult.of(
                    RitualResult.Status.DENIED_NOT_ACTIVE,
                    "ritual_not_active",
                    "ritual activation is not active");
        }
        sessions.remove(activationId);
        if (session.state == RitualSessionState.PRECOMMIT) {
            return RitualResult.of(RitualResult.Status.INTERRUPTED_PRECOMMIT, reason, "ritual interrupted before commit");
        }
        return RitualResult.of(
                RitualResult.Status.INTERRUPTED_POSTCOMMIT,
                reason,
                "ritual interrupted after components were committed");
    }

    public synchronized TickSummary tick(long nowTick, int maxSessionsToProcess) {
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        if (maxSessionsToProcess <= 0) return new TickSummary(0, 0, 0);

        int committed = 0;
        int completed = 0;
        int cancelled = 0;
        for (RitualSessionRegistry.Session session : sessions.sessions(maxSessionsToProcess)) {
            if (session.state == RitualSessionState.PRECOMMIT && nowTick >= session.commitAtTick) {
                ArcanaDecision available = safeComponentCheck(session, nowTick);
                if (!available.allowed()) {
                    sessions.remove(session.activationId);
                    cancelled++;
                    continue;
                }

                RitualComponentReservation reservation = safeReserve(session, nowTick);
                if (!reservation.decision().allowed()) {
                    sessions.remove(session.activationId);
                    cancelled++;
                    continue;
                }
                try {
                    reservation.commit();
                    session.state = RitualSessionState.COMMITTED;
                    committed++;
                } catch (RuntimeException | LinkageError failure) {
                    try {
                        reservation.refund();
                    } catch (RuntimeException | LinkageError ignored) {
                        // Reservation remains fail-closed: no outcome executes after a failed commit.
                    }
                    sessions.remove(session.activationId);
                    cancelled++;
                    continue;
                }
            }

            if (session.state == RitualSessionState.COMMITTED && nowTick >= session.completeAtTick) {
                ArcanaDecision outcome = safeOutcome(session, nowTick);
                sessions.remove(session.activationId);
                if (outcome.allowed()) completed++;
                else cancelled++;
            }
        }
        return new TickSummary(committed, completed, cancelled);
    }

    public synchronized int activeSessionCount() {
        return sessions.size();
    }

    public synchronized List<RitualSessionSnapshot> snapshot(int maxEntries) {
        if (maxEntries <= 0 || maxEntries > MAX_SNAPSHOT_ENTRIES) {
            throw new IllegalArgumentException("snapshot maxEntries outside bounds");
        }
        return sessions.sessions(maxEntries).stream().map(RitualSessionRegistry.Session::snapshot).toList();
    }

    public synchronized RitualRestoreResult restore(
            List<RitualDefinition> definitions,
            List<RitualSessionSnapshot> snapshots,
            long nowTick
    ) {
        Objects.requireNonNull(definitions, "definitions");
        Objects.requireNonNull(snapshots, "snapshots");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        if (definitions.size() > MAX_SNAPSHOT_ENTRIES || snapshots.size() > MAX_SNAPSHOT_ENTRIES) {
            throw new IllegalArgumentException("ritual restore input exceeds bound");
        }

        Map<ArcanaRitualId, RitualDefinition> byId = new HashMap<>();
        for (RitualDefinition definition : definitions) {
            if (definition == null || byId.putIfAbsent(definition.id(), definition) != null) {
                throw new IllegalArgumentException("ritual definitions must be non-null and unique");
            }
        }

        int restored = 0;
        int rejected = 0;
        for (RitualSessionSnapshot snapshot : snapshots) {
            if (!restoreOne(byId, snapshot, nowTick)) rejected++;
            else restored++;
        }
        return new RitualRestoreResult(restored, rejected);
    }

    private boolean restoreOne(
            Map<ArcanaRitualId, RitualDefinition> definitions,
            RitualSessionSnapshot snapshot,
            long nowTick
    ) {
        if (snapshot == null) return false;
        RitualDefinition definition = definitions.get(snapshot.ritualId());
        if (definition == null) return false;
        if (snapshot.commitAtTick() - snapshot.startedAtTick() != definition.commitDelayTicks()) return false;
        if (snapshot.completeAtTick() - snapshot.startedAtTick() != definition.completionDelayTicks()) return false;
        if (sessions.anchorBusy(snapshot.context().anchor()) || !sessions.hasCapacity()) return false;
        if (!activationGuard.remember(snapshot.activationId(), snapshot.startedAtTick(), nowTick)) return false;

        RitualSessionRegistry.Session restored = new RitualSessionRegistry.Session(
                definition,
                snapshot.activationId(),
                snapshot.context(),
                snapshot.startedAtTick(),
                snapshot.commitAtTick(),
                snapshot.completeAtTick(),
                snapshot.state());
        return sessions.add(restored);
    }

    private ArcanaDecision safeRequirement(RitualDefinition definition, RitualContext context, long nowTick) {
        try {
            return Objects.requireNonNull(requirements.check(definition, context, nowTick), "requirement decision");
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("ritual_requirement_failed", "ritual requirement evaluator failed closed");
        }
    }

    private ArcanaDecision safeComponentCheck(RitualSessionRegistry.Session session, long nowTick) {
        try {
            return Objects.requireNonNull(
                    components.check(session.definition, session.context, nowTick),
                    "component decision");
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("ritual_component_check_failed", "ritual component check failed closed");
        }
    }

    private RitualComponentReservation safeReserve(RitualSessionRegistry.Session session, long nowTick) {
        try {
            return Objects.requireNonNull(
                    components.reserve(session.definition, session.context, nowTick),
                    "component reservation");
        } catch (RuntimeException | LinkageError failure) {
            return RitualComponentReservation.denied(
                    "ritual_component_reserve_failed",
                    "ritual component reservation failed closed");
        }
    }

    private ArcanaDecision safeOutcome(RitualSessionRegistry.Session session, long nowTick) {
        try {
            return Objects.requireNonNull(
                    outcomes.execute(session.definition, session.context, nowTick),
                    "outcome decision");
        } catch (RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny("ritual_outcome_failed", "ritual outcome failed closed");
        }
    }

    private static long safeAdd(long base, long delta) {
        if (delta > Long.MAX_VALUE - base) return Long.MAX_VALUE;
        return base + delta;
    }

    public record TickSummary(int committed, int completed, int cancelled) {
        public TickSummary {
            if (committed < 0 || completed < 0 || cancelled < 0) {
                throw new IllegalArgumentException("tick summary counts cannot be negative");
            }
        }
    }
}
