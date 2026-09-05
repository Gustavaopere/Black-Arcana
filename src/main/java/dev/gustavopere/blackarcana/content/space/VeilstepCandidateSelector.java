package dev.gustavopere.blackarcana.content.space;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Selects the first valid server-generated nearby destination from a bounded candidate set. */
public final class VeilstepCandidateSelector {
    private final SafeDestinationPolicy policy;

    public VeilstepCandidateSelector(SafeDestinationPolicy policy) {
        this.policy = Objects.requireNonNull(policy, "policy");
    }

    public Optional<Candidate> select(List<Candidate> candidates) {
        Objects.requireNonNull(candidates, "candidates");
        if (candidates.size() > LiminalSafetyCeilings.MAX_SAFE_SEARCH_CANDIDATES) {
            throw new IllegalArgumentException("safe-position search exceeds hard candidate ceiling");
        }
        for (Candidate candidate : candidates) {
            Objects.requireNonNull(candidate, "candidate");
            if (policy.validate(candidate.facts()).allowed()) return Optional.of(candidate);
        }
        return Optional.empty();
    }

    public record Candidate(String destinationId, SafeDestinationPolicy.Facts facts) {
        public Candidate {
            Objects.requireNonNull(destinationId, "destinationId");
            Objects.requireNonNull(facts, "facts");
            if (destinationId.isBlank() || destinationId.length() > 160) {
                throw new IllegalArgumentException("destinationId must be bounded");
            }
        }
    }
}
