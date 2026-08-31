package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaCastResult.Status;
import dev.gustavopere.blackarcana.api.ArcanaServices.ArcanaEffect;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastHazardGate;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastRequestValidator;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastSuccessObserver;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.HazardPreparation;
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
    private final CastHazardGate hazardGate;

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
        this(
            identity,
            replayGuard,
            progression,
            cooldowns,
            targets,
            costs,
            worldPolicy,
            effect,
            CastSuccessObserver.noop(),
            CastHazardGate.noop());
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
        this(
            identity,
            replayGuard,
            progression,
            cooldowns,
            targets,
            costs,
            worldPolicy,
            effect,
            successObserver,
            CastHazardGate.noop());
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
            CastSuccessObserver successObserver,
            CastHazardGate hazardGate
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
        this.hazardGate = Objects.requireNonNull(hazardGate);
    }

    /**
     * Rebinds only the Stage 05A hazard gate while preserving every established
     * Stage 02 collaborator and observer. The original engine remains immutable.
     */
    public ArcanaCastEngine withHazardGate(CastHazardGate replacement) {
        return new ArcanaCastEngine(
            identity,
            replayGuard,
            progression,
            cooldowns,
            targets,
            costs,
            worldPolicy,
            effect,
            successObserver,
            Objects.requireNonNull(replacement, "replacement"));
    }

    /**
     * Evaluates only established query-only gates for selected-spell presentation.
     *
     * <p>This method deliberately skips replay admission, target resolution, world
     * authorization and hazard preparation. It never reserves resources, starts a
     * cooldown or executes the spell. A CLEAR result is therefore informational,
     * not a guarantee that a later cast will succeed.</p>
     */
    public ArcanaGatePreflight previewReadOnlyGates(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");

        ArcanaDecision decision = Objects.requireNonNull(identity.check(request), "identity decision");
        if (!decision.allowed()) {
            return ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.IDENTITY, decision);
        }

        decision = Objects.requireNonNull(progression.check(request), "progression decision");
        if (!decision.allowed()) {
            return ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.PROGRESSION, decision);
        }

        decision = Objects.requireNonNull(cooldowns.check(request), "cooldown decision");
        if (!decision.allowed()) {
            return ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.COOLDOWN, decision);
        }

        decision = Objects.requireNonNull(costs.check(request), "cost decision");
        if (!decision.allowed()) {
            return ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.COST, decision);
        }

        return ArcanaGatePreflight.clear();
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

        HazardPreparation hazard = Objects.requireNonNull(
            hazardGate.preflight(request, target),
            "hazard preparation");
        ArcanaDecision hazardDecision = Objects.requireNonNull(hazard.decision(), "hazard preflight decision");
        if (!hazardDecision.allowed()) {
            hazard.cancel();
            return ArcanaCastResult.denied(Status.DENIED_HAZARD, hazardDecision);
        }

        final CostReservation reservation;
        try {
            reservation = Objects.requireNonNull(costs.reserve(request), "cost reservation");
        } catch (RuntimeException | Error failure) {
            hazard.cancel();
            throw failure;
        }
        if (!reservation.reserved()) {
            hazard.cancel();
            return ArcanaCastResult.denied(Status.DENIED_COST, reservation.decision());
        }

        boolean committed = false;
        boolean hazardCommitted = false;
        try {
            hazardDecision = Objects.requireNonNull(hazard.activate(), "hazard activation decision");
            if (!hazardDecision.allowed()) {
                return ArcanaCastResult.denied(Status.DENIED_HAZARD, hazardDecision);
            }

            EffectResult effectResult = effect.apply(request, target);
            if (!effectResult.success()) {
                return new ArcanaCastResult(Status.EFFECT_FAILED, "effect_failed", effectResult.detail());
            }

            reservation.commit();
            committed = true;
            cooldowns.start(request);
            hazard.commit();
            hazardCommitted = true;
            notifySuccess(request, target, effectResult);
            return ArcanaCastResult.success(effectResult.detail());
        } finally {
            if (!hazardCommitted) hazard.cancel();
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
