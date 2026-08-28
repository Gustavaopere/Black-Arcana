package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.network.CastIntentPayload;

import java.util.Objects;
import java.util.function.Function;

/**
 * Coordinates charge/channel lifecycle without creating a second execution
 * pipeline. Begin performs cheap canonical identity/loadout checks; release
 * consumes the server-owned channel session and executes the same
 * {@link ArcanaCastEngine} used by immediate casts exactly once.
 */
public final class ArcanaChannelCastCoordinator {
    private final ArcanaSpellRegistry spells;
    private final LoadoutRegistry loadouts;
    private final ArcanaChannelManager channels;
    private final Function<ArcanaSpellId, ArcanaCastEngine> engineResolver;

    public ArcanaChannelCastCoordinator(
            ArcanaSpellRegistry spells,
            LoadoutRegistry loadouts,
            ArcanaChannelManager channels,
            Function<ArcanaSpellId, ArcanaCastEngine> engineResolver
    ) {
        this.spells = Objects.requireNonNull(spells, "spells");
        this.loadouts = Objects.requireNonNull(loadouts, "loadouts");
        this.channels = Objects.requireNonNull(channels, "channels");
        this.engineResolver = Objects.requireNonNull(engineResolver, "engineResolver");
    }

    public ArcanaDecision begin(ArcanaCastContext context, CastIntentPayload intent, ArcanaChannelSpec spec) {
        Objects.requireNonNull(context, "context");
        Objects.requireNonNull(intent, "intent");
        Objects.requireNonNull(spec, "spec");

        ArcanaSpellId spellId = intent.parsedSpellId();
        ArcanaSpellDefinition definition = spells.resolve(spellId).orElse(null);
        if (definition == null) {
            return ArcanaDecision.deny("unknown_spell", "spell is not registered on the server");
        }
        if (engineResolver.apply(spellId) == null) {
            return ArcanaDecision.deny("spell_runtime_unavailable", "spell has no installed server execution runtime");
        }

        ArcanaCastRequest provisional = new ArcanaCastRequest(
                intent.parsedCastId(), definition, context, intent.loadoutSlot(), intent.targetHint(), 0L);
        ArcanaDecision decision = spells.check(provisional);
        if (!decision.allowed()) return decision;
        decision = loadouts.check(provisional);
        if (!decision.allowed()) return decision;

        return channels.begin(
                context.casterId(),
                intent.parsedCastId(),
                spellId,
                intent.loadoutSlot(),
                context.serverTick(),
                spec);
    }

    public ArcanaCastResult release(
            ArcanaCastContext context,
            ArcanaCastId castId,
            String targetHint
    ) {
        Objects.requireNonNull(context, "context");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(targetHint, "targetHint");
        if (targetHint.length() > ArcanaCastRequest.MAX_TARGET_HINT_LENGTH) {
            return ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_CHANNEL,
                    ArcanaDecision.deny("target_hint_too_long", "release target hint exceeds request bound"));
        }

        ArcanaChannelManager.ReleaseResult release = channels.release(
                context.casterId(), castId, context.serverTick());
        if (!release.decision().allowed()) {
            return ArcanaCastResult.denied(ArcanaCastResult.Status.DENIED_CHANNEL, release.decision());
        }

        ArcanaChannelManager.ReleasedChannel channel = release.released().orElseThrow();
        ArcanaSpellDefinition definition = spells.resolve(channel.spellId()).orElse(null);
        if (definition == null) {
            return ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_IDENTITY,
                    ArcanaDecision.deny("unknown_spell", "channeled spell is no longer registered on the server"));
        }

        ArcanaCastEngine engine = engineResolver.apply(channel.spellId());
        if (engine == null) {
            return ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_IDENTITY,
                    ArcanaDecision.deny("spell_runtime_unavailable", "channeled spell runtime is no longer installed"));
        }

        ArcanaCastRequest request = new ArcanaCastRequest(
                channel.castId(),
                definition,
                context,
                channel.loadoutSlot(),
                targetHint,
                channel.channelTicks());
        return engine.execute(request);
    }

    public boolean cancel(ArcanaCastContext context, ArcanaCastId castId) {
        Objects.requireNonNull(context, "context");
        return channels.cancel(context.casterId(), Objects.requireNonNull(castId, "castId"));
    }
}
