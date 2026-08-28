package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class CompositeCostProvider implements CostProvider {
    private final List<CostProvider> providers;

    public CompositeCostProvider(List<? extends CostProvider> providers) {
        Objects.requireNonNull(providers, "providers");
        this.providers = List.copyOf(providers);
        for (CostProvider provider : this.providers) Objects.requireNonNull(provider, "provider");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        for (CostProvider provider : providers) {
            ArcanaDecision decision = Objects.requireNonNull(provider.check(request), "cost decision");
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        List<CostReservation> reservations = new ArrayList<>(providers.size());
        try {
            for (CostProvider provider : providers) {
                CostReservation reservation = Objects.requireNonNull(provider.reserve(request), "cost reservation");
                if (!reservation.reserved()) {
                    refundReverse(reservations);
                    return new DeniedReservation(reservation.decision());
                }
                reservations.add(reservation);
            }
            return new CompositeReservation(reservations);
        } catch (RuntimeException ex) {
            try {
                refundReverse(reservations);
            } catch (RuntimeException rollback) {
                ex.addSuppressed(rollback);
            }
            throw ex;
        }
    }

    private static void refundReverse(List<CostReservation> reservations) {
        RuntimeException first = null;
        for (int index = reservations.size() - 1; index >= 0; index--) {
            try {
                reservations.get(index).refund();
            } catch (RuntimeException ex) {
                if (first == null) first = ex;
                else first.addSuppressed(ex);
            }
        }
        if (first != null) throw first;
    }

    private record DeniedReservation(ArcanaDecision decision) implements CostReservation {
        private DeniedReservation {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed()) throw new IllegalArgumentException("denied reservation requires a denial decision");
        }
        @Override public void commit() { throw new IllegalStateException("denied reservation cannot commit"); }
        @Override public void refund() { }
    }

    private static final class CompositeReservation implements CostReservation {
        private enum State { RESERVED, COMMITTED, REFUNDED }

        private final List<CostReservation> reservations;
        private State state = State.RESERVED;

        private CompositeReservation(List<CostReservation> reservations) {
            this.reservations = List.copyOf(reservations);
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public synchronized void commit() {
            requireReserved();
            for (CostReservation reservation : reservations) reservation.commit();
            state = State.COMMITTED;
        }

        @Override
        public synchronized void refund() {
            requireReserved();
            refundReverse(reservations);
            state = State.REFUNDED;
        }

        private void requireReserved() {
            if (state != State.RESERVED) {
                throw new IllegalStateException("reservation already terminated: " + state);
            }
        }
    }
}
