package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaCastResult.Status;
import dev.gustavopere.blackarcana.api.ArcanaServices.ArcanaEffect;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetSelector;
import dev.gustavopere.blackarcana.api.ArcanaServices.WorldEffectPolicy;

import java.util.Objects;

public final class ArcanaCastEngine {
    private final ProgressionGate progression;
    private final CooldownService cooldowns;
    private final TargetSelector targets;
    private final CostProvider costs;
    private final WorldEffectPolicy worldPolicy;
    private final ArcanaEffect effect;

    public ArcanaCastEngine(
            ProgressionGate progression,
            CooldownService cooldowns,
            TargetSelector targets,
            CostProvider costs,
            WorldEffectPolicy worldPolicy,
            ArcanaEffect effect
    ) {
        this.progression = Objects.requireNonNull(progression);
        this.cooldowns = Objects.requireNonNull(cooldowns);
        this.targets = Objects.requireNonNull(targets);
        this.costs = Objects.requireNonNull(costs);
        this.worldPolicy = Objects.requireNonNull(worldPolicy);
        this.effect = Objects.requireNonNull(effect);
    }

    public ArcanaCastResult execute(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");

        ArcanaDecision decision = progression.check(request);
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

        if (!costs.consume(request)) {
            return ArcanaCastResult.denied(Status.DENIED_COST, ArcanaDecision.deny("cost_race", "resource changed before execution"));
        }

        EffectResult effectResult = effect.apply(request, target);
        if (!effectResult.success()) {
            return new ArcanaCastResult(Status.EFFECT_FAILED, "effect_failed", effectResult.detail());
        }

        cooldowns.start(request);
        return ArcanaCastResult.success(effectResult.detail());
    }
}
