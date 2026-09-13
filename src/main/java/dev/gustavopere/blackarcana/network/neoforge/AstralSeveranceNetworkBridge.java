package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import dev.gustavopere.blackarcana.network.AstralReturnIntentPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.util.Objects;

/**
 * Narrow C2S transport for Astral Severance control intent.
 *
 * <p>Caster identity is derived exclusively from {@link IPayloadContext#player()}. The client never supplies
 * caster identity or an authoritative position. The transport rate cap is a protocol abuse bound, not a
 * spell balance value: at most MOVE plus RETURN may be admitted for one caster in one server tick.</p>
 */
public final class AstralSeveranceNetworkBridge {
    static final int MAX_CONTROL_INTENTS_PER_TICK = 2;
    private static final IngressRateLimiter INGRESS = new IngressRateLimiter(
            MAX_CONTROL_INTENTS_PER_TICK,
            1L,
            NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS);

    private static volatile MoveHandler moveHandler = (player, payload) ->
            AstralSeveranceRuntime.ControlResult.INVALID_INTENT;
    private static volatile ReturnHandler returnHandler = (player, payload) -> false;

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
    }

    public static void installMoveHandler(MoveHandler handler) {
        moveHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void installReturnHandler(ReturnHandler handler) {
        returnHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void sendMove(AstralMoveIntentPayload payload) {
        PacketDistributor.sendToServer(AstralMoveIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    public static void sendReturn(AstralReturnIntentPayload payload) {
        PacketDistributor.sendToServer(AstralReturnIntentPacket.from(Objects.requireNonNull(payload, "payload")));
    }

    private static void handleMove(AstralMoveIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        if (!claimIngress(player).allowed()) return;
        moveHandler.handle(player, packet.toDomain());
    }

    private static void handleReturn(AstralReturnIntentPacket packet, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player)) return;
        if (!claimIngress(player).allowed()) return;
        returnHandler.handle(player, packet.toDomain());
    }

    private static ArcanaDecision claimIngress(ServerPlayer player) {
        return INGRESS.claim(player.getUUID(), player.serverLevel().getGameTime());
    }

    @FunctionalInterface
    public interface MoveHandler {
        AstralSeveranceRuntime.ControlResult handle(ServerPlayer player, AstralMoveIntentPayload payload);
    }

    @FunctionalInterface
    public interface ReturnHandler {
        boolean handle(ServerPlayer player, AstralReturnIntentPayload payload);
    }
}
