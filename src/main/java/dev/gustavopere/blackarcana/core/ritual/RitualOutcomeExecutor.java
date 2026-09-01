package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

@FunctionalInterface
public interface RitualOutcomeExecutor {
    ArcanaDecision execute(RitualDefinition definition, RitualContext context, long nowTick);
}
