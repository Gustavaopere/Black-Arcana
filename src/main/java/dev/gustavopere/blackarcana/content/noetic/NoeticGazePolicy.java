package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

/** Pure fail-closed admission policy for reciprocal Gaze of Stillness facts. */
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
