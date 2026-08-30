package dev.gustavopere.blackarcana.content.souls;

import java.util.Objects;
import java.util.Set;

/** Explicit whitelist for occult perception; it never turns into a generic hidden-entity reveal. */
public final class SpiritSightPolicy {
    public static final double ABSOLUTE_MAX_RADIUS = 128.0D;
    public static final long ABSOLUTE_MAX_DURATION_TICKS = 12_000L;

    public boolean visible(Trace trace) {
        Objects.requireNonNull(trace, "trace");
        if (!trace.providerAvailable()) return false;
        return switch (trace.kind()) {
            case MALUM_SPIRIT, EIDOLON_OCCULT, BLACK_ARCANA_WARD, BLACK_ARCANA_DOMAIN -> true;
            case HIDDEN_PLAYER, PRIVATE_CONTAINER, OTHER -> false;
        };
    }

    public boolean visible(Policy policy, TraceView trace) {
        Objects.requireNonNull(policy, "policy");
        Objects.requireNonNull(trace, "trace");
        if (!visible(new Trace(trace.kind(), trace.providerAvailable()))) return false;
        if (!policy.allowedKinds().contains(trace.kind())) return false;
        if (trace.privateData() && !policy.revealPrivateData()) return false;
        double radiusSquared = policy.radius() * policy.radius();
        return trace.distanceSquared() <= radiusSquared;
    }

    public record Policy(
        double radius,
        long durationTicks,
        Set<TraceKind> allowedKinds,
        boolean revealPrivateData
    ) {
        public Policy {
            if (!Double.isFinite(radius) || radius < 1.0D || radius > ABSOLUTE_MAX_RADIUS) {
                throw new IllegalArgumentException("radius must be finite and within the absolute Spirit Sight bound");
            }
            if (durationTicks < 1L || durationTicks > ABSOLUTE_MAX_DURATION_TICKS) {
                throw new IllegalArgumentException("durationTicks must be within the absolute Spirit Sight bound");
            }
            Objects.requireNonNull(allowedKinds, "allowedKinds");
            if (allowedKinds.isEmpty()) throw new IllegalArgumentException("allowedKinds cannot be empty");
            allowedKinds = Set.copyOf(allowedKinds);
        }
    }

    public record Trace(TraceKind kind, boolean providerAvailable) {
        public Trace { Objects.requireNonNull(kind, "kind"); }
    }

    public record TraceView(
        double distanceSquared,
        TraceKind kind,
        boolean providerAvailable,
        boolean privateData
    ) {
        public TraceView {
            if (!Double.isFinite(distanceSquared) || distanceSquared < 0.0D) {
                throw new IllegalArgumentException("distanceSquared must be finite and non-negative");
            }
            Objects.requireNonNull(kind, "kind");
        }
    }

    public enum TraceKind {
        MALUM_SPIRIT,
        EIDOLON_OCCULT,
        BLACK_ARCANA_WARD,
        BLACK_ARCANA_DOMAIN,
        HIDDEN_PLAYER,
        PRIVATE_CONTAINER,
        OTHER
    }
}
