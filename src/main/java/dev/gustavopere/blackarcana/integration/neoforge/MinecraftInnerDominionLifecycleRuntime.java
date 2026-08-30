package dev.gustavopere.blackarcana.integration.neoforge;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;

import java.util.Objects;

/**
 * NeoForge player-lifecycle bridge for pending Inner Dominion return obligations.
 *
 * Login rehydrates persisted obligations through the core runtime. Logout fires before
 * vanilla saves/removes the ServerPlayer, so a successful recovery is captured by the
 * normal player save. Respawn fires after the replacement ServerPlayer is registered.
 */
public final class MinecraftInnerDominionLifecycleRuntime {
    private MinecraftInnerDominionLifecycleRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftInnerDominionLifecycleRuntime::onPlayerLoggedIn);
        gameBus.addListener(MinecraftInnerDominionLifecycleRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftInnerDominionLifecycleRuntime::onPlayerRespawn);
    }

    private static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        recover(event.getEntity());
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        recover(event.getEntity());
    }

    private static void onPlayerRespawn(PlayerEvent.PlayerRespawnEvent event) {
        recover(event.getEntity());
    }

    private static void recover(net.minecraft.world.entity.player.Player player) {
        if (!(player instanceof ServerPlayer serverPlayer)) return;
        MinecraftServer server = serverPlayer.serverLevel().getServer();
        MinecraftInnerDominionRuntime.recoverParticipant(server, serverPlayer.getUUID());
    }
}
