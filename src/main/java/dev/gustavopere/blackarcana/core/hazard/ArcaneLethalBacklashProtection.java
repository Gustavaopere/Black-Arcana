package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtection;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.Objects;
import java.util.UUID;

/**
 * Server-neutral lethal-backlash resolver.
 *
 * <p>The caller supplies the already-reduced damage amount observed immediately before health
 * application plus current health and absorption. Equipment is never re-queried: settlement
 * providers are derived exclusively from the frozen root-cast snapshot.</p>
 */
public final class ArcaneLethalBacklashProtection {
    private static final double MAX_DAMAGE = 1_000_000.0D;

    private ArcaneLethalBacklashProtection() { }

    public static Result resolve(
        UUID casterId,
        ArcanaDamageInstanceId damageInstanceId,
        double finalDamage,
        double health,
        double absorption,
        boolean protectionAllowed,
        ArcaneEmergencyProtectionSnapshot frozenSnapshot,
        ArcaneEmergencyProtectionStateService state,
        long serverTick,
        ArcaneEmergencyProtectionCoordinator coordinator
    ) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(damageInstanceId, "damageInstanceId");
        Objects.requireNonNull(frozenSnapshot, "frozenSnapshot");
        Objects.requireNonNull(state, "state");
        Objects.requireNonNull(coordinator, "coordinator");
        requireFiniteNonNegative(finalDamage, MAX_DAMAGE, "finalDamage");
        requireFiniteNonNegative(health, Double.MAX_VALUE, "health");
        requireFiniteNonNegative(absorption, Double.MAX_VALUE, "absorption");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");

        double survivablePool = saturatingFiniteAdd(health, absorption);
        if (finalDamage < survivablePool) {
            return new Result(finalDamage, 0.0D, false, "not_lethal");
        }

        ArcaneEmergencyProtectionCoordinator.Result protectedResult = coordinator.protect(
            new ArcaneEmergencyProtection.Query(
                casterId,
                damageInstanceId,
                finalDamage,
                0.0D,
                protectionAllowed),
            ArcaneFrozenEmergencyProtection.providers(frozenSnapshot, state, serverTick));
        return new Result(
            protectedResult.remainingBacklash(),
            protectedResult.absorbed(),
            protectedResult.consumed(),
            protectedResult.sourceId());
    }

    public record Result(double remainingDamage, double absorbed, boolean consumed, String code) {
        public Result {
            Objects.requireNonNull(code, "code");
            requireFiniteNonNegative(remainingDamage, MAX_DAMAGE, "remainingDamage");
            requireFiniteNonNegative(absorbed, MAX_DAMAGE, "absorbed");
            if (absorbed > MAX_DAMAGE - remainingDamage) {
                throw new IllegalArgumentException("resolved damage exceeds absolute bounds");
            }
        }
    }

    private static void requireFiniteNonNegative(double value, double maximum, String name) {
        if (!Double.isFinite(value) || value < 0.0D || value > maximum) {
            throw new IllegalArgumentException(name + " outside absolute bounds");
        }
    }

    private static double saturatingFiniteAdd(double first, double second) {
        double sum = first + second;
        return Double.isFinite(sum) ? sum : Double.MAX_VALUE;
    }
}
