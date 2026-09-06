package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

/** Pure fail-closed privacy/admission policy for Stage 07.07 observation mechanics. */
public final class NoeticObservationPolicy {
    private NoeticObservationPolicy() { }

    public static ArcanaDecision authorize(NoeticObservationKind kind, NoeticObservationFacts facts) {
        Objects.requireNonNull(kind, "kind");
        Objects.requireNonNull(facts, "facts");

        if (!facts.targetLoaded()) {
            return ArcanaDecision.deny("noetic_target_unloaded", "Noetic observation never force-loads an unavailable target");
        }
        if (!facts.sameDimension()) {
            return ArcanaDecision.deny("noetic_dimension_denied", "Noetic observation is restricted to the viewer's loaded dimension");
        }
        if (!facts.withinRange()) {
            return ArcanaDecision.deny("noetic_range_denied", "Noetic observation target is outside the hard range ceiling");
        }
        if (!facts.targetAlive()) {
            return ArcanaDecision.deny("noetic_target_dead", "Noetic observation requires a live eligible target");
        }
        if (facts.targetPlayer() && !facts.explicitConsent() && kind != NoeticObservationKind.NAMESCRY) {
            return ArcanaDecision.deny(
                    "noetic_player_privacy",
                    "Observation of another player requires explicit server-authorized consent");
        }

        return switch (kind) {
            case NAMESCRY -> facts.targetPlayer() && !facts.explicitConsent()
                    ? ArcanaDecision.deny("noetic_namescry_player_privacy", "Namescry of another player requires explicit server-authorized consent")
                    : ArcanaDecision.allow();
            case BORROWED_SIGHT -> facts.ownedFamiliar() || facts.explicitConsent()
                    ? ArcanaDecision.allow()
                    : ArcanaDecision.deny("noetic_borrowed_sight_authority", "Borrowed Sight requires an owned familiar or an explicitly consenting bonded target");
            case OCCULT_APPRAISAL -> facts.lineOfSight()
                    ? ArcanaDecision.allow()
                    : ArcanaDecision.deny("noetic_appraisal_los", "Occult Appraisal requires live line of sight");
            case ASTRAL_SEVERANCE -> ArcanaDecision.allow();
        };
    }
}
