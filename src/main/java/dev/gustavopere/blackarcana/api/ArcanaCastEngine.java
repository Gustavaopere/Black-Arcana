package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaCastResult.Status;
import dev.gustavopere.blackarcana.api.ArcanaServices.ArcanaEffect;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastRequestValidator;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastSuccessObserver;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;
import dev.gustavopere.blackarcana.api.ArcanaServices.ReplayGuard;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetSelector;
import dev.gustavopere.blackarcana.api.ArcanaServices.WorldEffectPolicy;

import java.util.Objects;

public final class ArcanaCastEngine {
    private final CastRequestValidator identity;
    private final ReplayGuard replayGuard;
    private final ProgressionGate progression;
    private final CooldownService cooldowns;
    private final TargetSelector targets;
    private final CostProvider costs;
    private final WorldEffectPolicy worldPolicy;
    private final ArcanaEffect effect;
    private final CastSuccessObserver successObserver;

    public ArcanaCastEngine(
            CastRequestValidator identity,
            ReplayGuard replayGuard,
            ProgressionGate progression,
            CooldownService cooldowns,
            TargetSelector targets,
            CostProvider costs,
            WorldEffectPolicy worldPolicy,
            ArcanaEffect effect
    ) {
        this(identity, replayGuard, progression, cooldowns, targets, costs, worldPolicy, effect, CastSuccessObserver.noop());
    }

    public ArcanaCastEngine(
            CastRequestValidator identity,
            ReplayGuard replayGuard,
            ProgressionGate progression,
            CooldownService cooldowns,
            TargetSelector targets,
            CostProvider costs,
            WorldEffectPolicy worldPolicy,
            ArcanaEffect effect,
            CastSuccessObserver successObserver
    ) {
        this.identity = Objects.requireNonNull(identity);
        this.replayGuard = Objects.requireNonNull(replayGuard);
        this.progression = Objects.requireNonNull(progression);
        this.cooldowns = Objects.requireNonNull(cooldowns);
        this.targets = Objects.requireNonNull(targets);
        this.costs = Objects.requireNonNull(costs);
        this.worldPolicy = Objects.requireNonNull(worldPolicy);
        this.effect = Objects.requireNonNull(effect);
        this.successObserver = Objects.requireNonNull(successObserver);
    }

    public ArcanaCastResult execute(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");

        ArcanaDecision decision = identity.check(request);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_IDENTITY, decision);

        decision = replayGuard.claim(request);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_REPLAY, decision);

        decision = progression.check(request);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_PROGRESSION, decision);

        decision = cooldowns.check(request);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_COOLDOWN, decision);

        TargetResolution target = targets.resolve(request);
        if (!target.resolved()) {
            return ArcanaCastResult.denied(Status.DENIED_TARGET, ArcanaDecision.deny("target", target.detail()));
        }

        decision = costs.check(request);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_COST, decision);

        decision = worldPolicy.authorize(request, target);
        if (!decision.allowed()) return ArcanaCastResult.denied(Status.DENIED_WORLD_POLICY, decision);

        CostReservation reservation = Objects.requireNonNull(costs.reserve(request), "cost reservation");
        if (!reservation.reserved()) {
            return ArcanaCastResult.denied(Status.DENIED_COST, reservation.decision());
        }

        boolean committed = false;
        try {
            EffectResult effectResult = effect.apply(request, target);
            if (!effectResult.success()) {
                return new ArcanaCastResult(Status.EFFECT_FAILED, "effect_failed", effectResult.detail());
            }

            reservation.commit();
            committed = true;
            cooldowns.start(request);
            notifySuccess(request, target, effectResult);
            return ArcanaCastResult.success(effectResult.detail());
        } finally {
            if (!committed) reservation.refund();
        }
    }

    private void notifySuccess(ArcanaCastRequest request, TargetResolution target, EffectResult effectResult) {
        try {
            successObserver.onSuccess(request, target, effectResult);
        } catch (RuntimeException ignored) {
            // The spell and resource transaction are already committed. Optional
            // observers must fail independently instead of duplicating/refunding casts.
        }
    }
}
