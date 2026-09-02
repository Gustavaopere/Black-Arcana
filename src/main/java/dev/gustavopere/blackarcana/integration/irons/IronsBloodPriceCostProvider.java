package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.content.blood.BloodPriceCostProvider;
import dev.gustavopere.blackarcana.content.blood.BloodPriceHealthAccess;

import java.util.Objects;
import java.util.function.Predicate;

/**
 * Iron's-specific Blood Price composition.
 *
 * Iron's remains authoritative for mana state and percent-of-maximum resolution. Blood Price
 * receives that resolved mana amount, substitutes only the configured fraction with real health,
 * then sends the reduced flat mana cost back through {@link IronsManaCostProvider}. Eligibility is
 * injected by the caller so this class does not invent RPG/perk ownership.
 */
public final class IronsBloodPriceCostProvider implements CostProvider {
    private final BloodPriceCostProvider delegate;

    public IronsBloodPriceCostProvider(
        IronsManaAccess manaAccess,
        BloodPriceHealthAccess healthAccess,
        Predicate<ArcanaCastRequest> enabled,
        double healthFraction,
        double healthPerMana,
        double minimumRemainingHealth
    ) {
        Objects.requireNonNull(manaAccess, "manaAccess");
        this.delegate = new BloodPriceCostProvider(
            new IronsManaCostProvider(manaAccess),
            Objects.requireNonNull(healthAccess, "healthAccess"),
            Objects.requireNonNull(enabled, "enabled"),
            request -> resolvedManaCost(manaAccess, request),
            healthFraction,
            healthPerMana,
            minimumRemainingHealth);
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        return delegate.check(Objects.requireNonNull(request, "request"));
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        return delegate.reserve(Objects.requireNonNull(request, "request"));
    }

    private static double resolvedManaCost(IronsManaAccess manaAccess, ArcanaCastRequest request) {
        ArcanaCost cost = request.spell().cost();
        if (!IronsManaCostProvider.RESOURCE_ID.equals(cost.resourceId())) {
            throw new IllegalArgumentException("Blood Price cannot rewrite non-Iron's mana resource " + cost.resourceId());
        }
        IronsManaSnapshot snapshot = Objects.requireNonNull(
            manaAccess.snapshot(request.context().casterId()),
            "Iron's mana snapshot");
        return IronsManaCostProvider.requiredMana(cost, snapshot.maximum());
    }
}
