package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.Objects;
import java.util.Optional;

/**
 * Immutable delayed-backlash unit.
 *
 * Legacy debt deliberately has no damage identity and therefore can never
 * acquire emergency-protection context after the fact. Contextual debt keeps
 * the damage identity and the frozen cast-time protection snapshot intact
 * across logout/restart boundaries.
 */
public record PendingBacklashDebt(
    double amount,
    Optional<ArcanaDamageInstanceId> damageInstanceId,
    boolean protectionAllowed,
    ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
) {
    public PendingBacklashDebt {
        if (!Double.isFinite(amount) || amount <= 0.0D
            || amount > PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER) {
            throw new IllegalArgumentException("amount outside absolute bounds");
        }
        damageInstanceId = Objects.requireNonNull(damageInstanceId, "damageInstanceId");
        emergencyProtectionSnapshot = Objects.requireNonNull(
            emergencyProtectionSnapshot, "emergencyProtectionSnapshot");
        if (damageInstanceId.isEmpty()) {
            if (protectionAllowed || !emergencyProtectionSnapshot.candidates().isEmpty()) {
                throw new IllegalArgumentException("legacy debt cannot carry emergency protection context");
            }
        }
    }

    public static PendingBacklashDebt legacy(double amount) {
        return new PendingBacklashDebt(
            amount,
            Optional.empty(),
            false,
            ArcaneEmergencyProtectionSnapshot.empty());
    }

    public static PendingBacklashDebt contextual(
        double amount,
        ArcanaDamageInstanceId damageInstanceId,
        boolean protectionAllowed,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        return new PendingBacklashDebt(
            amount,
            Optional.of(Objects.requireNonNull(damageInstanceId, "damageInstanceId")),
            protectionAllowed,
            Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot"));
    }

    public boolean hasCausalContext() {
        return damageInstanceId.isPresent();
    }

    /** Returns the same frozen causal context with a safely clamped amount. */
    public PendingBacklashDebt withAmount(double boundedAmount) {
        return new PendingBacklashDebt(
            boundedAmount,
            damageInstanceId,
            protectionAllowed,
            emergencyProtectionSnapshot);
    }
}
