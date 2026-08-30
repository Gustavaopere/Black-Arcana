package dev.gustavopere.blackarcana.content.souls;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

/**
 * Host-facing contract for Spirit Sight. Providers expose only traces backed by real host state;
 * the runtime never synthesizes world entities or caches provider results as occult state.
 */
public interface SpiritTraceProvider {
    int ABSOLUTE_MAX_PROVIDER_ID_LENGTH = 96;

    String providerId();

    List<Trace> query(Query query);

    record Query(
        UUID viewerId,
        String dimensionId,
        double x,
        double y,
        double z,
        double radius
    ) {
        public Query {
            Objects.requireNonNull(viewerId, "viewerId");
            Objects.requireNonNull(dimensionId, "dimensionId");
            if (dimensionId.isBlank() || dimensionId.length() > 128) {
                throw new IllegalArgumentException("dimensionId must be a bounded stable identifier");
            }
            if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) {
                throw new IllegalArgumentException("query coordinates must be finite");
            }
            if (!Double.isFinite(radius) || radius < 1.0D || radius > SpiritSightPolicy.ABSOLUTE_MAX_RADIUS) {
                throw new IllegalArgumentException("query radius must remain within Spirit Sight bounds");
            }
        }
    }

    record Trace(
        UUID traceId,
        double x,
        double y,
        double z,
        SpiritSightPolicy.TraceKind kind,
        boolean privateData
    ) {
        public Trace {
            Objects.requireNonNull(traceId, "traceId");
            Objects.requireNonNull(kind, "kind");
            if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) {
                throw new IllegalArgumentException("trace coordinates must be finite");
            }
        }
    }

    static boolean validProviderId(String providerId) {
        if (providerId == null || providerId.isBlank() || providerId.length() > ABSOLUTE_MAX_PROVIDER_ID_LENGTH) {
            return false;
        }
        return providerId.matches("[a-z0-9_.-]+:[a-z0-9_./-]+");
    }
}
