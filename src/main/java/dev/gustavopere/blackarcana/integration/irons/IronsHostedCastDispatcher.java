package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;

import java.util.Objects;

/** Routes an Iron-hosted cast through the same authoritative Black Arcana ingress. */
public final class IronsHostedCastDispatcher {
    private IronsHostedCastDispatcher() { }

    public static CastResultPayload cast(ServerPlayer player, ArcanaSpellId spellId) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(spellId, "spellId");
        CastIntentPayload intent = new CastIntentPayload(
            ArcanaProtocol.VERSION,
            ArcanaCastId.random().canonical(),
            spellId.canonical(),
            0,
            "");
        CastResultPayload result = ArcanaServerRuntimeManager.handleCastIntent(player, intent);
        if (!ArcanaCastResult.Status.SUCCESS.name().equals(result.status())) {
            String detail = result.detail().isBlank() ? result.code() : result.detail();
            player.displayClientMessage(Component.literal("Black Arcana: " + detail), true);
        }
        return result;
    }
}
