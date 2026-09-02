package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.souls.SpiritSightPolicy;
import dev.gustavopere.blackarcana.content.souls.SpiritTraceProvider;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Server-authoritative, provider-backed Spirit Sight runtime. */
public final class MinecraftSpiritSightRuntime {
    public static final int ABSOLUTE_MAX_PROVIDERS = 32;
    public static final int ABSOLUTE_MAX_SESSIONS = 4096;
    public static final int ABSOLUTE_MAX_VISIBLE_TRACES = 256;

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());
    private static final SpiritSightPolicy VISIBILITY_POLICY = new SpiritSightPolicy();

    private MinecraftSpiritSightRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftSpiritSightRuntime::onServerStarted);
        gameBus.addListener(MinecraftSpiritSightRuntime::onServerTick);
        gameBus.addListener(MinecraftSpiritSightRuntime::onServerStopped);
    }

    public static ArcanaDecision registerProvider(MinecraftServer server, SpiritTraceProvider provider) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(provider, "provider");
        ServerState state = stateForRegistration(server);
        String providerId = provider.providerId();
        if (!SpiritTraceProvider.validProviderId(providerId)) {
            return ArcanaDecision.deny(
                "spirit_sight_provider_id_invalid",
                "Spirit Sight provider id must be a bounded namespaced identifier");
        }
        synchronized (state) {
            if (!state.providers.containsKey(providerId) && state.providers.size() >= ABSOLUTE_MAX_PROVIDERS) {
                return ArcanaDecision.deny(
                    "spirit_sight_provider_capacity",
                    "Spirit Sight provider registry reached its bounded capacity");
            }
            state.providers.put(providerId, provider);
        }
        return ArcanaDecision.allow();
    }

    public static boolean unregisterProvider(MinecraftServer server, String providerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(providerId, "providerId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        synchronized (state) {
            return state.providers.remove(providerId) != null;
        }
    }

    public static ArcanaDecision activate(
        MinecraftServer server,
        UUID casterId,
        SpiritSightPolicy.Policy policy
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(policy, "policy");
        ServerState state = STATES.get(server);
        if (state == null) {
            return ArcanaDecision.deny(
                "spirit_sight_runtime_unavailable",
                "Spirit Sight runtime is unavailable on this server");
        }
        LivingEntity caster = findLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive()) {
            return ArcanaDecision.deny(
                "spirit_sight_caster_unavailable",
                "Spirit Sight requires a loaded living caster");
        }
        long nowTick = server.overworld().getGameTime();
        long expiresAtTick = saturatingAdd(nowTick, policy.durationTicks());
        synchronized (state) {
            state.pruneExpired(nowTick);
            if (!state.sessions.containsKey(casterId) && state.sessions.size() >= ABSOLUTE_MAX_SESSIONS) {
                return ArcanaDecision.deny(
                    "spirit_sight_session_capacity",
                    "Spirit Sight session registry reached its bounded capacity");
            }
            state.sessions.put(casterId, new Session(policy, expiresAtTick));
        }
        return ArcanaDecision.allow();
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

    public static List<SpiritTraceProvider.Trace> visibleTraces(MinecraftServer server, UUID casterId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        ServerState state = STATES.get(server);
        if (state == null) return List.of();

        long nowTick = server.overworld().getGameTime();
        Session session;
        List<SpiritTraceProvider> providers;
        synchronized (state) {
            state.pruneExpired(nowTick);
            session = state.sessions.get(casterId);
            if (session == null) return List.of();
            providers = List.copyOf(state.providers.values());
        }

        LivingEntity caster = findLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            synchronized (state) {
                state.sessions.remove(casterId);
            }
            return List.of();
        }

        SpiritTraceProvider.Query query = new SpiritTraceProvider.Query(
            casterId,
            level.dimension().location().toString(),
            caster.getX(),
            caster.getY(),
            caster.getZ(),
            session.policy.radius());
        List<SpiritTraceProvider.Trace> visible = new ArrayList<>();
        for (SpiritTraceProvider provider : providers) {
            List<SpiritTraceProvider.Trace> traces;
            try {
                traces = provider.query(query);
            } catch (RuntimeException ignored) {
                continue;
            }
            if (traces == null || traces.isEmpty()) continue;
            for (SpiritTraceProvider.Trace trace : traces) {
                if (trace == null) continue;
                double dx = trace.x() - query.x();
                double dy = trace.y() - query.y();
                double dz = trace.z() - query.z();
                double distanceSquared = dx * dx + dy * dy + dz * dz;
                if (!Double.isFinite(distanceSquared)) continue;
                SpiritSightPolicy.TraceView traceView = new SpiritSightPolicy.TraceView(
                    distanceSquared,
                    trace.kind(),
                    true,
                    trace.privateData());
                if (!VISIBILITY_POLICY.visible(session.policy, traceView)) continue;
                visible.add(trace);
                if (visible.size() >= ABSOLUTE_MAX_VISIBLE_TRACES) {
                    return List.copyOf(visible);
                }
            }
        }
        return List.copyOf(visible);
    }

    private static ServerState stateForRegistration(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        stateForRegistration(event.getServer());
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        ServerState state = STATES.get(event.getServer());
        if (state == null) return;
        long nowTick = event.getServer().overworld().getGameTime();
        synchronized (state) {
            state.pruneExpired(nowTick);
        }
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
        private final Map<String, SpiritTraceProvider> providers = new HashMap<>();
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

    private record Session(SpiritSightPolicy.Policy policy, long expiresAtTick) {
        private Session {
            Objects.requireNonNull(policy, "policy");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
        }
    }
}
