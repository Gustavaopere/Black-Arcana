package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;
import java.util.function.BiConsumer;

/** Transport-only bridge for server-authored Noetic camera presentation. */
public final class NoeticViewNetworkBridge {
    private static volatile BiConsumer<Player, NoeticViewPayload> clientHandler = (player, payload) -> { };

    private NoeticViewNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToClient(
                NoeticViewPacket.TYPE,
                NoeticViewPacket.STREAM_CODEC,
                NoeticViewNetworkBridge::handleClientbound);
    }

    public static void installClientHandler(BiConsumer<Player, NoeticViewPayload> handler) {
        clientHandler = Objects.requireNonNull(handler, "handler");
    }

    public static boolean send(ServerPlayer player, NoeticViewPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");
        if (!player.connection.hasChannel(NoeticViewPacket.TYPE)) return false;
        PacketDistributor.sendToPlayer(player, NoeticViewPacket.from(payload));
        return true;
    }

    static void dispatchClientbound(Player player, NoeticViewPayload payload) {
        clientHandler.accept(player, Objects.requireNonNull(payload, "payload"));
    }

    private static void handleClientbound(NoeticViewPacket packet, IPayloadContext context) {
        dispatchClientbound(context.player(), packet.toDomain());
    }
}
