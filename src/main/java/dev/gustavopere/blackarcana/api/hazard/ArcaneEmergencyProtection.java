package dev.gustavopere.blackarcana.api.hazard;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;
import java.util.UUID;

/** Transactional last-resort protection against already-settled backlash. */
public interface ArcaneEmergencyProtection {
    String providerId();
    Reservation reserve(Query query);

    record Query(
        UUID casterId,
        ArcanaDamageInstanceId damageInstanceId,
        double predictedBacklash,
        double unavoidableFloor,
        boolean protectionAllowed
    ) {
        public Query {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(damageInstanceId, "damageInstanceId");
            if (!Double.isFinite(predictedBacklash) || predictedBacklash < 0.0D || predictedBacklash > 1_000_000.0D) {
                throw new IllegalArgumentException("predictedBacklash outside absolute bounds");
            }
            if (!Double.isFinite(unavoidableFloor) || unavoidableFloor < 0.0D || unavoidableFloor > predictedBacklash) {
                throw new IllegalArgumentException("unavoidableFloor outside backlash bounds");
            }
        }
    }

    interface Reservation {
        ArcanaDecision decision();

        /** Requested absorption; the coordinator still clamps against the unavoidable floor. */
        double absorption();

        void commit();
        void refund();
    }
}
