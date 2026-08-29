package dev.gustavopere.blackarcana.content.noetic;

import java.util.LinkedHashSet;
import java.util.Objects;
import java.util.Set;

/** Server-owned privacy and loading policy for remote perception. */
public final class DivinationVisibilityPolicy {
    private static final Set<String> APPROVED_METADATA = Set.of("health", "status_effects", "held_item", "armor_summary", "occult_trace");

    public record Facts(boolean loaded, boolean sameDimension, boolean playerTarget, boolean consentOrCovenant, boolean ownedFamiliar, double distance) {
        public Facts {
            if (!Double.isFinite(distance) || distance < 0D) throw new IllegalArgumentException("distance must be finite and non-negative");
        }
    }

    private final double maxRange;
    public DivinationVisibilityPolicy(double maxRange) {
        if (!Double.isFinite(maxRange) || maxRange <= 0D || maxRange > FamiliarSafetyCeilings.MAX_SCRY_RANGE) throw new IllegalArgumentException("maxRange outside safety ceiling");
        this.maxRange = maxRange;
    }

    public boolean canNamescry(Facts facts) {
        Objects.requireNonNull(facts, "facts");
        return facts.loaded() && facts.sameDimension() && facts.distance() <= maxRange && (!facts.playerTarget() || facts.consentOrCovenant());
    }

    public boolean canBorrowSight(Facts facts) {
        Objects.requireNonNull(facts, "facts");
        return facts.loaded() && facts.sameDimension() && facts.distance() <= maxRange && facts.ownedFamiliar();
    }

    public Set<String> filterMetadata(Set<String> requested) {
        Objects.requireNonNull(requested, "requested");
        LinkedHashSet<String> allowed = new LinkedHashSet<>();
        for (String field : requested) if (APPROVED_METADATA.contains(field)) allowed.add(field);
        return Set.copyOf(allowed);
    }
}
