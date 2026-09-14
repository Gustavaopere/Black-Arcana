package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;

import java.util.Objects;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * Pure server-side ingress between a validated wire intent and a spell engine.
 * Client target hints remain advisory: they are copied into the request only so
 * a server-owned TargetSelector can re-resolve and validate them against live world state.
 */
public final class ArcanaCastIngressService {
    private final ArcanaSpellRegistry spellRegistry;
    private final IngressRateLimiter rateLimiter;
    private final Predicate<ArcanaSpellId> channelOnlyRoute;
    private final Function<ArcanaSpellId, ArcanaCastEngine> engineResolver;

    public ArcanaCastIngressService(
            ArcanaSpellRegistry spellRegistry,
            IngressRateLimiter rateLimiter,
            Function<ArcanaSpellId, ArcanaCastEngine> engineResolver
    ) {
        this(spellRegistry, rateLimiter, spellId -> false, engineResolver);
    }

    public ArcanaCastIngressService(
            ArcanaSpellRegistry spellRegistry,
            IngressRateLimiter rateLimiter,
            Predicate<ArcanaSpellId> channelOnlyRoute,
            Function<ArcanaSpellId, ArcanaCastEngine> engineResolver
    ) {
        this.spellRegistry = Objects.requireNonNull(spellRegistry, "spellRegistry");
        this.rateLimiter = Objects.requireNonNull(rateLimiter, "rateLimiter");
        this.channelOnlyRoute = Objects.requireNonNull(channelOnlyRoute, "channelOnlyRoute");
        this.engineResolver = Objects.requireNonNull(engineResolver, "engineResolver");
    }

    public CastResultPayload handle(ArcanaCastContext context, CastIntentPayload intent) {
        Objects.requireNonNull(context, "context");
        Objects.requireNonNull(intent, "intent");

        ArcanaDecision ingress = rateLimiter.claim(context.casterId(), context.serverTick());
        if (!ingress.allowed()) {
            return result(intent, ArcanaCastResult.denied(ArcanaCastResult.Status.DENIED_INGRESS, ingress));
        }

        ArcanaSpellId spellId = intent.parsedSpellId();
        ArcanaSpellDefinition definition = spellRegistry.resolve(spellId).orElse(null);
        if (definition == null) {
            return result(intent, ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_IDENTITY,
                    ArcanaDecision.deny("unknown_spell", "spell is not registered on the server")));
        }

        if (channelOnlyRoute.test(spellId)) {
            return result(intent, ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_CHANNEL,
                    ArcanaDecision.deny(
                            "channel_requires_begin",
                            "spell requires the server-authoritative channel invocation route")));
        }

        ArcanaCastEngine engine = engineResolver.apply(spellId);
        if (engine == null) {
            return result(intent, ArcanaCastResult.denied(
                    ArcanaCastResult.Status.DENIED_IDENTITY,
                    ArcanaDecision.deny("spell_runtime_unavailable", "spell has no installed server execution runtime")));
        }

        ArcanaCastRequest request = new ArcanaCastRequest(
                intent.parsedCastId(), definition, context, intent.loadoutSlot(), intent.targetHint());
        return result(intent, engine.execute(request));
    }

    private static CastResultPayload result(CastIntentPayload intent, ArcanaCastResult result) {
        return CastResultPayload.from(intent.parsedCastId(), result);
    }
}
