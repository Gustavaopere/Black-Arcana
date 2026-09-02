package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.LawOfRecurrenceTracker;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Server-authoritative timed damage adaptation for Law of Recurrence. */
public final class MinecraftLawOfRecurrenceRuntime {
    public static final int DEFAULT_MAX_SESSIONS = LawOfRecurrenceTracker.ABSOLUTE_MAX_TRACKED_CASTERS;

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftLawOfRecurrenceRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftLawOfRecurrenceRuntime::onServerStarted);
        gameBus.addListener(MinecraftLawOfRecurrenceRuntime::onServerTick);
        gameBus.addListener(MinecraftLawOfRecurrenceRuntime::onLivingDamagePre);
        gameBus.addListener(MinecraftLawOfRecurrenceRuntime::onServerStopped);
    }

    public static ArcanaDecision activate(
        MinecraftServer server,
        UUID casterId,
        LawOfRecurrenceTracker.Policy policy
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(policy, "policy");

        ServerState state = STATES.get(server);
        if (state == null) {
            return ArcanaDecision.deny(
                "law_of_recurrence_runtime_unavailable",
                "Law of Recurrence runtime is unavailable on this server");
        }

        LivingEntity caster = findLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive()) {
            return ArcanaDecision.deny(
                "law_of_recurrence_caster_unavailable",
                "Law of Recurrence requires a loaded living caster");
        }

        long nowTick = server.overworld().getGameTime();
        long expiresAtTick = saturatingAdd(nowTick, policy.durationTicks());
        synchronized (state) {
            state.pruneExpired(nowTick);
            if (!state.sessions.containsKey(casterId) && state.sessions.size() >= DEFAULT_MAX_SESSIONS) {
                return ArcanaDecision.deny(
                    "law_of_recurrence_session_capacity",
                    "Law of Recurrence session registry reached its bounded capacity");
            }
            state.sessions.put(casterId, new Session(
                new LawOfRecurrenceTracker(1, policy),
                expiresAtTick));
        }
        return ArcanaDecision.allow();
    }

    public static int activeSessions(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        if (state == null) return 0;
        synchronized (state) {
            return state.sessions.size();
        }
    }

    public static boolean isActive(MinecraftServer server, UUID casterId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        long nowTick = server.overworld().getGameTime();
        synchronized (state) {
            state.pruneExpired(nowTick);
            return state.sessions.containsKey(casterId);
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        STATES.put(event.getServer(), new ServerState());
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        ServerState state = STATES.get(event.getServer());
        if (state == null) return;
        long nowTick = event.getServer().overworld().getGameTime();
        synchronized (state) {
            state.pruneExpired(nowTick);
        }
    }

    private static void onLivingDamagePre(LivingDamageEvent.Pre event) {
        if (!(event.getEntity().level() instanceof ServerLevel level)) return;
        MinecraftServer server = level.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;

        UUID casterId = event.getEntity().getUUID();
        long nowTick = server.overworld().getGameTime();
        Session session;
        synchronized (state) {
            session = state.sessions.get(casterId);
            if (session == null) return;
            if (nowTick >= session.expiresAtTick) {
                state.sessions.remove(casterId);
                return;
            }
        }

        float incomingDamage = event.getNewDamage();
        if (!Float.isFinite(incomingDamage) || incomingDamage <= 0.0F) return;

        String damageFamily = MinecraftDamageFamilyClassifier.classify(event.getSource());
        LawOfRecurrenceTracker.Outcome outcome = session.tracker.observe(casterId, damageFamily, nowTick);
        double adjusted = incomingDamage
            * (1.0D - outcome.resistance())
            * (1.0D + outcome.vulnerability());
        if (!Double.isFinite(adjusted) || adjusted < 0.0D) return;
        event.setNewDamage((float) Math.min(adjusted, Float.MAX_VALUE));
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static LivingEntity findLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    private static final class ServerState {
        private final Map<UUID, Session> sessions = new HashMap<>();

        private void pruneExpired(long nowTick) {
            Iterator<Map.Entry<UUID, Session>> iterator = sessions.entrySet().iterator();
            while (iterator.hasNext()) {
                if (nowTick >= iterator.next().getValue().expiresAtTick) {
                    iterator.remove();
                }
            }
        }
    }

    private record Session(LawOfRecurrenceTracker tracker, long expiresAtTick) {
        private Session {
            Objects.requireNonNull(tracker, "tracker");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
        }
    }
}
