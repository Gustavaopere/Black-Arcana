package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.LoadoutSnapshotPayload;
import dev.gustavopere.blackarcana.network.LoadoutUpdatePayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.List;
import java.util.Objects;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;

/** Transport-only bridge for Stage 05 loadout editing/synchronization. */
public final class LoadoutNetworkBridge {
    private static volatile BiFunction<ServerPlayer, LoadoutUpdatePayload, LoadoutSnapshotPayload> serverHandler =
            (player, update) -> new LoadoutSnapshotPayload(ArcanaProtocol.VERSION, List.of());
    private static volatile BiConsumer<Player, LoadoutSnapshotPayload> clientHandler = (player, snapshot) -> { };

    private LoadoutNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(LoadoutUpdatePacket.TYPE, LoadoutUpdatePacket.STREAM_CODEC, LoadoutNetworkBridge::handleServerbound);
        registrar.playToClient(LoadoutSnapshotPacket.TYPE, LoadoutSnapshotPacket.STREAM_CODEC, LoadoutNetworkBridge::handleClientbound);
    }

    public static void installServerHandler(BiFunction<ServerPlayer, LoadoutUpdatePayload, LoadoutSnapshotPayload> handler) {
        serverHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientHandler(BiConsumer<Player, LoadoutSnapshotPayload> handler) {
        clientHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void sendSnapshot(ServerPlayer player, LoadoutSnapshotPayload snapshot) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(snapshot, "snapshot");
        if (!player.connection.hasChannel(LoadoutSnapshotPacket.TYPE)) return;
        PacketDistributor.sendToPlayer(player, LoadoutSnapshotPacket.from(snapshot));
    }

    public static void requestUpdate(LoadoutUpdatePayload update) {
        PacketDistributor.sendToServer(LoadoutUpdatePacket.from(Objects.requireNonNull(update, "update")));
    }

    private static void handleServerbound(LoadoutUpdatePacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        LoadoutSnapshotPayload snapshot = Objects.requireNonNull(
                serverHandler.apply(player, packet.toDomain()), "server loadout snapshot");
        context.reply(LoadoutSnapshotPacket.from(snapshot));
    }

    private static void handleClientbound(LoadoutSnapshotPacket packet, IPayloadContext context) {
        clientHandler.accept(context.player(), packet.toDomain());
    }
}
