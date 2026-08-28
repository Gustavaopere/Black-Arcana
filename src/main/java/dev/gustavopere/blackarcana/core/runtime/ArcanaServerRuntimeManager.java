package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.config.SpellDataDefinition;
import dev.gustavopere.blackarcana.core.registry.SpellDataCatalog;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.CooldownSnapshotPayload;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.ServerPlayerArcanaContext;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
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
    private static volatile List<SpellDataDefinition> CURRENT_SPELL_DATA = List.of();

    private ArcanaServerRuntimeManager() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStarted);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerTick);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStopping);
        gameBus.addListener(ArcanaServerRuntimeManager::onServerStopped);
        gameBus.addListener(ArcanaServerRuntimeManager::onPlayerLoggedIn);
    }

    /** Integrations may register bootstrap logic before the server starts. */
    public static void addInitializer(Consumer<ArcanaServerRuntime> initializer) {
        INITIALIZERS.add(Objects.requireNonNull(initializer, "initializer"));
    }

    /**
     * Atomically validates a datapack metadata snapshot before publishing it to
     * current and future server runtimes. Gameplay implementation is not data-driven here.
     */
    public static void reloadSpellData(Collection<SpellDataDefinition> definitions) {
        Objects.requireNonNull(definitions, "definitions");
        SpellDataCatalog validator = new SpellDataCatalog();
        validator.replaceAll(definitions);
        List<SpellDataDefinition> validated = List.copyOf(validator.snapshot().values());

        CURRENT_SPELL_DATA = validated;
        synchronized (RUNTIMES) {
            RUNTIMES.forEach((server, runtime) -> {
                runtime.spellData().replaceAll(validated);
                var presentation = runtime.spellData().presentationPayload();
                server.getPlayerList().getPlayers().forEach(player ->
                        ArcanaNetworkBridge.sendSpellPresentation(player, presentation));
            });
        }
    }

    public static List<SpellDataDefinition> currentSpellDataSnapshot() {
        return CURRENT_SPELL_DATA;
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

        CastResultPayload result = runtime.handle(ServerPlayerArcanaContext.from(player), intent);
        if (ArcanaCastResult.Status.SUCCESS.name().equals(result.status())) {
            ArcanaNetworkBridge.sendCooldownSnapshot(
                    player,
                    cooldownSnapshot(runtime, player, server.overworld().getGameTime()));
        }
        return result;
    }

    private static void onServerStarted(ServerStartedEvent event) {
        MinecraftServer server = event.getServer();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        INITIALIZERS.forEach(initializer -> initializer.accept(runtime));
        runtime.spellData().replaceAll(CURRENT_SPELL_DATA);
        BlackArcanaSavedData.get(server).restore(
                runtime.cooldowns(), runtime.charges(), runtime.loadouts(), server.overworld().getGameTime());
        runtime.pruneOrphanedPersistentState();
        RUNTIMES.put(server, runtime);
    }

    private static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        MinecraftServer server = player.serverLevel().getServer();
        ArcanaServerRuntime runtime = RUNTIMES.get(server);
        if (runtime == null) return;

        ArcanaNetworkBridge.sendSpellPresentation(player, runtime.spellData().presentationPayload());
        ArcanaNetworkBridge.sendCooldownSnapshot(
                player,
                cooldownSnapshot(runtime, player, server.overworld().getGameTime()));
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        long now = server.overworld().getGameTime();
        ArcanaServerRuntime runtime = RUNTIMES.get(server);
        if (runtime != null) runtime.tick(now);
        if (now % PERSIST_INTERVAL_TICKS == 0L) persist(server, now);
    }

    private static void onServerStopping(ServerStoppingEvent event) {
        MinecraftServer server = event.getServer();
        persist(server, server.overworld().getGameTime());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        RUNTIMES.remove(event.getServer());
    }

    private static CooldownSnapshotPayload cooldownSnapshot(
            ArcanaServerRuntime runtime,
            ServerPlayer player,
            long now
    ) {
        List<CooldownSnapshotPayload.Entry> entries = runtime.cooldowns()
                .remainingSnapshot(player.getUUID(), now, ArcanaProtocol.MAX_COOLDOWN_ENTRIES)
                .entrySet().stream()
                .sorted(Map.Entry.comparingByKey(Comparator.naturalOrder()))
                .map(entry -> new CooldownSnapshotPayload.Entry(entry.getKey(), entry.getValue()))
                .toList();
        return new CooldownSnapshotPayload(ArcanaProtocol.VERSION, entries);
    }

    private static void persist(MinecraftServer server, long now) {
        ArcanaServerRuntime runtime = RUNTIMES.get(server);
        if (runtime == null) return;
        BlackArcanaSavedData.get(server).capture(
                runtime.cooldowns(), runtime.charges(), runtime.loadouts(), now);
    }
}
