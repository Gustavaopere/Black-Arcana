package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;

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

    public static void dispatchBeginResultClientbound(Player player, ChannelBeginResultPayload payload) {
        beginResultHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    public static void dispatchCapabilityClientbound(Player player, ChannelCapabilityPayload payload) {
        capabilityHandler.handle(player, Objects.requireNonNull(payload, "payload"));
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
