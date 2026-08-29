package dev.gustavopere.blackarcana.content.space;

import java.util.Objects;
import java.util.UUID;

/**
 * Produces an atomic swap plan only when both server snapshots are still mutually valid.
 * Minecraft adapters must compare endpoint versions again immediately before applying movement.
 */
public final class ReciprocalTranspositionPlanner {
    private final SafeDestinationPolicy destinationPolicy;

    public ReciprocalTranspositionPlanner(SafeDestinationPolicy destinationPolicy) {
        this.destinationPolicy = Objects.requireNonNull(destinationPolicy, "destinationPolicy");
    }

    public Plan plan(Endpoint first, Endpoint second) {
        Objects.requireNonNull(first, "first");
        Objects.requireNonNull(second, "second");
        if (first.entityId().equals(second.entityId())) return Plan.denied("same_entity");
        if (!first.consentAllowed() || !second.consentAllowed()) return Plan.denied("consent_denied");
        SafeDestinationPolicy.Decision firstDestination = destinationPolicy.validate(second.destinationFor(first));
        if (!firstDestination.allowed()) return Plan.denied("first_" + firstDestination.code());
        SafeDestinationPolicy.Decision secondDestination = destinationPolicy.validate(first.destinationFor(second));
        if (!secondDestination.allowed()) return Plan.denied("second_" + secondDestination.code());
        return Plan.allowed(first.entityId(), second.entityId(), first.version(), second.version());
    }

    public record Endpoint(UUID entityId, long version, boolean consentAllowed, SafeDestinationPolicy.Facts ownLocationFacts) {
        public Endpoint {
            Objects.requireNonNull(entityId, "entityId");
            Objects.requireNonNull(ownLocationFacts, "ownLocationFacts");
            if (version < 0L) throw new IllegalArgumentException("version cannot be negative");
        }
        private SafeDestinationPolicy.Facts destinationFor(Endpoint mover) { return ownLocationFacts; }
    }

    public record Plan(boolean allowed, String code, UUID firstEntity, UUID secondEntity, long firstVersion, long secondVersion) {
        public Plan { Objects.requireNonNull(code, "code"); }
        static Plan allowed(UUID first, UUID second, long firstVersion, long secondVersion) {
            return new Plan(true, "", first, second, firstVersion, secondVersion);
        }
        static Plan denied(String code) { return new Plan(false, code, null, null, -1L, -1L); }
    }
}
