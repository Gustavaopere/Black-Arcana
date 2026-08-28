package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCasterMode;
import net.minecraft.server.level.ServerPlayer;

import java.util.Objects;

public final class ServerPlayerArcanaContext {
    private ServerPlayerArcanaContext() { }

    public static ArcanaCastContext from(ServerPlayer player) {
        Objects.requireNonNull(player, "player");
        ArcanaCasterMode mode = player.isCreative() ? ArcanaCasterMode.CREATIVE : ArcanaCasterMode.SURVIVAL;
        return new ArcanaCastContext(
                player.getUUID(),
                player.level().getGameTime(),
                player.level().dimension().location().toString(),
                mode);
    }
}
