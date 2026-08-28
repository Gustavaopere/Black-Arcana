package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** Transactional Black Arcana cost provider backed by Iron's player mana. */
public final class IronsManaCostProvider implements CostProvider {
    public static final String RESOURCE_ID = "irons_spellbooks:mana";
    private static final float EPSILON = 0.0001F;

    private final IronsManaAccess access;

    public IronsManaCostProvider(IronsManaAccess access) {
        this.access = Objects.requireNonNull(access, "access");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaCost cost = request.spell().cost();
        if (!RESOURCE_ID.equals(cost.resourceId())) {
            return ArcanaDecision.deny(
                "irons_mana_resource_mismatch",
                "Iron's mana provider cannot pay resource " + cost.resourceId());
        }

        IronsManaSnapshot snapshot;
        try {
            snapshot = Objects.requireNonNull(access.snapshot(request.context().casterId()), "mana snapshot");
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny(
                "irons_mana_query_failed",
                "Iron's mana state could not be queried: " + failure.getClass().getSimpleName());
        }

        float required;
        try {
            required = requiredMana(cost, snapshot.maximum());
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("irons_mana_cost_invalid", failure.getMessage());
        }

        if (snapshot.current() + EPSILON < required) {
            return ArcanaDecision.deny(
                "insufficient_irons_mana",
                "Requires " + required + " Iron's mana but only " + snapshot.current() + " is available");
        }
        return ArcanaDecision.allow();
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaDecision preflight = check(request);
        if (!preflight.allowed()) return new DeniedReservation(preflight);

        IronsManaSnapshot snapshot;
        try {
            snapshot = Objects.requireNonNull(access.snapshot(request.context().casterId()), "mana snapshot");
        } catch (RuntimeException failure) {
            return new DeniedReservation(ArcanaDecision.deny(
                "irons_mana_query_failed",
                "Iron's mana state could not be queried during reservation: " + failure.getClass().getSimpleName()));
        }

        float required;
        try {
            required = requiredMana(request.spell().cost(), snapshot.maximum());
        } catch (RuntimeException failure) {
            return new DeniedReservation(ArcanaDecision.deny("irons_mana_cost_invalid", failure.getMessage()));
        }
        if (snapshot.current() + EPSILON < required) {
            return new DeniedReservation(ArcanaDecision.deny(
                "insufficient_irons_mana",
                "Iron's mana changed before reservation could commit"));
        }
        if (required <= EPSILON) return NoOpReservation.INSTANCE;

        UUID casterId = request.context().casterId();
        ArcanaDecision deducted;
        try {
            deducted = Objects.requireNonNull(access.adjust(casterId, -required), "mana adjustment decision");
        } catch (RuntimeException failure) {
            deducted = ArcanaDecision.deny(
                "irons_mana_reservation_failed",
                "Iron's mana reservation failed: " + failure.getClass().getSimpleName());
        }
        if (!deducted.allowed()) return new DeniedReservation(deducted);
        return new ManaReservation(access, casterId, required);
    }

    static float requiredMana(ArcanaCost cost, float maximum) {
        Objects.requireNonNull(cost, "cost");
        double required = switch (cost.unit()) {
            case FLAT -> cost.amount();
            case PERCENT_OF_MAX -> cost.amount() * maximum;
        };
        if (!Double.isFinite(required) || required < 0.0D || required > Float.MAX_VALUE) {
            throw new IllegalArgumentException("resolved Iron's mana cost is outside supported bounds");
        }
        return (float) required;
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
        private final IronsManaAccess access;
        private final UUID casterId;
        private final float amount;
        private final AtomicBoolean terminal = new AtomicBoolean();
        private volatile boolean committed;

        private ManaReservation(IronsManaAccess access, UUID casterId, float amount) {
            this.access = access;
            this.casterId = casterId;
            this.amount = amount;
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public void commit() {
            if (terminal.compareAndSet(false, true)) committed = true;
        }

        @Override
        public void refund() {
            if (!terminal.compareAndSet(false, true)) return;
            ArcanaDecision refund = access.adjust(casterId, amount);
            if (!refund.allowed()) {
                throw new IllegalStateException("Iron's mana refund failed: " + refund.code());
            }
        }

        boolean committed() {
            return committed;
        }
    }
}
