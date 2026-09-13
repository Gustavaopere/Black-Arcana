package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import net.minecraft.world.entity.player.Player;

import java.util.Objects;
import java.util.UUID;
import java.util.function.Consumer;

/**
 * Physical-client adapter for the provider-free Stage 05.15 presentation controller.
 *
 * <p>The default sink is intentionally a no-op until Phase D supplies project-owned audiovisual
 * resources. Lifecycle/correlation is live now; no renderer or provider dependency is introduced.</p>
 */
public final class CastPresentationClientRuntime {
    static final int MAX_CORRELATED_CASTS = 64;
    static final long STALE_AGE_TICKS = 200L;

    private static volatile Consumer<CastAudiovisualOrchestration.Directive> sink = directive -> { };
    private static final CastPresentationController CONTROLLER = new CastPresentationController(
            MAX_CORRELATED_CASTS,
            STALE_AGE_TICKS,
            CastPresentationClientRuntime::currentPolicy,
            directive -> sink.accept(directive));
    private static UUID playerId;

    private CastPresentationClientRuntime() { }

    public static synchronized void installSink(Consumer<CastAudiovisualOrchestration.Directive> nextSink) {
        sink = Objects.requireNonNull(nextSink, "nextSink");
    }

    public static synchronized void recordLocalIntent(
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            long tick
    ) {
        CONTROLLER.recordLocalIntent(
                Objects.requireNonNull(castId, "castId"),
                Objects.requireNonNull(spellId, "spellId"),
                tick);
    }

    public static synchronized void acceptResult(Player player, CastResultPayload payload) {
        ensurePlayer(player);
        CONTROLLER.acceptAuthoritativeResult(
                Objects.requireNonNull(payload, "payload"),
                player.tickCount);
    }

    public static synchronized void tick(Player player) {
        ensurePlayer(player);
        CONTROLLER.evictStale(player.tickCount);
    }

    public static synchronized void clear() {
        playerId = null;
        CONTROLLER.clear();
    }

    private static CastPresentationLifecycle.SensoryPolicy currentPolicy() {
        return new CastPresentationLifecycle.SensoryPolicy(
                BlackArcanaClientConfig.PARTICLE_DENSITY.get(),
                BlackArcanaClientConfig.REDUCED_MOTION.get(),
                BlackArcanaClientConfig.REDUCED_FLASHES.get());
    }

    private static void ensurePlayer(Player player) {
        Objects.requireNonNull(player, "player");
        UUID incoming = player.getUUID();
        if (playerId != null && !playerId.equals(incoming)) {
            CONTROLLER.clear();
        }
        playerId = incoming;
    }
}
