package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Server-authoritative bounded control runtime for Gaze of Stillness. */
public final class MinecraftGazeOfStillnessRuntime {
    public static final long MAX_CONTINUOUS_TICKS = 160L;
    public static final long MIN_PLAYER_REAPPLICATION_IMMUNITY_TICKS = 40L;
    public static final double MAX_RANGE_BLOCKS = 128.0D;
    public static final int MAX_ACTIVE_SESSIONS = 4096;
    private static final double MIN_FACING_DOT = 0.5D;

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftGazeOfStillnessRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftGazeOfStillnessRuntime::onServerStarted);
        gameBus.addListener(MinecraftGazeOfStillnessRuntime::onServerTick);
        gameBus.addListener(MinecraftGazeOfStillnessRuntime::onServerStopped);
    }

    public static StartResult start(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            long requestedDurationTicks,
            double maxRange,
            double horizontalMovementMultiplier,
            double playerDurationMultiplier,
            double bossDurationMultiplier,
            long playerImmunityTicks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");

        if (requestedDurationTicks <= 0L || requestedDurationTicks > MAX_CONTINUOUS_TICKS) {
            return StartResult.denied(
                "gaze_stillness_duration",
                "Gaze duration must be positive and no greater than the 160-tick Noetic safety ceiling");
        }
        if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > MAX_RANGE_BLOCKS) {
            return StartResult.denied(
                "gaze_stillness_range_config",
                "Gaze range is outside the generic same-dimension remote safety ceiling");
        }
        if (!unitInterval(horizontalMovementMultiplier)
                || !unitInterval(playerDurationMultiplier)
                || !unitInterval(bossDurationMultiplier)) {
            return StartResult.denied(
                "gaze_stillness_multiplier",
                "Gaze multipliers must be finite values in [0, 1]");
        }
        if (playerImmunityTicks < MIN_PLAYER_REAPPLICATION_IMMUNITY_TICKS) {
            return StartResult.denied(
                "gaze_stillness_player_immunity",
                "Player reapplication immunity cannot be shorter than the 40-tick hard floor");
        }
        if (casterId.equals(targetId)) {
            return StartResult.denied("gaze_stillness_self", "Gaze of Stillness requires a distinct target");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return StartResult.denied("gaze_stillness_caster_unavailable", "Caster must be loaded and alive");
        }
        if (target == null || !target.isAlive() || target.level() != level) {
            return StartResult.denied(
                "gaze_stillness_target_unavailable",
                "Target must be loaded, alive and in the caster dimension");
        }
        if (!withinRange(caster, target, maxRange)) {
            return StartResult.denied("gaze_stillness_range", "Target is outside configured Gaze range");
        }
        if (!reciprocalLineOfSight(caster, target)) {
            return StartResult.denied("gaze_stillness_los", "Gaze requires reciprocal line of sight");
        }
        if (!reciprocalFacing(caster, target)) {
            return StartResult.denied("gaze_stillness_facing", "Gaze requires reciprocal facing");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return StartResult.denied("gaze_stillness_runtime_unavailable", "Black Arcana server runtime is unavailable");
        }
        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, facts);
        if (!authorization.decision().allowed()) {
            return new StartResult(authorization.decision(), 0L);
        }

        double semanticMultiplier = facts.player()
            ? playerDurationMultiplier
            : (facts.boss() ? bossDurationMultiplier : 1.0D);
        long policyDuration = Math.min(requestedDurationTicks, authorization.limits().maxControlTicks());
        long settledDuration = (long) Math.floor(policyDuration * semanticMultiplier);
        if (settledDuration <= 0L) {
            return StartResult.denied(
                "gaze_stillness_control_zero",
                "Target policy reduced Gaze control duration to zero");
        }

        ServerState state = stateFor(server);
        long nowTick = server.overworld().getGameTime();
        synchronized (state) {
            state.pruneImmunity(nowTick);
            Long immunityUntil = state.playerImmunityUntil.get(targetId);
            if (facts.player() && immunityUntil != null && nowTick < immunityUntil) {
                return StartResult.denied(
                    "gaze_stillness_reapplication_immunity",
                    "Player target is inside the server-enforced Gaze reapplication immunity window");
            }
            if (state.sessions.containsKey(targetId)) {
                return StartResult.denied(
                    "gaze_stillness_target_active",
                    "Target already has an active Gaze of Stillness session");
            }
            if (state.sessions.size() >= MAX_ACTIVE_SESSIONS) {
                return StartResult.denied(
                    "gaze_stillness_session_capacity",
                    "Gaze session registry reached its bounded server capacity");
            }
            state.sessions.put(targetId, new Session(
                casterId,
                targetId,
                saturatingAdd(nowTick, settledDuration),
                maxRange,
                horizontalMovementMultiplier,
                playerImmunityTicks));
        }
        return new StartResult(ArcanaDecision.allow(), settledDuration);
    }

    public static boolean isActive(MinecraftServer server, UUID targetId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(targetId, "targetId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        synchronized (state) {
            return state.sessions.containsKey(targetId);
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        stateFor(event.getServer());
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;
        long nowTick = server.overworld().getGameTime();
        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);

        synchronized (state) {
            state.pruneImmunity(nowTick);
            Iterator<Map.Entry<UUID, Session>> iterator = state.sessions.entrySet().iterator();
            while (iterator.hasNext()) {
                Session session = iterator.next().getValue();
                LivingEntity caster = findLoadedLivingEntity(server, session.casterId());
                LivingEntity target = findLoadedLivingEntity(server, session.targetId());

                boolean expired = nowTick >= session.expiresAtTick();
                boolean validEntities = caster != null && target != null
                    && caster.isAlive() && target.isAlive()
                    && caster.level() instanceof ServerLevel
                    && target.level() == caster.level();
                if (expired || !validEntities || runtime == null) {
                    endSession(iterator, state, target, session, nowTick);
                    continue;
                }

                ServerLevel level = (ServerLevel) caster.level();
                if (!withinRange(caster, target, session.maxRange())
                        || !reciprocalLineOfSight(caster, target)
                        || !reciprocalFacing(caster, target)) {
                    endSession(iterator, state, target, session, nowTick);
                    continue;
                }

                EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
                EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, facts);
                if (!authorization.decision().allowed() || authorization.limits().maxControlTicks() <= 0) {
                    endSession(iterator, state, target, session, nowTick);
                    continue;
                }

                Vec3 movement = target.getDeltaMovement();
                target.setDeltaMovement(
                    movement.x * session.horizontalMovementMultiplier(),
                    movement.y,
                    movement.z * session.horizontalMovementMultiplier());
            }
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static void endSession(
            Iterator<Map.Entry<UUID, Session>> iterator,
            ServerState state,
            LivingEntity target,
            Session session,
            long nowTick
    ) {
        iterator.remove();
        if (target instanceof ServerPlayer) {
            state.playerImmunityUntil.put(
                session.targetId(),
                saturatingAdd(nowTick, session.playerImmunityTicks()));
        }
    }

    private static EntityInteractionAuthorization authorize(
            ArcanaServerRuntime runtime,
            ServerLevel level,
            LivingEntity caster,
            LivingEntity target,
            EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.CONTROL,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.CONTROL));
    }

    private static boolean reciprocalLineOfSight(LivingEntity caster, LivingEntity target) {
        return caster.hasLineOfSight(target) && target.hasLineOfSight(caster);
    }

    private static boolean reciprocalFacing(LivingEntity caster, LivingEntity target) {
        return facing(caster, target) && facing(target, caster);
    }

    private static boolean facing(LivingEntity source, LivingEntity target) {
        Vec3 direction = target.getEyePosition().subtract(source.getEyePosition());
        double lengthSquared = direction.lengthSqr();
        if (!Double.isFinite(lengthSquared) || lengthSquared <= 1.0E-12D) return false;
        Vec3 look = source.getLookAngle();
        double dot = look.dot(direction.scale(1.0D / Math.sqrt(lengthSquared)));
        return Double.isFinite(dot) && dot >= MIN_FACING_DOT;
    }

    private static boolean withinRange(LivingEntity caster, LivingEntity target, double maxRange) {
        double distanceSquared = caster.distanceToSqr(target);
        return Double.isFinite(distanceSquared) && distanceSquared <= maxRange * maxRange;
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static boolean unitInterval(double value) {
        return Double.isFinite(value) && value >= 0.0D && value <= 1.0D;
    }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    private static ServerState stateFor(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    private static final class ServerState {
        private final Map<UUID, Session> sessions = new LinkedHashMap<>();
        private final Map<UUID, Long> playerImmunityUntil = new LinkedHashMap<>();

        private void pruneImmunity(long nowTick) {
            playerImmunityUntil.entrySet().removeIf(entry -> nowTick >= entry.getValue());
        }
    }

    private record Session(
            UUID casterId,
            UUID targetId,
            long expiresAtTick,
            double maxRange,
            double horizontalMovementMultiplier,
            long playerImmunityTicks
    ) {
        private Session {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(targetId, "targetId");
        }
    }

    public record StartResult(ArcanaDecision decision, long settledDurationTicks) {
        public StartResult {
            Objects.requireNonNull(decision, "decision");
            if (settledDurationTicks < 0L) {
                throw new IllegalArgumentException("settledDurationTicks cannot be negative");
            }
        }

        private static StartResult denied(String code, String detail) {
            return new StartResult(ArcanaDecision.deny(code, detail), 0L);
        }
    }
}
