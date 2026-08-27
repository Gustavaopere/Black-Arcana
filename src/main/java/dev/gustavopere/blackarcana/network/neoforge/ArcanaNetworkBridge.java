package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;
import java.util.function.BiConsumer;

/**
 * Narrow NeoForge transport bridge. It knows packet registration and logical-side
 * players, but delegates gameplay execution to Black Arcana-owned runtime code.
 */
public final class ArcanaNetworkBridge {
    @FunctionalInterface
    public interface ServerCastIntentHandler {
        CastResultPayload handle(ServerPlayer player, CastIntentPayload intent);
    }

    private static volatile ServerCastIntentHandler serverHandler = ArcanaNetworkBridge::notReady;
    private static volatile BiConsumer<Player, CastResultPayload> clientResultHandler = (player, result) -> { };

    private ArcanaNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(CastIntentPacket.TYPE, CastIntentPacket.STREAM_CODEC, ArcanaNetworkBridge::handleServerbound);
        registrar.playToClient(CastResultPacket.TYPE, CastResultPacket.STREAM_CODEC, ArcanaNetworkBridge::handleClientbound);
    }

    public static void installServerHandler(ServerCastIntentHandler handler) {
        serverHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientResultHandler(BiConsumer<Player, CastResultPayload> handler) {
        clientResultHandler = Objects.requireNonNull(handler, "handler");
    }

    private static void handleServerbound(CastIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) {
            return;
        }
        CastResultPayload result = Objects.requireNonNull(
                serverHandler.handle(player, packet.toDomain()), "server cast result");
        context.reply(CastResultPacket.from(result));
    }

    private static void handleClientbound(CastResultPacket packet, IPayloadContext context) {
        clientResultHandler.accept(context.player(), packet.toDomain());
    }

    private static CastResultPayload notReady(ServerPlayer player, CastIntentPayload intent) {
        ArcanaCastResult result = ArcanaCastResult.denied(
                ArcanaCastResult.Status.DENIED_IDENTITY,
                dev.gustavopere.blackarcana.api.ArcanaDecision.deny(
                        "server_runtime_unavailable",
                        "Black Arcana cast runtime is not installed yet"));
        return CastResultPayload.from(intent.parsedCastId(), result);
    }
}
