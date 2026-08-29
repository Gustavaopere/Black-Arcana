package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataDefinition;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDangerProfileRuntimeStore;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.Comparator;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Event-driven publication of bounded, server-authored hazard preflight metadata. */
public final class HazardPreflightSyncService {
    private static final Set<MinecraftServer> ACTIVE_SERVERS =
            Collections.newSetFromMap(new IdentityHashMap<>());
    private static volatile HazardPreflightPayload current =
            new HazardPreflightPayload(ArcanaProtocol.VERSION, java.util.List.of());

    private HazardPreflightSyncService() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(HazardPreflightSyncService::onServerStarted);
        gameBus.addListener(HazardPreflightSyncService::onServerStopped);
        gameBus.addListener(HazardPreflightSyncService::onPlayerLoggedIn);
    }

    public static void reload(Map<ArcanaSpellId, ArcaneDangerDataDefinition> definitions) {
        Objects.requireNonNull(definitions, "definitions");
        HazardPreflightPayload next = payloadFor(definitions);

        // Publish gameplay profiles only after the advisory payload has also validated.
        ArcaneDangerProfileRuntimeStore.reload(definitions);
        current = next;
        synchronized (ACTIVE_SERVERS) {
            for (MinecraftServer server : ACTIVE_SERVERS) {
                for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                    ArcanaNetworkBridge.sendHazardPreflight(player, next);
                }
            }
        }
    }

    static HazardPreflightPayload payloadFor(Map<ArcanaSpellId, ArcaneDangerDataDefinition> definitions) {
        return new HazardPreflightPayload(
                ArcanaProtocol.VERSION,
                definitions.entrySet().stream()
                        .sorted(Map.Entry.comparingByKey(Comparator.comparing(ArcanaSpellId::canonical)))
                        .map(entry -> toEntry(entry.getKey(), entry.getValue()))
                        .toList());
    }

    private static HazardPreflightPayload.Entry toEntry(
            ArcanaSpellId spellId,
            ArcaneDangerDataDefinition definition
    ) {
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(definition, "definition");
        if (!spellId.canonical().equals(definition.id())) {
            throw new IllegalArgumentException("danger definition id does not match map key: " + spellId.canonical());
        }
        return new HazardPreflightPayload.Entry(
                definition.id(),
                definition.tier().name(),
                definition.minimumArcaneResistance(),
                definition.recommendedArcaneResistance());
    }

    private static void onServerStarted(ServerStartedEvent event) {
        synchronized (ACTIVE_SERVERS) {
            ACTIVE_SERVERS.add(event.getServer());
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        synchronized (ACTIVE_SERVERS) {
            ACTIVE_SERVERS.remove(event.getServer());
        }
    }

    private static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        ArcanaNetworkBridge.sendHazardPreflight(player, current);
    }
}
