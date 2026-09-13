package dev.gustavopere.blackarcana.content.noetic;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.function.Supplier;

/**
 * Bounded server-owned lifecycle for Astral Severance.
 *
 * <p>The runtime owns projection identity plus an ephemeral logical viewpoint. Client input may express only
 * bounded movement/look axes for the exact server-authored projection identity; it never supplies an
 * authoritative world position. The caller owns loaded-region admission and supplies it as a fail-closed
 * predicate, so this class never requests chunks or creates a world entity.</p>
 *
 * <p>Resource, cooldown, progression and cast admission remain outside this class and must continue through
 * the canonical casting/channel pipeline.</p>
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

    public enum ControlResult {
        APPLIED,
        NO_ACTIVE_PROJECTION,
        SESSION_MISMATCH,
        STALE_SEQUENCE,
        INVALID_INTENT,
        OUT_OF_RANGE,
        DESTINATION_UNAVAILABLE
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

    private static final ProjectionPose LEGACY_ORIGIN = new ProjectionPose(0.0D, 0.0D, 0.0D, 0.0F, 0.0F);

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

    /**
     * Compatibility entry point for the pre-viewpoint lifecycle. Production adapters that expose viewpoint
     * state must use the origin-aware overload so no synthetic world origin can become presentation truth.
     */
    public synchronized StartResult start(
            UUID casterId,
            long nowTick,
            int durationTicks,
            double maxRangeBlocks
    ) {
        return start(casterId, nowTick, durationTicks, maxRangeBlocks, LEGACY_ORIGIN);
    }

    public synchronized StartResult start(
            UUID casterId,
            long nowTick,
            int durationTicks,
            double maxRangeBlocks,
            ProjectionPose originPose
    ) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(originPose, "originPose");
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
                new ProjectionSession(
                        casterId,
                        projectionId,
                        nowTick,
                        expiresAtTick,
                        maxRangeBlocks,
                        originPose));
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
     * Applies one exact-session bounded control intent to the server-owned logical viewpoint.
     *
     * <p>Rejected range/unavailable-destination intents still consume their valid sequence number. This makes
     * replaying a previously refused packet unable to become valid later after world/session state changes.
     * Malformed numeric input is rejected before sequence consumption.</p>
     */
    public synchronized ControlResult applyControl(
            UUID casterId,
            ControlIntent intent,
            ControlLimits limits,
            Predicate<ProjectionPose> destinationAvailable
    ) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(intent, "intent");
        Objects.requireNonNull(limits, "limits");
        Objects.requireNonNull(destinationAvailable, "destinationAvailable");

        ProjectionSession session = projectionsByCaster.get(casterId);
        if (session == null) {
            return ControlResult.NO_ACTIVE_PROJECTION;
        }
        if (!session.projectionId.equals(intent.projectionId())) {
            return ControlResult.SESSION_MISMATCH;
        }
        if (!intent.valid()) {
            return ControlResult.INVALID_INTENT;
        }
        if (intent.sequence() <= session.lastProcessedControlSequence) {
            return ControlResult.STALE_SEQUENCE;
        }

        ProjectionPose candidate = session.candidatePose(intent, limits);
        session.lastProcessedControlSequence = intent.sequence();

        if (session.originPose.distanceSquared(candidate)
                > session.maxRangeBlocks * session.maxRangeBlocks + 1.0E-9D) {
            return ControlResult.OUT_OF_RANGE;
        }

        final boolean available;
        try {
            available = destinationAvailable.test(candidate);
        } catch (RuntimeException failure) {
            return ControlResult.DESTINATION_UNAVAILABLE;
        }
        if (!available) {
            return ControlResult.DESTINATION_UNAVAILABLE;
        }

        session.pose = candidate;
        return ControlResult.APPLIED;
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

    /** Server-owned logical viewpoint position/rotation. It is never the physical player position. */
    public record ProjectionPose(double x, double y, double z, float yawDegrees, float pitchDegrees) {
        public ProjectionPose {
            if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)
                    || !Float.isFinite(yawDegrees) || !Float.isFinite(pitchDegrees)) {
                throw new IllegalArgumentException("Astral projection pose must be finite");
            }
            if (pitchDegrees < -90.0F || pitchDegrees > 90.0F) {
                throw new IllegalArgumentException("Astral projection pitch must stay within [-90, 90]");
            }
            yawDegrees = wrapDegrees(yawDegrees);
        }

        private double distanceSquared(ProjectionPose other) {
            double dx = other.x - x;
            double dy = other.y - y;
            double dz = other.z - z;
            return dx * dx + dy * dy + dz * dz;
        }
    }

    /**
     * Bounded client intent. The packet-facing layer may transport these axes, but never an authoritative
     * destination coordinate. Sequence identity is scoped to one server-authored projection id.
     */
    public record ControlIntent(
            UUID projectionId,
            long sequence,
            double strafeAxis,
            double verticalAxis,
            double forwardAxis,
            float yawDeltaDegrees,
            float pitchDeltaDegrees
    ) {
        public ControlIntent {
            Objects.requireNonNull(projectionId, "projectionId");
        }

        private boolean valid() {
            return sequence > 0L
                    && finiteUnitAxis(strafeAxis)
                    && finiteUnitAxis(verticalAxis)
                    && finiteUnitAxis(forwardAxis)
                    && Float.isFinite(yawDeltaDegrees)
                    && Float.isFinite(pitchDeltaDegrees);
        }
    }

    /** Server-selected safety limits; these are not spell balance defaults. */
    public record ControlLimits(double maxStepBlocks, float maxLookDeltaDegrees) {
        public ControlLimits {
            if (!Double.isFinite(maxStepBlocks)
                    || maxStepBlocks <= 0.0D
                    || maxStepBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
                throw new IllegalArgumentException("Astral control step is outside the hard Noetic ceiling");
            }
            if (!Float.isFinite(maxLookDeltaDegrees)
                    || maxLookDeltaDegrees <= 0.0F
                    || maxLookDeltaDegrees > 180.0F) {
                throw new IllegalArgumentException("Astral control look delta must be within (0, 180]");
            }
        }
    }

    public record ActiveProjection(
            UUID projectionId,
            UUID casterId,
            UUID physicalBodyId,
            long startedAtTick,
            long expiresAtTick,
            double maxRangeBlocks,
            ProjectionPose originPose,
            ProjectionPose pose,
            long lastProcessedControlSequence
    ) {
        public ActiveProjection {
            Objects.requireNonNull(projectionId, "projectionId");
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(physicalBodyId, "physicalBodyId");
            Objects.requireNonNull(originPose, "originPose");
            Objects.requireNonNull(pose, "pose");
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
            if (lastProcessedControlSequence < 0L) {
                throw new IllegalArgumentException("Astral control sequence must be non-negative");
            }
        }
    }

    private static boolean finiteUnitAxis(double value) {
        return Double.isFinite(value) && value >= -1.0D && value <= 1.0D;
    }

    private static float clamp(float value, float min, float max) {
        return Math.max(min, Math.min(max, value));
    }

    private static float wrapDegrees(float value) {
        float wrapped = value % 360.0F;
        if (wrapped >= 180.0F) wrapped -= 360.0F;
        if (wrapped < -180.0F) wrapped += 360.0F;
        return wrapped;
    }

    private static final class ProjectionSession {
        private final UUID casterId;
        private final UUID projectionId;
        private final long startedAtTick;
        private final long expiresAtTick;
        private final double maxRangeBlocks;
        private final ProjectionPose originPose;
        private ProjectionPose pose;
        private long lastProcessedControlSequence;
        private CloseReason closeReason;

        private ProjectionSession(
                UUID casterId,
                UUID projectionId,
                long startedAtTick,
                long expiresAtTick,
                double maxRangeBlocks,
                ProjectionPose originPose
        ) {
            this.casterId = Objects.requireNonNull(casterId, "casterId");
            this.projectionId = Objects.requireNonNull(projectionId, "projectionId");
            this.startedAtTick = startedAtTick;
            this.expiresAtTick = expiresAtTick;
            this.maxRangeBlocks = maxRangeBlocks;
            this.originPose = Objects.requireNonNull(originPose, "originPose");
            this.pose = originPose;
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

        private ProjectionPose candidatePose(ControlIntent intent, ControlLimits limits) {
            float yawDelta = clamp(
                    intent.yawDeltaDegrees(),
                    -limits.maxLookDeltaDegrees(),
                    limits.maxLookDeltaDegrees());
            float pitchDelta = clamp(
                    intent.pitchDeltaDegrees(),
                    -limits.maxLookDeltaDegrees(),
                    limits.maxLookDeltaDegrees());
            float nextYaw = wrapDegrees(pose.yawDegrees() + yawDelta);
            float nextPitch = clamp(pose.pitchDegrees() + pitchDelta, -90.0F, 90.0F);

            double strafe = intent.strafeAxis();
            double vertical = intent.verticalAxis();
            double forward = intent.forwardAxis();
            double magnitudeSquared = strafe * strafe + vertical * vertical + forward * forward;
            if (magnitudeSquared > 1.0D) {
                double scale = 1.0D / Math.sqrt(magnitudeSquared);
                strafe *= scale;
                vertical *= scale;
                forward *= scale;
            }

            double yawRadians = Math.toRadians(nextYaw);
            double sin = Math.sin(yawRadians);
            double cos = Math.cos(yawRadians);
            double step = limits.maxStepBlocks();
            double worldX = (strafe * cos - forward * sin) * step;
            double worldY = vertical * step;
            double worldZ = (forward * cos + strafe * sin) * step;
            return new ProjectionPose(
                    pose.x() + worldX,
                    pose.y() + worldY,
                    pose.z() + worldZ,
                    nextYaw,
                    nextPitch);
        }

        private ActiveProjection snapshot() {
            return new ActiveProjection(
                    projectionId,
                    casterId,
                    casterId,
                    startedAtTick,
                    expiresAtTick,
                    maxRangeBlocks,
                    originPose,
                    pose,
                    lastProcessedControlSequence);
        }
    }
}
