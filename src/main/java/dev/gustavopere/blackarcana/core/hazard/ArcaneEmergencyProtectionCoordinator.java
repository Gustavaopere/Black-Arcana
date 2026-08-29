package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtection;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * Applies at most one successful emergency reservation to a damage instance.
 * Provider failures fail closed; already-committed identities are idempotent no-ops.
 */
public final class ArcaneEmergencyProtectionCoordinator {
    public static final int MAX_PROVIDERS = 16;
    public static final int MAX_SETTLEMENT_PROVIDERS = ArcaneEmergencyProtectionSnapshot.MAX_CANDIDATES;
    public static final int MAX_REMEMBERED_DAMAGE_INSTANCES = 8_192;

    private final List<ArcaneEmergencyProtection> providers;
    private final Set<ArcanaDamageInstanceId> committed = new HashSet<>();
    private final ArrayDeque<ArcanaDamageInstanceId> order = new ArrayDeque<>();

    public ArcaneEmergencyProtectionCoordinator(List<ArcaneEmergencyProtection> providers) {
        Objects.requireNonNull(providers, "providers");
        if (providers.size() > MAX_PROVIDERS) throw new IllegalArgumentException("too many emergency protection providers");
        this.providers = List.copyOf(providers);
    }

    public synchronized Result protect(ArcaneEmergencyProtection.Query query) {
        return protect(query, List.of());
    }

    /**
     * Applies the coordinator's long-lived providers plus providers bound to this settlement's
     * frozen hazard snapshot. The same committed damage-id memory is shared across both paths.
     */
    public synchronized Result protect(
        ArcaneEmergencyProtection.Query query,
        List<ArcaneEmergencyProtection> settlementProviders
    ) {
        Objects.requireNonNull(query, "query");
        Objects.requireNonNull(settlementProviders, "settlementProviders");
        if (settlementProviders.size() > MAX_SETTLEMENT_PROVIDERS) {
            throw new IllegalArgumentException("too many settlement emergency protection providers");
        }
        for (ArcaneEmergencyProtection provider : settlementProviders) {
            Objects.requireNonNull(provider, "settlement emergency provider");
        }
        if (!query.protectionAllowed() || query.predictedBacklash() <= query.unavoidableFloor()) {
            return new Result(query.predictedBacklash(), 0.0D, false, "protection_unavailable");
        }
        if (committed.contains(query.damageInstanceId())) {
            return new Result(query.predictedBacklash(), 0.0D, false, "already_processed");
        }

        Result staticResult = tryProviders(query, providers);
        if (staticResult != null) return staticResult;
        Result settlementResult = tryProviders(query, settlementProviders);
        if (settlementResult != null) return settlementResult;
        return new Result(query.predictedBacklash(), 0.0D, false, "no_reservation");
    }

    private Result tryProviders(
        ArcaneEmergencyProtection.Query query,
        List<ArcaneEmergencyProtection> candidates
    ) {
        for (ArcaneEmergencyProtection provider : candidates) {
            final ArcaneEmergencyProtection.Reservation reservation;
            try {
                reservation = Objects.requireNonNull(provider.reserve(query), "reservation");
            } catch (RuntimeException | LinkageError failure) {
                continue;
            }
            if (!reservation.decision().allowed()) continue;

            double maxAbsorbable = Math.max(0.0D, query.predictedBacklash() - query.unavoidableFloor());
            double requested = reservation.absorption();
            if (!Double.isFinite(requested) || requested <= 0.0D) {
                safeRefund(reservation);
                continue;
            }
            double absorbed = Math.min(maxAbsorbable, requested);
            if (absorbed <= 0.0D) {
                safeRefund(reservation);
                continue;
            }

            try {
                reservation.commit();
            } catch (RuntimeException | LinkageError failure) {
                safeRefund(reservation);
                continue;
            }
            remember(query.damageInstanceId());
            return new Result(query.predictedBacklash() - absorbed, absorbed, true, provider.providerId());
        }
        return null;
    }

    public synchronized boolean wasCommitted(ArcanaDamageInstanceId id) {
        return committed.contains(Objects.requireNonNull(id, "id"));
    }

    private void remember(ArcanaDamageInstanceId id) {
        if (committed.add(id)) order.addLast(id);
        while (order.size() > MAX_REMEMBERED_DAMAGE_INSTANCES) {
            committed.remove(order.removeFirst());
        }
    }

    private static void safeRefund(ArcaneEmergencyProtection.Reservation reservation) {
        try {
            reservation.refund();
        } catch (RuntimeException | LinkageError ignored) {
            // Reservation provider owns compensation diagnostics; coordinator remains fail-closed.
        }
    }

    public record Result(double remainingBacklash, double absorbed, boolean consumed, String sourceId) {
        public Result {
            Objects.requireNonNull(sourceId, "sourceId");
            if (!Double.isFinite(remainingBacklash) || remainingBacklash < 0.0D) throw new IllegalArgumentException("invalid remaining backlash");
            if (!Double.isFinite(absorbed) || absorbed < 0.0D) throw new IllegalArgumentException("invalid absorbed amount");
        }
    }
}
