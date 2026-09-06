package dev.gustavopere.blackarcana.content.noetic;

/** Immutable hard-bounded configuration for one familiar-centered Pact Sanctuary aura. */
public record PactSanctuarySpec(int radiusBlocks, int durationTicks, int memberBudget) {
    public PactSanctuarySpec {
        if (radiusBlocks <= 0 || radiusBlocks > NoeticSafetyCeilings.MAX_SANCTUARY_RADIUS) {
            throw new IllegalArgumentException(
                    "radiusBlocks must be within 1.." + NoeticSafetyCeilings.MAX_SANCTUARY_RADIUS);
        }
        if (durationTicks <= 0 || durationTicks > NoeticSafetyCeilings.MAX_SANCTUARY_DURATION_TICKS) {
            throw new IllegalArgumentException(
                    "durationTicks must be within 1.." + NoeticSafetyCeilings.MAX_SANCTUARY_DURATION_TICKS);
        }
        if (memberBudget <= 0 || memberBudget > NoeticSafetyCeilings.MAX_SANCTUARY_MEMBERS) {
            throw new IllegalArgumentException(
                    "memberBudget must be within 1.." + NoeticSafetyCeilings.MAX_SANCTUARY_MEMBERS);
        }
    }
}
