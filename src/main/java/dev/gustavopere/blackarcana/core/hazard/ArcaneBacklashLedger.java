package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSettlement;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;

import java.util.Objects;

/**
 * Bounded causal ledger for confirmed health damage belonging to one root cast.
 * Canonical aggregation is linear: F(D)=D. The ledger never applies Minecraft damage itself.
 */
public final class ArcaneBacklashLedger {
    private final ArcaneHazardSession session;
    private final ArcaneBacklashSnapshot snapshot;
    private double confirmedEligibleDamage;
    private double backlashSettled;

    public ArcaneBacklashLedger(ArcaneHazardSession session, ArcaneBacklashSnapshot snapshot) {
        this.session = Objects.requireNonNull(session, "session");
        this.snapshot = Objects.requireNonNull(snapshot, "snapshot");
        if (!session.snapshot().equals(snapshot.hazard())) {
            throw new IllegalArgumentException("backlash snapshot must match hazard session snapshot");
        }
    }

    public synchronized ArcaneBacklashSettlement settle(ArcaneConfirmedDamage damage) {
        Objects.requireNonNull(damage, "damage");
        var provenance = damage.provenance();

        if (provenance.family() == ArcaneDamageFamily.ARCANE_BACKLASH) {
            return ArcaneBacklashSettlement.ignored(damage.healthDamage(), "backlash_non_recursive");
        }
        if (!provenance.hazardEligible()) {
            return ArcaneBacklashSettlement.ignored(damage.healthDamage(), "hazard_ineligible");
        }
        if (provenance.family() == ArcaneDamageFamily.OWNED_SUMMON && !snapshot.policy().allowOwnedSummon()) {
            return ArcaneBacklashSettlement.ignored(damage.healthDamage(), "summon_not_opted_in");
        }

        ArcaneHazardSession.ClaimResult claim = session.claim(provenance, damage.serverTick());
        if (claim != ArcaneHazardSession.ClaimResult.ACCEPTED) {
            return ArcaneBacklashSettlement.denied(damage.healthDamage(), "hazard_claim_" + claim.name().toLowerCase());
        }
        if (damage.healthDamage() == 0.0D) {
            return ArcaneBacklashSettlement.settled(0.0D, 0.0D, 0.0D);
        }

        double previousAggregate = confirmedEligibleDamage;
        double newAggregate = saturatingAdd(
            previousAggregate,
            damage.healthDamage(),
            snapshot.policy().maximumTotalEligibleDamage());
        double deltaEligible = Math.max(0.0D, newAggregate - previousAggregate);
        confirmedEligibleDamage = newAggregate;

        double rawBacklash = multiplyFinite(
            deltaEligible,
            snapshot.hazard().profile().backlashMultiplier(),
            snapshot.arcaneResistance().residualBacklashMultiplier());
        double backlash = clampPositiveSettlement(rawBacklash);
        backlashSettled = saturatingAdd(
            backlashSettled,
            backlash,
            ArcaneBacklashPolicyCeilings.MAX_TOTAL_SETTLED_BACKLASH);

        return ArcaneBacklashSettlement.settled(damage.healthDamage(), deltaEligible, backlash);
    }

    public ArcaneBacklashSnapshot snapshot() {
        return snapshot;
    }

    public boolean isExpired(long currentTick) {
        return session.isExpired(currentTick) || session.closed();
    }

    public synchronized double confirmedEligibleDamage() {
        return confirmedEligibleDamage;
    }

    public synchronized double backlashSettled() {
        return backlashSettled;
    }

    private double clampPositiveSettlement(double raw) {
        if (raw <= 0.0D) return 0.0D;
        double bounded = Math.min(raw, snapshot.policy().maximumBacklashPerSettlement());
        return Math.max(bounded, snapshot.policy().minimumBacklashPerPositiveSettlement());
    }

    private static double multiplyFinite(double first, double second, double third) {
        double product = first * second;
        if (!Double.isFinite(product)) return Double.MAX_VALUE;
        product *= third;
        return Double.isFinite(product) ? Math.max(0.0D, product) : Double.MAX_VALUE;
    }

    private static double saturatingAdd(double current, double increment, double ceiling) {
        if (increment <= 0.0D || current >= ceiling) return Math.min(current, ceiling);
        double remaining = ceiling - current;
        return increment >= remaining ? ceiling : current + increment;
    }

    /** Separate technical ceiling so profile policy cannot accidentally make accumulated backlash unbounded. */
    private static final class ArcaneBacklashPolicyCeilings {
        private static final double MAX_TOTAL_SETTLED_BACKLASH = 100_000_000.0D;
    }
}
