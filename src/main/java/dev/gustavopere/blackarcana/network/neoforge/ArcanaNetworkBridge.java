package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.CooldownSnapshotPayload;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;
import java.util.function.BiConsumer;

/**
 * Narrow NeoForge transport bridge. It knows packet registration and logical-side
 * players, but delegates gameplay execution and client presentation to installed handlers.
 */
public final class ArcanaNetworkBridge {
    @FunctionalInterface
    public interface ServerCastIntentHandler {
        CastResultPayload handle(ServerPlayer player, CastIntentPayload intent);
    }

    private static volatile ServerCastIntentHandler serverHandler = ArcanaNetworkBridge::notReady;
    private static volatile BiConsumer<Player, CastResultPayload> clientResultHandler = (player, result) -> { };
    private static volatile BiConsumer<Player, CooldownSnapshotPayload> clientCooldownHandler = (player, snapshot) -> { };
    private static volatile BiConsumer<Player, SpellPresentationPayload> clientPresentationHandler = (player, presentation) -> { };
    private static volatile BiConsumer<Player, HazardPreflightPayload> clientHazardPreflightHandler = (player, preflight) -> { };

    private ArcanaNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(CastIntentPacket.TYPE, CastIntentPacket.STREAM_CODEC, ArcanaNetworkBridge::handleServerbound);
        registrar.playToClient(CastResultPacket.TYPE, CastResultPacket.STREAM_CODEC, ArcanaNetworkBridge::handleCastResult);
        registrar.playToClient(CooldownSnapshotPacket.TYPE, CooldownSnapshotPacket.STREAM_CODEC, ArcanaNetworkBridge::handleCooldownSnapshot);
        registrar.playToClient(SpellPresentationPacket.TYPE, SpellPresentationPacket.STREAM_CODEC, ArcanaNetworkBridge::handleSpellPresentation);
        registrar.playToClient(HazardPreflightPacket.TYPE, HazardPreflightPacket.STREAM_CODEC, ArcanaNetworkBridge::handleHazardPreflight);
    }

    public static void installServerHandler(ServerCastIntentHandler handler) {
        serverHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientResultHandler(BiConsumer<Player, CastResultPayload> handler) {
        clientResultHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientCooldownHandler(BiConsumer<Player, CooldownSnapshotPayload> handler) {
        clientCooldownHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientPresentationHandler(BiConsumer<Player, SpellPresentationPayload> handler) {
        clientPresentationHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installClientHazardPreflightHandler(BiConsumer<Player, HazardPreflightPayload> handler) {
        clientHazardPreflightHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void sendCastIntent(CastIntentPayload intent) {
        PacketDistributor.sendToServer(CastIntentPacket.from(Objects.requireNonNull(intent, "intent")));
    }

    public static void sendCooldownSnapshot(ServerPlayer player, CooldownSnapshotPayload snapshot) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(snapshot, "snapshot");
        if (!player.connection.hasChannel(CooldownSnapshotPacket.TYPE)) return;
        PacketDistributor.sendToPlayer(player, CooldownSnapshotPacket.from(snapshot));
    }

    public static void sendSpellPresentation(ServerPlayer player, SpellPresentationPayload presentation) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(presentation, "presentation");
        if (!player.connection.hasChannel(SpellPresentationPacket.TYPE)) return;
        PacketDistributor.sendToPlayer(player, SpellPresentationPacket.from(presentation));
    }

    public static void sendHazardPreflight(ServerPlayer player, HazardPreflightPayload preflight) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(preflight, "preflight");
        if (!player.connection.hasChannel(HazardPreflightPacket.TYPE)) return;
        PacketDistributor.sendToPlayer(player, HazardPreflightPacket.from(preflight));
    }

    private static void handleServerbound(CastIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        CastResultPayload result = Objects.requireNonNull(
                serverHandler.handle(player, packet.toDomain()), "server cast result");
        context.reply(CastResultPacket.from(result));
    }

    private static void handleCastResult(CastResultPacket packet, IPayloadContext context) {
        clientResultHandler.accept(context.player(), packet.toDomain());
    }

    private static void handleCooldownSnapshot(CooldownSnapshotPacket packet, IPayloadContext context) {
        clientCooldownHandler.accept(context.player(), packet.toDomain());
    }

    private static void handleSpellPresentation(SpellPresentationPacket packet, IPayloadContext context) {
        clientPresentationHandler.accept(context.player(), packet.toDomain());
    }

    private static void handleHazardPreflight(HazardPreflightPacket packet, IPayloadContext context) {
        clientHazardPreflightHandler.accept(context.player(), packet.toDomain());
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
