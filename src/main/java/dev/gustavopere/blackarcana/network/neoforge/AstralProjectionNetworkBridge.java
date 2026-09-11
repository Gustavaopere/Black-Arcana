package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralProjectionMovementIntent;
import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralProjectionViewPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.BiPredicate;

/** Transport-only bridge for the bounded Astral Severance control/viewpoint channel. */
public final class AstralProjectionNetworkBridge {
    private static volatile BiFunction<ServerPlayer, AstralProjectionMovementIntent, AstralSeveranceRuntime.MoveResult>
            serverMoveHandler = (player, intent) -> AstralSeveranceRuntime.MoveResult.NO_ACTIVE_PROJECTION;
    private static volatile BiPredicate<ServerPlayer, UUID> serverReturnHandler = (player, projectionId) -> false;
    private static volatile BiConsumer<Player, AstralProjectionViewPayload> clientViewHandler = (player, payload) -> { };

    private AstralProjectionNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(AstralProjectionMovePacket.TYPE, AstralProjectionMovePacket.STREAM_CODEC,
                AstralProjectionNetworkBridge::handleMove);
        registrar.playToServer(AstralProjectionReturnPacket.TYPE, AstralProjectionReturnPacket.STREAM_CODEC,
                AstralProjectionNetworkBridge::handleReturn);
        registrar.playToClient(AstralProjectionViewPacket.TYPE, AstralProjectionViewPacket.STREAM_CODEC,
                AstralProjectionNetworkBridge::handleView);
    }

    public static void installServerMoveHandler(
            BiFunction<ServerPlayer, AstralProjectionMovementIntent, AstralSeveranceRuntime.MoveResult> handler
    ) {
        serverMoveHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installServerReturnHandler(BiPredicate<ServerPlayer, UUID> handler) {
        serverReturnHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientViewHandler(BiConsumer<Player, AstralProjectionViewPayload> handler) {
        clientViewHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void sendBegin(ServerPlayer player, UUID projectionId, int projectionEntityId) {
        sendView(player, new AstralProjectionViewPayload(
                ArcanaProtocol.VERSION,
                AstralProjectionViewPayload.Action.BEGIN,
                projectionId,
                projectionEntityId));
    }

    public static void sendEnd(ServerPlayer player, UUID projectionId, int projectionEntityId) {
        sendView(player, new AstralProjectionViewPayload(
                ArcanaProtocol.VERSION,
                AstralProjectionViewPayload.Action.END,
                projectionId,
                projectionEntityId));
    }

    public static void sendMove(AstralProjectionMovementIntent intent) {
        PacketDistributor.sendToServer(AstralProjectionMovePacket.from(Objects.requireNonNull(intent, "intent")));
    }

    public static void sendReturn(UUID projectionId) {
        PacketDistributor.sendToServer(AstralProjectionReturnPacket.from(
                Objects.requireNonNull(projectionId, "projectionId")));
    }

    private static void sendView(ServerPlayer player, AstralProjectionViewPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");
        if (!player.connection.hasChannel(AstralProjectionViewPacket.TYPE)) return;
        PacketDistributor.sendToPlayer(player, AstralProjectionViewPacket.from(payload));
    }

    private static void handleMove(AstralProjectionMovePacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        serverMoveHandler.apply(player, packet.toIntent());
    }

    private static void handleReturn(AstralProjectionReturnPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        serverReturnHandler.test(player, packet.projectionId());
    }

    private static void handleView(AstralProjectionViewPacket packet, IPayloadContext context) {
        clientViewHandler.accept(context.player(), packet.toDomain());
    }
}
