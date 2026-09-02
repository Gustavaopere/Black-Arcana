package dev.gustavopere.blackarcana.content.blood;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

/** Pure bounded planner; the Minecraft adapter revalidates and applies each drain server-side. */
public final class SanguineHarvestPlanner {
    private SanguineHarvestPlanner() { }

    public static HarvestPlan plan(List<Candidate> candidates, int maxTargets, double maxTotalYield) {
        Objects.requireNonNull(candidates, "candidates");
        if (maxTargets <= 0 || maxTargets > BloodSafetyCeilings.MAX_HARVEST_TARGETS) {
            throw new IllegalArgumentException("maxTargets outside hard bounds");
        }
        if (!Double.isFinite(maxTotalYield) || maxTotalYield <= 0.0D) {
            throw new IllegalArgumentException("maxTotalYield must be finite and positive");
        }

        List<Drain> drains = new ArrayList<>();
        double remaining = maxTotalYield;
        for (Candidate candidate : candidates) {
            Objects.requireNonNull(candidate, "candidate");
            if (drains.size() >= maxTargets || remaining <= 0.0D) break;
            if (!candidate.eligible() || candidate.antiFarmWeight() <= 0.0D || candidate.maxDrain() <= 0.0D) continue;
            double drain = Math.min(remaining, candidate.maxDrain() * candidate.antiFarmWeight());
            if (drain <= 0.0D) continue;
            drains.add(new Drain(candidate.entityId(), drain));
            remaining -= drain;
        }
        return new HarvestPlan(List.copyOf(drains), maxTotalYield - remaining);
    }

    public record Candidate(UUID entityId, double maxDrain, double antiFarmWeight, boolean eligible) {
        public Candidate {
            Objects.requireNonNull(entityId, "entityId");
            if (!Double.isFinite(maxDrain) || maxDrain < 0.0D) throw new IllegalArgumentException("maxDrain invalid");
            if (!Double.isFinite(antiFarmWeight) || antiFarmWeight < 0.0D || antiFarmWeight > 1.0D) {
                throw new IllegalArgumentException("antiFarmWeight must be in [0,1]");
            }
        }
    }

    public record Drain(UUID entityId, double amount) {
        public Drain {
            Objects.requireNonNull(entityId, "entityId");
            if (!Double.isFinite(amount) || amount <= 0.0D) throw new IllegalArgumentException("amount invalid");
        }
    }

    public record HarvestPlan(List<Drain> drains, double totalYield) {
        public HarvestPlan {
            drains = List.copyOf(Objects.requireNonNull(drains, "drains"));
            if (drains.size() > BloodSafetyCeilings.MAX_HARVEST_TARGETS) {
                throw new IllegalArgumentException("harvest plan exceeds hard target ceiling");
            }
            if (!Double.isFinite(totalYield) || totalYield < 0.0D) throw new IllegalArgumentException("totalYield invalid");
        }
    }
}
