package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaPaymentPolicy;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.Objects;

public final class PolicyAwareCostProvider implements CostProvider {
    private final ArcanaPaymentPolicy policy;
    private final CostProvider delegate;

    public PolicyAwareCostProvider(ArcanaPaymentPolicy policy, CostProvider delegate) {
        this.policy = Objects.requireNonNull(policy, "policy");
        this.delegate = Objects.requireNonNull(delegate, "delegate");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        if (policy.bypasses(request.context().casterMode())) return ArcanaDecision.allow();
        return Objects.requireNonNull(delegate.check(request), "cost decision");
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        if (policy.bypasses(request.context().casterMode())) return NoOpReservation.INSTANCE;
        return Objects.requireNonNull(delegate.reserve(request), "cost reservation");
    }

    private enum NoOpReservation implements CostReservation {
        INSTANCE;

        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { }
        @Override public void refund() { }
    }
}
