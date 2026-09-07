package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

/** Pure fail-closed admission and diminishing-return policy for Noetic gaze actions. */
public final class NoeticGazePolicy {
    private NoeticGazePolicy() { }

    public static ArcanaDecision authorizeStillness(Facts facts) {
        Objects.requireNonNull(facts, "facts");
        if (!facts.targetLoaded()) return deny("gaze_target_unloaded", "Gaze target must already be loaded");
        if (!facts.sameDimension()) return deny("gaze_dimension", "Gaze target must remain in the caster dimension");
        if (!facts.withinRange()) return deny("gaze_range", "Gaze target exceeds the hard range ceiling");
        if (!facts.casterLineOfSight()) return deny("gaze_caster_los", "Caster must maintain line of sight to the target");
        if (!facts.targetLineOfSight()) return deny("gaze_target_los", "Target must maintain reciprocal line of sight");
        if (!facts.casterFacingTarget()) return deny("gaze_caster_facing", "Caster must face the target");
        if (!facts.targetFacingCaster()) return deny("gaze_target_facing", "Target must face the caster");
        if (!facts.targetAlive()) return deny("gaze_target_dead", "Gaze target must remain alive");
        if (!facts.controlAuthorized()) return deny("gaze_control_denied", "Canonical CONTROL admission denied the gaze");
        return ArcanaDecision.allow();
    }

    public static ArcanaDecision authorizeNullification(boolean bossTarget, boolean controlAuthorized) {
        if (!controlAuthorized) {
            return deny("nullifying_gaze_control_denied", "Canonical CONTROL admission denied nullification");
        }
        if (bossTarget) {
            return deny(
                    "nullifying_gaze_boss_resistant",
                    "Boss targets require an explicit provider-specific nullification contract");
        }
        return ArcanaDecision.allow();
    }

    /**
     * Applies the canonical control cap first, then halves duration for each recent successful application.
     * Reaching the hard DR stack ceiling grants temporary reapplication immunity.
     */
    public static int effectiveControlTicks(int requestedTicks, int policyCapTicks, int priorApplications) {
        if (requestedTicks <= 0 || policyCapTicks <= 0) return 0;
        if (priorApplications < 0) throw new IllegalArgumentException("priorApplications cannot be negative");
        if (priorApplications >= NoeticSafetyCeilings.MAX_GAZE_DR_STACKS) return 0;

        int bounded = Math.min(
                NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS,
                Math.min(requestedTicks, policyCapTicks));
        for (int i = 0; i < priorApplications && bounded > 1; i++) {
            bounded = Math.max(1, bounded / 2);
        }
        return bounded;
    }

    private static ArcanaDecision deny(String code, String detail) {
        return ArcanaDecision.deny(code, detail);
    }

    public record Facts(
            boolean targetLoaded,
            boolean sameDimension,
            boolean withinRange,
            boolean casterLineOfSight,
            boolean targetLineOfSight,
            boolean casterFacingTarget,
            boolean targetFacingCaster,
            boolean targetAlive,
            boolean controlAuthorized
    ) { }
}
