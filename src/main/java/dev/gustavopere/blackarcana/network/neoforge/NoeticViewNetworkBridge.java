package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import net.minecraft.world.entity.player.Player;

import java.util.Objects;

/** Clientbound-only presentation bridge for validated Borrowed Sight instructions. */
public final class NoeticViewNetworkBridge {
    private static volatile ClientHandler clientHandler = (player, payload) -> { };

    private NoeticViewNetworkBridge() {
    }

    public static void installClientHandler(ClientHandler handler) {
        clientHandler = Objects.requireNonNull(handler, "handler");
    }

    public static void dispatchClientbound(Player player, NoeticViewPayload payload) {
        clientHandler.handle(player, Objects.requireNonNull(payload, "payload"));
    }

    @FunctionalInterface
    public interface ClientHandler {
        void handle(Player player, NoeticViewPayload payload);
    }
}
