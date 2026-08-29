package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

@FunctionalInterface
public interface RitualComponentProvider {
    ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick);

    default RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
        ArcanaDecision decision = check(definition, context, nowTick);
        return decision.allowed()
                ? RitualComponentReservation.reserved(() -> { }, () -> { })
                : RitualComponentReservation.denied(decision.code(), decision.detail());
    }
}
