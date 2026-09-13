package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.integration.neoforge.MinecraftNoeticRuntime;
import dev.gustavopere.blackarcana.network.AstralReturnIntentPayload;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;

import java.util.Objects;

/** Server-side adapter for Astral control messages whose gameplay policy is already fully specified. */
public final class AstralSeveranceNetworkService {
    private AstralSeveranceNetworkService() { }

    /**
     * Closes only the authenticated caster's exact active projection and only with a sequence newer than the
     * most recent accepted/refused MOVE intent. Payload handlers run on the NeoForge main thread by default,
     * so the snapshot validation and close occur in server event order.
     */
    public static boolean handleReturn(ServerPlayer player, AstralReturnIntentPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");

        MinecraftServer server = player.serverLevel().getServer();
        var active = MinecraftNoeticRuntime.astralProjection(server, player.getUUID()).orElse(null);
        if (active == null) return false;
        if (!active.projectionId().equals(payload.projectionId())) return false;
        if (payload.sequence() <= active.lastProcessedControlSequence()) return false;

        return MinecraftNoeticRuntime.requestAstralReturn(
                server,
                player.getUUID(),
                payload.projectionId());
    }
}
