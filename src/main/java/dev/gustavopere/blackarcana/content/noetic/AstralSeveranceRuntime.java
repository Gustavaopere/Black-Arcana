package dev.gustavopere.blackarcana.content.noetic;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;

/**
 * Bounded server-owned lifecycle for Astral Severance.
 *
 * <p>This runtime deliberately owns no arbitrary observed target, client-authored position, avatar entity,
 * camera state, resource provider or cooldown policy. It supplies the unique projection/session identity and
 * terminal lifecycle that a later canonical cast adapter may activate only after its upstream transaction has
 * already authorized the spell.</p>
 */
public final class AstralSeveranceRuntime {
    public enum StartResult {
        STARTED,
        CASTER_ALREADY_PROJECTED,
        GLOBAL_LIMIT,
        INVALID_DURATION,
        INVALID_RANGE,
        IDENTITY_COLLISION
    }

    public enum CloseReason {
        EXPLICIT_RETURN,
        EXPIRED,
        BODY_DAMAGED,
        BODY_DEATH,
        VIEWER_LOGOUT,
        DIMENSION_CHANGED,
        AUTHORIZATION_REVOKED,
        SERVER_STOP
    }

    private final int maxActiveProjections;
    private final Supplier<UUID> projectionIdSupplier;
    private final Map<UUID, ProjectionSession> projectionsByCaster = new LinkedHashMap<>();

    public AstralSeveranceRuntime(int maxActiveProjections) {
        this(maxActiveProjections, UUID::randomUUID);
    }

    AstralSeveranceRuntime(int maxActiveProjections, Supplier<UUID> projectionIdSupplier) {
        if (maxActiveProjections <= 0 || maxActiveProjections > NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS) {
            throw new IllegalArgumentException("Astral projection limit exceeds the hard Noetic ceiling");
        }
        this.maxActiveProjections = maxActiveProjections;
        this.projectionIdSupplier = Objects.requireNonNull(projectionIdSupplier, "projectionIdSupplier");
    }

    public synchronized StartResult start(
            UUID casterId,
            long nowTick,
            int durationTicks,
            double maxRangeBlocks
    ) {
        Objects.requireNonNull(casterId, "casterId");
        if (nowTick < 0L) {
            throw new IllegalArgumentException("Astral projection tick must be non-negative");
        }
        if (durationTicks <= 0 || durationTicks > NoeticSafetyCeilings.MAX_DURATION_TICKS) {
            return StartResult.INVALID_DURATION;
        }
        if (!Double.isFinite(maxRangeBlocks)
                || maxRangeBlocks <= 0.0D
                || maxRangeBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
            return StartResult.INVALID_RANGE;
        }
        if (projectionsByCaster.containsKey(casterId)) {
            return StartResult.CASTER_ALREADY_PROJECTED;
        }
        if (projectionsByCaster.size() >= maxActiveProjections) {
            return StartResult.GLOBAL_LIMIT;
        }

        final long expiresAtTick;
        try {
            expiresAtTick = Math.addExact(nowTick, durationTicks);
        } catch (ArithmeticException overflow) {
            return StartResult.INVALID_DURATION;
        }

        UUID projectionId = Objects.requireNonNull(projectionIdSupplier.get(), "projectionId");
        for (ProjectionSession existing : projectionsByCaster.values()) {
            if (existing.projectionId.equals(projectionId)) {
                return StartResult.IDENTITY_COLLISION;
            }
        }

        projectionsByCaster.put(
                casterId,
                new ProjectionSession(casterId, projectionId, nowTick, expiresAtTick, maxRangeBlocks));
        return StartResult.STARTED;
    }

    public synchronized Optional<ActiveProjection> projection(UUID casterId) {
        Objects.requireNonNull(casterId, "casterId");
        ProjectionSession session = projectionsByCaster.get(casterId);
        return session == null ? Optional.empty() : Optional.of(session.snapshot());
    }

    public synchronized List<ActiveProjection> activeProjections() {
        return projectionsByCaster.values().stream().map(ProjectionSession::snapshot).toList();
    }

    public synchronized int activeCount() {
        return projectionsByCaster.size();
    }

    /**
     * Accepts an explicit return only when both the caster and the server-authored projection identity match.
     * A stale, replayed or foreign handle is a no-op.
     */
    public synchronized boolean requestReturn(UUID casterId, UUID projectionId) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(projectionId, "projectionId");
        ProjectionSession session = projectionsByCaster.get(casterId);
        if (session == null || !session.projectionId.equals(projectionId)) {
            return false;
        }
        return close(casterId, CloseReason.EXPLICIT_RETURN);
    }

    public synchronized boolean close(UUID casterId, CloseReason reason) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(reason, "reason");
        ProjectionSession session = projectionsByCaster.remove(casterId);
        return session != null && session.close(reason);
    }

    public synchronized int expire(long nowTick) {
        if (nowTick < 0L) {
            throw new IllegalArgumentException("Astral projection tick must be non-negative");
        }
        List<UUID> expiredCasters = new ArrayList<>();
        for (Map.Entry<UUID, ProjectionSession> entry : projectionsByCaster.entrySet()) {
            if (entry.getValue().expiredAt(nowTick)) {
                expiredCasters.add(entry.getKey());
            }
        }
        int closed = 0;
        for (UUID casterId : expiredCasters) {
            if (close(casterId, CloseReason.EXPIRED)) {
                closed++;
            }
        }
        return closed;
    }

    public synchronized int clearForServerStop() {
        List<ProjectionSession> sessions = new ArrayList<>(projectionsByCaster.values());
        projectionsByCaster.clear();
        int closed = 0;
        for (ProjectionSession session : sessions) {
            if (session.close(CloseReason.SERVER_STOP)) {
                closed++;
            }
        }
        return closed;
    }

    public record ActiveProjection(
            UUID projectionId,
            UUID casterId,
            UUID physicalBodyId,
            long startedAtTick,
            long expiresAtTick,
            double maxRangeBlocks
    ) {
        public ActiveProjection {
            Objects.requireNonNull(projectionId, "projectionId");
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(physicalBodyId, "physicalBodyId");
            if (!casterId.equals(physicalBodyId)) {
                throw new IllegalArgumentException("Astral projection physical body must remain the canonical caster");
            }
            if (startedAtTick < 0L || expiresAtTick <= startedAtTick) {
                throw new IllegalArgumentException("Astral projection tick bounds are invalid");
            }
            if (!Double.isFinite(maxRangeBlocks)
                    || maxRangeBlocks <= 0.0D
                    || maxRangeBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
                throw new IllegalArgumentException("Astral projection range is outside the hard Noetic ceiling");
            }
        }
    }

    private static final class ProjectionSession {
        private final UUID casterId;
        private final UUID projectionId;
        private final long startedAtTick;
        private final long expiresAtTick;
        private final double maxRangeBlocks;
        private CloseReason closeReason;

        private ProjectionSession(
                UUID casterId,
                UUID projectionId,
                long startedAtTick,
                long expiresAtTick,
                double maxRangeBlocks
        ) {
            this.casterId = Objects.requireNonNull(casterId, "casterId");
            this.projectionId = Objects.requireNonNull(projectionId, "projectionId");
            this.startedAtTick = startedAtTick;
            this.expiresAtTick = expiresAtTick;
            this.maxRangeBlocks = maxRangeBlocks;
        }

        private boolean expiredAt(long tick) {
            return tick >= expiresAtTick;
        }

        private synchronized boolean close(CloseReason reason) {
            Objects.requireNonNull(reason, "reason");
            if (closeReason != null) {
                return false;
            }
            closeReason = reason;
            return true;
        }

        private ActiveProjection snapshot() {
            return new ActiveProjection(
                    projectionId,
                    casterId,
                    casterId,
                    startedAtTick,
                    expiresAtTick,
                    maxRangeBlocks);
        }
    }
}
