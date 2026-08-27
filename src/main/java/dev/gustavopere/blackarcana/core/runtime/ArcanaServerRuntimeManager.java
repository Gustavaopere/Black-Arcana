package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.neoforge.ServerPlayerArcanaContext;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

/** Owns exactly one Black Arcana runtime per live MinecraftServer instance. */
public final class ArcanaServerRuntimeManager {
    private static final long PERSIST_INTERVAL_TICKS = 200L;
    private static final Map<MinecraftServer, ArcanaServerRuntime> RUNTIMES =
            Collections.synchronizedMap(new IdentityHashMap<>());
    private static final List<Consumer<ArcanaServerRuntime>> INITIALIZERS = new CopyOnWriteArrayList<>();

    private ArcanaServerRuntimeManager() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStarted);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerTick);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStopping);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStopped);
    }

    /** Integrations may register bootstrap logic before the server starts. */
    public static void addInitializer(Consumer<ArcanaServerRuntime> initializer) {
        INITIALIZERS.add(Objects.requireNonNull(initializer, "initializer"));
    }

    public static Optional<ArcanaServerRuntime> get(MinecraftServer server) {
        return Optional.ofNullable(RUNTIMES.get(Objects.requireNonNull(server, "server")));
    }

    public static CastResultPayload handleCastIntent(ServerPlayer player, CastIntentPayload intent) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(intent, "intent");
        MinecraftServer server = player.serverLevel().getServer();
        ArcanaServerRuntime runtime = RUNTIMES.get(server);
        if (runtime == null) {
            return CastResultPayload.from(intent.parsedCastId(), ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_IDENTITY,
                    ArcanaDecision.deny("server_runtime_unavailable", "Black Arcana server runtime is not active")));
        }
        return runtime.handle(ServerPlayerArcanaContext.from(player), intent);
    }

    private static void onServerStarted(ServerStartedEvent event) {
        MinecraftServer server = event.getServer();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        INITIALIZERS.forEach(initializer -> initializer.accept(runtime));
        BlackArcanaSavedData.get(server).restore(
                runtime.cooldowns(), runtime.charges(), runtime.loadouts(), server.overworld().getGameTime());
        runtime.pruneOrphanedPersistentState();
        RUNTIMES.put(server, runtime);
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        long now = server.overworld().getGameTime();
        if (now % PERSIST_INTERVAL_TICKS != 0L) return;
        persist(server, now);
    }

    private static void onServerStopping(ServerStoppingEvent event) {
        MinecraftServer server = event.getServer();
        persist(server, server.overworld().getGameTime());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        RUNTIMES.remove(event.getServer());
    }

    private static void persist(MinecraftServer server, long now) {
        ArcanaServerRuntime runtime = RUNTIMES.get(server);
        if (runtime == null) return;
        BlackArcanaSavedData.get(server).capture(
                runtime.cooldowns(), runtime.charges(), runtime.loadouts(), now);
    }
}
