package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtection;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Adapts immutable cast-time emergency candidates into per-settlement transactional providers.
 * No live equipment lookup is performed here; every fact comes from the frozen hazard snapshot.
 */
public final class ArcaneFrozenEmergencyProtection {
    private ArcaneFrozenEmergencyProtection() { }

    public static List<ArcaneEmergencyProtection> providers(
        ArcaneEmergencyProtectionSnapshot snapshot,
        ArcaneEmergencyProtectionStateService state,
        long serverTick
    ) {
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(state, "state");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");

        List<ArcaneEmergencyProtection> providers = new ArrayList<>(snapshot.candidates().size());
        for (ArcaneEmergencyProtectionSnapshot.Candidate candidate : snapshot.candidates()) {
            providers.add(new CandidateProvider(candidate, state, serverTick));
        }
        return List.copyOf(providers);
    }

    private record CandidateProvider(
        ArcaneEmergencyProtectionSnapshot.Candidate candidate,
        ArcaneEmergencyProtectionStateService state,
        long serverTick
    ) implements ArcaneEmergencyProtection {
        private CandidateProvider {
            Objects.requireNonNull(candidate, "candidate");
            Objects.requireNonNull(state, "state");
            if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        }

        @Override
        public String providerId() {
            return candidate.sourceId();
        }

        @Override
        public Reservation reserve(Query query) {
            Objects.requireNonNull(query, "query");
            ArcaneEmergencyProtectionStateService.Reservation stateReservation = state.reserve(
                query.casterId(),
                candidate.resourceId(),
                serverTick,
                candidate.cooldownTicks());
            return new Reservation() {
                @Override
                public dev.gustavopere.blackarcana.api.ArcanaDecision decision() {
                    return stateReservation.decision();
                }

                @Override
                public double absorption() {
                    return stateReservation.decision().allowed() ? candidate.absorption() : 0.0D;
                }

                @Override
                public void commit() {
                    stateReservation.commit();
                }

                @Override
                public void refund() {
                    stateReservation.refund();
                }
            };
        }
    }
}
