package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Transactional composition for rituals that consume resources from multiple providers. */
public final class CompositeRitualComponentProvider implements RitualComponentProvider {
    public static final int MAX_PROVIDERS = 16;

    private final List<RitualComponentProvider> providers;

    public CompositeRitualComponentProvider(List<? extends RitualComponentProvider> providers) {
        Objects.requireNonNull(providers, "providers");
        if (providers.isEmpty() || providers.size() > MAX_PROVIDERS) {
            throw new IllegalArgumentException("ritual component provider count outside bounds");
        }
        this.providers = List.copyOf(providers);
        if (this.providers.stream().anyMatch(Objects::isNull)) {
            throw new IllegalArgumentException("ritual component providers cannot contain null");
        }
    }

    @Override
    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
        for (RitualComponentProvider provider : providers) {
            final ArcanaDecision decision;
            try {
                decision = Objects.requireNonNull(provider.check(definition, context, nowTick), "component decision");
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny(
                        "ritual_component_check_failed",
                        "composite ritual component check failed closed");
            }
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }

    @Override
    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
        ArcanaDecision preflight = check(definition, context, nowTick);
        if (!preflight.allowed()) {
            return RitualComponentReservation.denied(preflight.code(), preflight.detail());
        }

        List<RitualComponentReservation> reservations = new ArrayList<>(providers.size());
        try {
            for (RitualComponentProvider provider : providers) {
                RitualComponentReservation reservation = Objects.requireNonNull(
                        provider.reserve(definition, context, nowTick),
                        "component reservation");
                if (!reservation.decision().allowed()) {
                    refundReverse(reservations);
                    return RitualComponentReservation.denied(
                            reservation.decision().code(), reservation.decision().detail());
                }
                reservations.add(reservation);
            }
        } catch (RuntimeException | LinkageError failure) {
            try {
                refundReverse(reservations);
            } catch (RuntimeException rollbackFailure) {
                failure.addSuppressed(rollbackFailure);
            }
            return RitualComponentReservation.denied(
                    "ritual_component_reserve_failed",
                    "composite ritual component reservation failed closed");
        }

        return RitualComponentReservation.reserved(
                () -> reservations.forEach(RitualComponentReservation::commit),
                () -> refundReverse(reservations));
    }

    private static void refundReverse(List<RitualComponentReservation> reservations) {
        RuntimeException first = null;
        for (int index = reservations.size() - 1; index >= 0; index--) {
            try {
                reservations.get(index).refund();
            } catch (RuntimeException failure) {
                if (first == null) first = failure;
                else first.addSuppressed(failure);
            }
        }
        if (first != null) throw first;
    }
}
