package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;

/**
 * Narrow handler seam for the server-owned channel invocation transport.
 *
 * <p>This class deliberately does not define gameplay authority. Server handlers
 * are installed by the runtime layer; client handlers receive only validated
 * server-authored acknowledgement/capability payloads.</p>
 */
public final class ChannelNetworkBridge {
    private static volatile BeginHandler beginHandler = (player, payload) -> {
        throw new IllegalStateException("channel begin handler is not installed");
    };
    private static volatile ReleaseHandler releaseHandler = (player, payload) -> {
        throw new IllegalStateException("channel release handler is not installed");
    };
    private static volatile CancelHandler cancelHandler = (player, payload) -> {
        throw new IllegalStateException("channel cancel handler is not installed");
    };
    private static volatile BeginResultHandler beginResultHandler = (player, payload) -> { };
    private static volatile CapabilityHandler capabilityHandler = (player, payload) -> { };

    private ChannelNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(
                ChannelBeginIntentPacket.TYPE,
                ChannelBeginIntentPacket.STREAM_CODEC,
                ChannelNetworkBridge::handleBegin);
        registrar.playToServer(
                ChannelReleaseIntentPacket.TYPE,
                ChannelReleaseIntentPacket.STREAM_CODEC,
                ChannelNetworkBridge::handleRelease);
        registrar.playToServer(
                ChannelCancelIntentPacket.TYPE,
                ChannelCancelIntentPacket.STREAM_CODEC,
                ChannelNetworkBridge::handleCancel);
        registrar.playToClient(
                ChannelBeginResultPacket.TYPE,
                ChannelBeginResultPacket.STREAM_CODEC,
                ChannelNetworkBridge::handleBeginResult);
        registrar.playToClient(
                ChannelCapabilityPacket.TYPE,
                ChannelCapabilityPacket.STREAM_CODEC,
                ChannelNetworkBridge::handleCapability);
    }

    public static void installBeginHandler(BeginHandler handler) {
        beginHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installReleaseHandler(ReleaseHandler handler) {
        releaseHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installCancelHandler(CancelHandler handler) {
        cancelHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installBeginResultHandler(BeginResultHandler handler) {
        beginResultHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installCapabilityHandler(CapabilityHandler handler) {
        capabilityHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void requestBegin(ChannelBeginIntentPayload payload) {
        PacketDistributor.sendToServer(ChannelBeginIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static void requestRelease(ChannelReleaseIntentPayload payload) {
        PacketDistributor.sendToServer(ChannelReleaseIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static void requestCancel(ChannelCancelIntentPayload payload) {
        PacketDistributor.sendToServer(ChannelCancelIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static boolean sendCapability(ServerPlayer player, ChannelCapabilityPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");
        if (!player.connection.hasChannel(ChannelCapabilityPacket.TYPE)) return false;
        PacketDistributor.sendToPlayer(player, ChannelCapabilityPacket.from(payload));
        return true;
    }

    public static ChannelBeginResultPayload dispatchBeginServerbound(
            ServerPlayer player,
            ChannelBeginIntentPayload payload
    ) {
        return Objects.requireNonNull(
                beginHandler.handle(player, Objects.requireNonNull(payload, "payload")),
                "channel begin result");
    }

    public static CastResultPayload dispatchReleaseServerbound(
            ServerPlayer player,
            ChannelReleaseIntentPayload payload
    ) {
        return Objects.requireNonNull(
                releaseHandler.handle(player, Objects.requireNonNull(payload, "payload")),
                "channel release result");
    }

    public static boolean dispatchCancelServerbound(ServerPlayer player, ChannelCancelIntentPayload payload) {
        return cancelHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    public static void dispatchBeginResultClientbound(Player player, ChannelBeginResultPayload payload) {
        beginResultHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    public static void dispatchCapabilityClientbound(Player player, ChannelCapabilityPayload payload) {
        capabilityHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    private static void handleBegin(ChannelBeginIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        context.reply(ChannelBeginResultPacket.from(dispatchBeginServerbound(player, packet.toDomain())));
    }

    private static void handleRelease(ChannelReleaseIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        context.reply(CastResultPacket.from(dispatchReleaseServerbound(player, packet.toDomain())));
    }

    private static void handleCancel(ChannelCancelIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        dispatchCancelServerbound(player, packet.toDomain());
    }

    private static void handleBeginResult(ChannelBeginResultPacket packet, IPayloadContext context) {
        dispatchBeginResultClientbound(context.player(), packet.toDomain());
    }

    private static void handleCapability(ChannelCapabilityPacket packet, IPayloadContext context) {
        dispatchCapabilityClientbound(context.player(), packet.toDomain());
    }

    @FunctionalInterface
    public interface BeginHandler {
        ChannelBeginResultPayload handle(ServerPlayer player, ChannelBeginIntentPayload payload);
    }

    @FunctionalInterface
    public interface ReleaseHandler {
        CastResultPayload handle(ServerPlayer player, ChannelReleaseIntentPayload payload);
    }

    @FunctionalInterface
    public interface CancelHandler {
        boolean handle(ServerPlayer player, ChannelCancelIntentPayload payload);
    }

    @FunctionalInterface
    public interface BeginResultHandler {
        void handle(Player player, ChannelBeginResultPayload payload);
    }

    @FunctionalInterface
    public interface CapabilityHandler {
        void handle(Player player, ChannelCapabilityPayload payload);
    }
}
