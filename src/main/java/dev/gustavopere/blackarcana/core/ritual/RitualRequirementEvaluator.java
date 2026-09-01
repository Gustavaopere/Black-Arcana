package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

@FunctionalInterface
public interface RitualRequirementEvaluator {
    ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick);
}
