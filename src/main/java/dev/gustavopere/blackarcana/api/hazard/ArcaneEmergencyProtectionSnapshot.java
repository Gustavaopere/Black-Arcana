package dev.gustavopere.blackarcana.api.hazard;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;

/** Immutable emergency-protection facts frozen before one hazardous cast can produce effects. */
public record ArcaneEmergencyProtectionSnapshot(List<Candidate> candidates) {
    public static final int MAX_CANDIDATES = 32;
    public static final double ABSOLUTE_MAX_ABSORPTION = 1_000_000.0D;
    public static final long ABSOLUTE_MAX_COOLDOWN_TICKS = 20L * 60L * 60L * 24L * 30L;
    private static final Pattern ID = Pattern.compile("[a-z0-9_.:/-]{1,128}");

    public ArcaneEmergencyProtectionSnapshot {
        Objects.requireNonNull(candidates, "candidates");
        if (candidates.size() > MAX_CANDIDATES) {
            throw new IllegalArgumentException("too many emergency protection candidates");
        }
        candidates = List.copyOf(candidates);
        Set<String> resources = new HashSet<>();
        for (Candidate candidate : candidates) {
            Objects.requireNonNull(candidate, "candidate");
            if (!resources.add(candidate.resourceId())) {
                throw new IllegalArgumentException("duplicate emergency protection resource: " + candidate.resourceId());
            }
        }
    }

    public static ArcaneEmergencyProtectionSnapshot empty() {
        return new ArcaneEmergencyProtectionSnapshot(List.of());
    }

    public record Candidate(
        String sourceId,
        String resourceId,
        double absorption,
        long cooldownTicks
    ) {
        public Candidate {
            requireId(sourceId, "sourceId");
            requireId(resourceId, "resourceId");
            if (!Double.isFinite(absorption) || absorption <= 0.0D || absorption > ABSOLUTE_MAX_ABSORPTION) {
                throw new IllegalArgumentException("absorption outside absolute bounds");
            }
            if (cooldownTicks < 0L || cooldownTicks > ABSOLUTE_MAX_COOLDOWN_TICKS) {
                throw new IllegalArgumentException("cooldownTicks outside absolute bounds");
            }
        }
    }

    private static void requireId(String value, String name) {
        Objects.requireNonNull(value, name);
        if (!ID.matcher(value).matches()) throw new IllegalArgumentException("invalid " + name + ": " + value);
    }
}
