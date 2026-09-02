package dev.gustavopere.blackarcana.content.blood;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;

import java.util.Objects;
import java.util.function.Predicate;
import java.util.function.ToDoubleFunction;

/**
 * Transactional cost decorator for Blood Price.
 *
 * The delegate remains the authoritative resource provider. Blood Price only rewrites the
 * resource amount presented to that provider and reserves the substituted portion as real
 * health through {@link BloodPriceHealthAccess}. Both reservations are committed/refunded as
 * one canonical cast transaction.
 */
public final class BloodPriceCostProvider implements CostProvider {
    private final CostProvider delegate;
    private final BloodPriceHealthAccess healthAccess;
    private final Predicate<ArcanaCastRequest> enabled;
    private final ToDoubleFunction<ArcanaCastRequest> resolvedOriginalCost;
    private final double healthFraction;
    private final double healthPerResourceUnit;
    private final double minimumRemainingHealth;

    public BloodPriceCostProvider(
        CostProvider delegate,
        BloodPriceHealthAccess healthAccess,
        Predicate<ArcanaCastRequest> enabled,
        ToDoubleFunction<ArcanaCastRequest> resolvedOriginalCost,
        double healthFraction,
        double healthPerResourceUnit,
        double minimumRemainingHealth
    ) {
        this.delegate = Objects.requireNonNull(delegate, "delegate");
        this.healthAccess = Objects.requireNonNull(healthAccess, "healthAccess");
        this.enabled = Objects.requireNonNull(enabled, "enabled");
        this.resolvedOriginalCost = Objects.requireNonNull(resolvedOriginalCost, "resolvedOriginalCost");
        validateConfig(healthFraction, healthPerResourceUnit, minimumRemainingHealth);
        this.healthFraction = healthFraction;
        this.healthPerResourceUnit = healthPerResourceUnit;
        this.minimumRemainingHealth = minimumRemainingHealth;
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        if (!enabled.test(request)) return Objects.requireNonNull(delegate.check(request), "cost decision");

        Prepared prepared;
        try {
            prepared = prepare(request);
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny(
                "blood_price_quote_failed",
                "Blood Price could not resolve the cast cost: " + failure.getClass().getSimpleName());
        }
        if (!prepared.quote().affordable()) {
            return ArcanaDecision.deny(
                "insufficient_blood_price_health",
                "Blood Price would cross the configured minimum remaining health");
        }
        return Objects.requireNonNull(delegate.check(prepared.resourceRequest()), "cost decision");
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        if (!enabled.test(request)) return Objects.requireNonNull(delegate.reserve(request), "cost reservation");

        final Prepared prepared;
        try {
            prepared = prepare(request);
        } catch (RuntimeException failure) {
            return denied("blood_price_quote_failed", "Blood Price could not resolve the cast cost");
        }
        if (!prepared.quote().affordable()) {
            return denied(
                "insufficient_blood_price_health",
                "Blood Price would cross the configured minimum remaining health");
        }

        CostReservation resourceReservation = Objects.requireNonNull(
            delegate.reserve(prepared.resourceRequest()),
            "resource reservation");
        if (!resourceReservation.reserved()) return resourceReservation;

        final CostReservation healthReservation;
        try {
            healthReservation = Objects.requireNonNull(
                healthAccess.reserve(
                    request.context().casterId(),
                    prepared.quote().healthCost(),
                    minimumRemainingHealth),
                "health reservation");
        } catch (RuntimeException failure) {
            refundQuietly(resourceReservation, failure);
            throw failure;
        }

        if (!healthReservation.reserved()) {
            try {
                resourceReservation.refund();
            } catch (RuntimeException rollbackFailure) {
                throw new IllegalStateException("Blood Price resource rollback failed", rollbackFailure);
            }
            return healthReservation;
        }
        return new CombinedReservation(resourceReservation, healthReservation);
    }

    private Prepared prepare(ArcanaCastRequest request) {
        double resolvedCost = resolvedOriginalCost.applyAsDouble(request);
        double currentHealth = healthAccess.currentHealth(request.context().casterId());
        BloodPriceCalculator.Quote quote = BloodPriceCalculator.quote(
            resolvedCost,
            healthFraction,
            healthPerResourceUnit,
            currentHealth,
            minimumRemainingHealth);
        return new Prepared(withFlatResourceCost(request, quote.resourceCost()), quote);
    }

    private static ArcanaCastRequest withFlatResourceCost(ArcanaCastRequest request, double resourceCost) {
        ArcanaSpellDefinition spell = request.spell();
        ArcanaSpellDefinition adjusted = new ArcanaSpellDefinition(
            spell.id(),
            spell.translationKey(),
            spell.iconId(),
            new ArcanaCost(spell.cost().resourceId(), resourceCost),
            spell.requestsWorldMutation());
        return new ArcanaCastRequest(
            request.castId(),
            adjusted,
            request.context(),
            request.loadoutSlot(),
            request.targetHint(),
            request.channelTicks());
    }

    private static void validateConfig(
        double healthFraction,
        double healthPerResourceUnit,
        double minimumRemainingHealth
    ) {
        if (!Double.isFinite(healthFraction)
            || healthFraction < 0.0D
            || healthFraction > BloodSafetyCeilings.MAX_BLOOD_PRICE_FRACTION) {
            throw new IllegalArgumentException("healthFraction outside Blood Price ceiling");
        }
        if (!Double.isFinite(healthPerResourceUnit) || healthPerResourceUnit < 0.0D) {
            throw new IllegalArgumentException("healthPerResourceUnit must be finite and non-negative");
        }
        if (!Double.isFinite(minimumRemainingHealth)
            || minimumRemainingHealth < BloodSafetyCeilings.MIN_BLOOD_PRICE_REMAINING_HEALTH) {
            throw new IllegalArgumentException("minimumRemainingHealth below hard safety floor");
        }
    }

    private static CostReservation denied(String code, String detail) {
        return new DeniedReservation(ArcanaDecision.deny(code, detail));
    }

    private static void refundQuietly(CostReservation reservation, RuntimeException original) {
        try {
            reservation.refund();
        } catch (RuntimeException rollbackFailure) {
            original.addSuppressed(rollbackFailure);
        }
    }

    private record Prepared(ArcanaCastRequest resourceRequest, BloodPriceCalculator.Quote quote) {
        private Prepared {
            Objects.requireNonNull(resourceRequest, "resourceRequest");
            Objects.requireNonNull(quote, "quote");
        }
    }

    private record DeniedReservation(ArcanaDecision decision) implements CostReservation {
        private DeniedReservation {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed()) throw new IllegalArgumentException("denied reservation requires denial decision");
        }

        @Override public void commit() { throw new IllegalStateException("cannot commit denied Blood Price reservation"); }
        @Override public void refund() { }
    }

    private static final class CombinedReservation implements CostReservation {
        private enum State { RESERVED, COMMITTED, REFUNDED }

        private final CostReservation resource;
        private final CostReservation health;
        private State state = State.RESERVED;

        private CombinedReservation(CostReservation resource, CostReservation health) {
            this.resource = Objects.requireNonNull(resource, "resource");
            this.health = Objects.requireNonNull(health, "health");
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public synchronized void commit() {
            requireReserved();
            resource.commit();
            health.commit();
            state = State.COMMITTED;
        }

        @Override
        public synchronized void refund() {
            requireReserved();
            RuntimeException first = null;
            try {
                health.refund();
            } catch (RuntimeException failure) {
                first = failure;
            }
            try {
                resource.refund();
            } catch (RuntimeException failure) {
                if (first == null) first = failure;
                else first.addSuppressed(failure);
            }
            state = State.REFUNDED;
            if (first != null) throw first;
        }

        private void requireReserved() {
            if (state != State.RESERVED) {
                throw new IllegalStateException("Blood Price reservation already terminated: " + state);
            }
        }
    }
}
