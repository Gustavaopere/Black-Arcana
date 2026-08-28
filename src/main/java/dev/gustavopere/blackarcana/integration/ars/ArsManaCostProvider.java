package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** Transactional Black Arcana cost provider backed by Ars Nouveau player mana. */
public final class ArsManaCostProvider implements CostProvider {
    public static final String RESOURCE_ID = "ars_nouveau:mana";
    private static final double EPSILON = 0.000001D;

    private final ArsManaAccess access;

    public ArsManaCostProvider(ArsManaAccess access) {
        this.access = Objects.requireNonNull(access, "access");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaCost cost = request.spell().cost();
        if (!RESOURCE_ID.equals(cost.resourceId())) {
            return ArcanaDecision.deny(
                "ars_mana_resource_mismatch",
                "Ars mana provider cannot pay resource " + cost.resourceId());
        }

        ArsManaSnapshot snapshot;
        try {
            snapshot = Objects.requireNonNull(access.snapshot(request.context().casterId()), "mana snapshot");
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny(
                "ars_mana_query_failed",
                "Ars mana state could not be queried: " + failure.getClass().getSimpleName());
        }

        double required;
        try {
            required = requiredMana(cost, snapshot.maximum());
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("ars_mana_cost_invalid", failure.getMessage());
        }
        if (snapshot.current() + EPSILON < required) {
            return ArcanaDecision.deny(
                "insufficient_ars_mana",
                "Requires " + required + " Ars mana but only " + snapshot.current() + " is available");
        }
        return ArcanaDecision.allow();
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaDecision preflight = check(request);
        if (!preflight.allowed()) return new DeniedReservation(preflight);

        ArsManaSnapshot snapshot;
        try {
            snapshot = Objects.requireNonNull(access.snapshot(request.context().casterId()), "mana snapshot");
        } catch (RuntimeException failure) {
            return new DeniedReservation(ArcanaDecision.deny(
                "ars_mana_query_failed",
                "Ars mana state could not be queried during reservation: " + failure.getClass().getSimpleName()));
        }

        double required;
        try {
            required = requiredMana(request.spell().cost(), snapshot.maximum());
        } catch (RuntimeException failure) {
            return new DeniedReservation(ArcanaDecision.deny("ars_mana_cost_invalid", failure.getMessage()));
        }
        if (snapshot.current() + EPSILON < required) {
            return new DeniedReservation(ArcanaDecision.deny(
                "insufficient_ars_mana",
                "Ars mana changed before reservation could commit"));
        }
        if (required <= EPSILON) return NoOpReservation.INSTANCE;

        UUID casterId = request.context().casterId();
        ArcanaDecision deducted;
        try {
            deducted = Objects.requireNonNull(access.adjust(casterId, -required), "mana adjustment decision");
        } catch (RuntimeException failure) {
            deducted = ArcanaDecision.deny(
                "ars_mana_reservation_failed",
                "Ars mana reservation failed: " + failure.getClass().getSimpleName());
        }
        if (!deducted.allowed()) return new DeniedReservation(deducted);
        return new ManaReservation(access, casterId, required);
    }

    static double requiredMana(ArcanaCost cost, double maximum) {
        Objects.requireNonNull(cost, "cost");
        double required = switch (cost.unit()) {
            case FLAT -> cost.amount();
            case PERCENT_OF_MAX -> cost.amount() * maximum;
        };
        if (!Double.isFinite(required) || required < 0.0D) {
            throw new IllegalArgumentException("resolved Ars mana cost is outside supported bounds");
        }
        return required;
    }

    private record DeniedReservation(ArcanaDecision decision) implements CostReservation {
        private DeniedReservation {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed()) throw new IllegalArgumentException("denied reservation requires denial decision");
        }
        @Override public void commit() { throw new IllegalStateException("cannot commit denied mana reservation"); }
        @Override public void refund() { }
    }

    private enum NoOpReservation implements CostReservation {
        INSTANCE;
        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { }
        @Override public void refund() { }
    }

    private static final class ManaReservation implements CostReservation {
        private final ArsManaAccess access;
        private final UUID casterId;
        private final double amount;
        private final AtomicBoolean terminal = new AtomicBoolean();

        private ManaReservation(ArsManaAccess access, UUID casterId, double amount) {
            this.access = access;
            this.casterId = casterId;
            this.amount = amount;
        }

        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { terminal.compareAndSet(false, true); }

        @Override
        public void refund() {
            if (!terminal.compareAndSet(false, true)) return;
            ArcanaDecision refund = access.adjust(casterId, amount);
            if (!refund.allowed()) {
                throw new IllegalStateException("Ars mana refund failed: " + refund.code());
            }
        }
    }
}
