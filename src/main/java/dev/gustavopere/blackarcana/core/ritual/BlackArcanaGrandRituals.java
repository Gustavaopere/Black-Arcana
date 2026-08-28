package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Objects;

/** Canonical Black Arcana-owned grand ritual definitions. */
public final class BlackArcanaGrandRituals {
    /**
     * A long-form consecration used as the representative Stage 06 grand ritual.
     * The outcome is deliberately supplied by the server binding so progression,
     * optional resources and world policy stay outside the core definition.
     */
    public static final ArcanaRitualId VEIL_ANCHOR_CONSECRATION_ID =
            ArcanaRitualId.parse("black_arcana:veil_anchor_consecration");
    public static final RitualDefinition VEIL_ANCHOR_CONSECRATION =
            new RitualDefinition(VEIL_ANCHOR_CONSECRATION_ID, 100L, 400L);

    private BlackArcanaGrandRituals() { }

    public static void install(
            ArcanaServerRuntime runtime,
            RitualRequirementEvaluator requirements,
            RitualComponentProvider components,
            RitualOutcomeExecutor outcomes
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(requirements, "requirements");
        Objects.requireNonNull(components, "components");
        Objects.requireNonNull(outcomes, "outcomes");
        runtime.ritualDefinitions().register(VEIL_ANCHOR_CONSECRATION);
        runtime.ritualBindings().register(
                VEIL_ANCHOR_CONSECRATION_ID,
                requirements,
                components,
                outcomes);
    }
}
