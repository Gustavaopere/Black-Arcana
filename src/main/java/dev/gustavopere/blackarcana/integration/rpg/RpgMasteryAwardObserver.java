package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastSuccessObserver;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;

/**
 * Emits at most one bounded RPG mastery award for a committed, meaningful Black Arcana cast.
 * A reentrancy guard prevents progression events from feeding back into the same award path,
 * while the bounded throttle suppresses repetitive same-technique/same-target farming.
 */
public final class RpgMasteryAwardObserver implements CastSuccessObserver {
    private final RpgSkillTreeBridge bridge;
    private final Function<ArcanaCastRequest, Optional<RpgMasteryAwardSpec>> awardResolver;
    private final Consumer<ArcanaDecision> failureSink;
    private final MeaningfulMasteryAwardThrottle throttle;
    private final ThreadLocal<Boolean> awarding = ThreadLocal.withInitial(() -> false);

    public RpgMasteryAwardObserver(
        RpgSkillTreeBridge bridge,
        Function<ArcanaCastRequest, Optional<RpgMasteryAwardSpec>> awardResolver
    ) {
        this(bridge, awardResolver, ignored -> { }, new MeaningfulMasteryAwardThrottle());
    }

    public RpgMasteryAwardObserver(
        RpgSkillTreeBridge bridge,
        Function<ArcanaCastRequest, Optional<RpgMasteryAwardSpec>> awardResolver,
        Consumer<ArcanaDecision> failureSink
    ) {
        this(bridge, awardResolver, failureSink, new MeaningfulMasteryAwardThrottle());
    }

    RpgMasteryAwardObserver(
        RpgSkillTreeBridge bridge,
        Function<ArcanaCastRequest, Optional<RpgMasteryAwardSpec>> awardResolver,
        Consumer<ArcanaDecision> failureSink,
        MeaningfulMasteryAwardThrottle throttle
    ) {
        this.bridge = Objects.requireNonNull(bridge, "bridge");
        this.awardResolver = Objects.requireNonNull(awardResolver, "awardResolver");
        this.failureSink = Objects.requireNonNull(failureSink, "failureSink");
        this.throttle = Objects.requireNonNull(throttle, "throttle");
    }

    @Override
    public void onSuccess(ArcanaCastRequest request, TargetResolution target, EffectResult effectResult) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(effectResult, "effectResult");
        if (!effectResult.success() || !bridge.available() || awarding.get()) return;

        Optional<RpgMasteryAwardSpec> award = Objects.requireNonNull(
            awardResolver.apply(request), "awardResolver result");
        if (award.isEmpty() || !throttle.allow(request, target)) return;

        awarding.set(true);
        try {
            ArcanaDecision result = Objects.requireNonNull(
                bridge.awardMastery(request.context().casterId(), award.get()),
                "mastery award decision");
            if (!result.allowed()) failureSink.accept(result);
        } finally {
            awarding.set(false);
        }
    }
}
