package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastRequestPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;
import java.util.function.BiConsumer;

/** Narrow transport for bounded, presentation-only Arcane Resistance forecast requests. */
public final class HazardResistanceForecastNetworkBridge {
    @FunctionalInterface
    public interface ServerHandler {
        HazardResistanceForecastPayload handle(ServerPlayer player, HazardResistanceForecastRequestPayload request);
    }

    private static volatile ServerHandler serverHandler = HazardResistanceForecastNetworkBridge::unavailable;
    private static volatile BiConsumer<Player, HazardResistanceForecastPayload> clientHandler = (player, payload) -> { };

    private HazardResistanceForecastNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(
            HazardResistanceForecastRequestPacket.TYPE,
            HazardResistanceForecastRequestPacket.STREAM_CODEC,
            HazardResistanceForecastNetworkBridge::handleServerbound);
        registrar.playToClient(
            HazardResistanceForecastPacket.TYPE,
            HazardResistanceForecastPacket.STREAM_CODEC,
            HazardResistanceForecastNetworkBridge::handleClientbound);
    }

    public static void installServerHandler(ServerHandler handler) {
        serverHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientHandler(BiConsumer<Player, HazardResistanceForecastPayload> handler) {
        clientHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void request(HazardResistanceForecastRequestPayload request) {
        PacketDistributor.sendToServer(HazardResistanceForecastRequestPacket.from(
            Objects.requireNonNull(request, "request")));
    }

    private static void handleServerbound(HazardResistanceForecastRequestPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        HazardResistanceForecastPayload response = Objects.requireNonNull(
            serverHandler.handle(player, packet.toDomain()), "hazard resistance forecast");
        context.reply(HazardResistanceForecastPacket.from(response));
    }

    private static void handleClientbound(HazardResistanceForecastPacket packet, IPayloadContext context) {
        clientHandler.accept(context.player(), packet.toDomain());
    }

    private static HazardResistanceForecastPayload unavailable(
        ServerPlayer player,
        HazardResistanceForecastRequestPayload request
    ) {
        return new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            request.requestId(),
            request.spellId(),
            false,
            HazardResistanceForecastPayload.Status.UNAVAILABLE.name(),
            dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier.NORMAL.name(),
            0.0D,
            0.0D,
            0.0D);
    }
}
