package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import dev.gustavopere.blackarcana.network.AstralReturnIntentPayload;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Collections;
import java.util.Map;
import java.util.Objects;
import java.util.WeakHashMap;

/**
 * Narrow Astral Severance transport.
 *
 * <p>Caster identity for C2S control is derived exclusively from {@link IPayloadContext#player()}. The client
 * never supplies caster identity or an authoritative position. S2C view instructions are presentation-only
 * and carry the exact server-authored projection UUID plus its transient loaded entity id.</p>
 */
public final class AstralSeveranceNetworkBridge {
    static final int MAX_MOVE_INTENTS_PER_TICK = 1;
    static final int MAX_RETURN_INTENTS_PER_TICK = 1;

    /**
     * Network bridge lifetime is JVM-wide while server ticks are world/server-local. Keep limiter histories
     * scoped to the concrete MinecraftServer so an integrated-server restart or another server instance cannot
     * inherit a larger prior tick and fail every request as clock regression. Weak keys avoid retaining a
     * stopped server solely for transport abuse accounting.
     */
    private static final Map<MinecraftServer, ServerIngress> INGRESS_BY_SERVER =
            Collections.synchronizedMap(new WeakHashMap<>());

    private static volatile MoveHandler moveHandler = (player, payload) ->
            AstralSeveranceRuntime.ControlResult.INVALID_INTENT;
    private static volatile ReturnHandler returnHandler = (player, payload) -> false;
    private static volatile ViewHandler viewHandler = (player, payload) -> { };

    private AstralSeveranceNetworkBridge() { }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar(Integer.toString(ArcanaProtocol.VERSION));
        registrar.playToServer(
                AstralMoveIntentPacket.TYPE,
                AstralMoveIntentPacket.STREAM_CODEC,
                AstralSeveranceNetworkBridge::handleMove);
        registrar.playToServer(
                AstralReturnIntentPacket.TYPE,
                AstralReturnIntentPacket.STREAM_CODEC,
                AstralSeveranceNetworkBridge::handleReturn);
        registrar.playToClient(
                AstralViewPacket.TYPE,
                AstralViewPacket.STREAM_CODEC,
                AstralSeveranceNetworkBridge::handleView);
    }

    public static void installMoveHandler(MoveHandler handler) {
        moveHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installReturnHandler(ReturnHandler handler) {
        returnHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installViewHandler(ViewHandler handler) {
        viewHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void sendMove(AstralMoveIntentPayload payload) {
        PacketDistributor.sendToServer(AstralMoveIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static void sendReturn(AstralReturnIntentPayload payload) {
        PacketDistributor.sendToServer(AstralReturnIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static boolean sendView(ServerPlayer player, AstralViewPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");
        if (!player.connection.hasChannel(AstralViewPacket.TYPE)) return false;
        PacketDistributor.sendToPlayer(player, AstralViewPacket.from(payload));
        return true;
    }

    public static void dispatchViewClientbound(Player player, AstralViewPayload payload) {
        viewHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    private static void handleMove(AstralMoveIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        if (!claimMoveIngress(player).allowed()) return;
        moveHandler.handle(player, packet.toDomain());
    }

    private static void handleReturn(AstralReturnIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        if (!claimReturnIngress(player).allowed()) return;
        returnHandler.handle(player, packet.toDomain());
    }

    private static void handleView(AstralViewPacket packet, IPayloadContext context) {
        dispatchViewClientbound(context.player(), packet.toDomain());
    }

    private static ArcanaDecision claimMoveIngress(ServerPlayer player) {
        return ingressFor(player).move().claim(player.getUUID(), player.serverLevel().getGameTime());
    }

    private static ArcanaDecision claimReturnIngress(ServerPlayer player) {
        return ingressFor(player).returns().claim(player.getUUID(), player.serverLevel().getGameTime());
    }

    private static ServerIngress ingressFor(ServerPlayer player) {
        MinecraftServer server = player.serverLevel().getServer();
        synchronized (INGRESS_BY_SERVER) {
            return INGRESS_BY_SERVER.computeIfAbsent(server, ignored -> ServerIngress.create());
        }
    }

    private record ServerIngress(IngressRateLimiter move, IngressRateLimiter returns) {
        private static ServerIngress create() {
            return new ServerIngress(
                    new IngressRateLimiter(
                            MAX_MOVE_INTENTS_PER_TICK,
                            1L,
                            ArcanaServerRuntime.DEFAULT_MAX_TRACKED_CASTERS),
                    new IngressRateLimiter(
                            MAX_RETURN_INTENTS_PER_TICK,
                            1L,
                            ArcanaServerRuntime.DEFAULT_MAX_TRACKED_CASTERS));
        }
    }

    @FunctionalInterface
    public interface MoveHandler {
        AstralSeveranceRuntime.ControlResult handle(ServerPlayer player, AstralMoveIntentPayload payload);
    }

    @FunctionalInterface
    public interface ReturnHandler {
        boolean handle(ServerPlayer player, AstralReturnIntentPayload payload);
    }

    @FunctionalInterface
    public interface ViewHandler {
        void handle(Player player, AstralViewPayload payload);
    }
}
