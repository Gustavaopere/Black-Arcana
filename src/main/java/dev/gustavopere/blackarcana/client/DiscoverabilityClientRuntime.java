package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import net.minecraft.world.entity.player.Player;

import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Physical-client session state for Stage 05.16.
 *
 * This runtime observes already-accepted presentation facts only. It never emits cast/loadout
 * traffic and never participates in gameplay admission, progression, cooldowns, hazards, or cost.
 */
final class DiscoverabilityClientRuntime {
    private static final int MAX_ACTIVE_HINTS = 1;
    private static final long HINT_LIFETIME_TICKS = 200L;
    private static final DiscoverabilityModel MODEL = new DiscoverabilityModel(
            MAX_ACTIVE_HINTS,
            HINT_LIFETIME_TICKS);

    private static UUID playerId;

    private DiscoverabilityClientRuntime() { }

    static synchronized void acceptLoadout(Player player, List<ArcanaSpellId> acceptedLoadout) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(acceptedLoadout, "acceptedLoadout");
        ensurePlayer(player);
        if (acceptedLoadout.isEmpty()) return;

        DiscoverabilityModel.BindingSnapshot bindings = DiscoverabilityBindings.snapshot();
        MODEL.offer(
                DiscoverabilityModel.Topic.CORE_CASTING,
                DiscoverabilityModel.Priority.OPTIONAL,
                player.tickCount,
                BlackArcanaClientConfig.DISCOVERABILITY_HINTS.get(),
                bindings);

        if (bindings.editLoadout().unbound()) {
            MODEL.offer(
                    DiscoverabilityModel.Topic.UNBOUND_EDITOR,
                    DiscoverabilityModel.Priority.REQUIRED,
                    player.tickCount,
                    BlackArcanaClientConfig.DISCOVERABILITY_HINTS.get(),
                    bindings);
        }
    }

    static synchronized Optional<DiscoverabilityModel.Hint> active(Player player) {
        Objects.requireNonNull(player, "player");
        ensurePlayer(player);
        return MODEL.active(player.tickCount).map(hint -> new DiscoverabilityModel.Hint(
                hint.topic(),
                hint.priority(),
                hint.startedTick(),
                hint.expiresAtTick(),
                DiscoverabilityBindings.snapshot()));
    }

    static synchronized void dismissCore() {
        MODEL.dismiss(DiscoverabilityModel.Topic.CORE_CASTING);
        MODEL.dismiss(DiscoverabilityModel.Topic.UNBOUND_EDITOR);
    }

    static DiscoverabilityModel.BindingSnapshot currentBindings() {
        return DiscoverabilityBindings.snapshot();
    }

    static synchronized void clearSession() {
        playerId = null;
        MODEL.resetSession();
    }

    private static void ensurePlayer(Player player) {
        UUID incoming = player.getUUID();
        if (playerId != null && !playerId.equals(incoming)) {
            MODEL.resetSession();
        }
        playerId = incoming;
    }
}
