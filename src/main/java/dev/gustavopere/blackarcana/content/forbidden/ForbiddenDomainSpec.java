package dev.gustavopere.blackarcana.content.forbidden;

import java.util.Objects;

/** Immutable bounded contract for one localized Forbidden Domain archetype. */
public record ForbiddenDomainSpec(
        String id,
        ForbiddenDomainMode mode,
        int radius,
        int durationTicks,
        int entityBudget,
        int restorationBudget
) {
    public ForbiddenDomainSpec {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(mode, "mode");
        if (id.isBlank()) throw new IllegalArgumentException("id must not be blank");
        if (mode != ForbiddenDomainMode.LOCALIZED_FIELD) {
            throw new IllegalArgumentException("D032 authorizes localized in-world fields only");
        }
        requireBounded("radius", radius, ForbiddenDomainSafetyCeilings.MAX_RADIUS);
        requireBounded("durationTicks", durationTicks, ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS);
        requireBounded("entityBudget", entityBudget, ForbiddenDomainSafetyCeilings.MAX_TRACKED_ENTITIES);
        requireBounded("restorationBudget", restorationBudget, ForbiddenDomainSafetyCeilings.MAX_RESTORATION_POSITIONS);
    }

    private static void requireBounded(String field, int value, int maximum) {
        if (value <= 0 || value > maximum) {
            throw new IllegalArgumentException(field + " must be within 1.." + maximum);
        }
    }
}
