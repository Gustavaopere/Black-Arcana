package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSettlement;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;

import java.util.Objects;

/**
 * Server-neutral Stage 05A runtime. It owns causal root sessions and backlash ledgers,
 * but does not know about Minecraft events or damage sources.
 */
public final class ArcaneHazardRuntime {
    public record ActivationResult(boolean activated, boolean backlashActive, String code) {
        public ActivationResult {
            Objects.requireNonNull(code, "code");
            if (activated && !code.isEmpty()) {
                throw new IllegalArgumentException("activated result cannot carry a denial code");
            }
            if (!activated && code.isBlank()) {
                throw new IllegalArgumentException("denied activation requires a code");
            }
            if (!activated && backlashActive) {
                throw new IllegalArgumentException("backlash cannot be active when activation failed");
            }
        }

        public static ActivationResult success(boolean backlashActive) {
            return new ActivationResult(true, backlashActive, "");
        }

        public static ActivationResult denied(String code) {
            return new ActivationResult(false, false, code);
        }
    }

    public record TickResult(int sessionsPruned, int ledgersPruned) {
        public TickResult {
            if (sessionsPruned < 0 || ledgersPruned < 0) {
                throw new IllegalArgumentException("prune counts cannot be negative");
            }
        }
    }

    private final ArcaneHazardSessionRegistry sessions;
    private final ArcaneBacklashLedgerRegistry backlashLedgers;

    public ArcaneHazardRuntime(int maxSessions) {
        this.sessions = new ArcaneHazardSessionRegistry(maxSessions);
        this.backlashLedgers = new ArcaneBacklashLedgerRegistry(maxSessions);
    }

    public ActivationResult activate(
        ArcaneHazardSnapshot snapshot,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy backlashPolicy
    ) {
        return activate(snapshot, resistance, backlashPolicy, ArcaneEmergencyProtectionSnapshot.empty());
    }

    public ActivationResult activate(
        ArcaneHazardSnapshot snapshot,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy backlashPolicy,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(resistance, "resistance");
        Objects.requireNonNull(backlashPolicy, "backlashPolicy");
        Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot");

        ArcaneHazardSessionRegistry.OpenResult opened = sessions.open(snapshot, emergencyProtectionSnapshot);
        if (!opened.opened()) return ActivationResult.denied(opened.code());

        ArcaneHazardSession session = opened.session().orElseThrow();
        if (!snapshot.profile().tier().requiresBacklashRisk()) {
            return ActivationResult.success(false);
        }

        if (backlashLedgers.open(session, resistance, backlashPolicy).isEmpty()) {
            sessions.close(snapshot.rootCastId());
            return ActivationResult.denied("backlash_ledger_capacity");
        }
        return ActivationResult.success(true);
    }

    public ArcaneBacklashSettlement settle(ArcaneConfirmedDamage damage) {
        return backlashLedgers.settle(Objects.requireNonNull(damage, "damage"));
    }

    public boolean close(ArcanaCastId castId) {
        Objects.requireNonNull(castId, "castId");
        boolean ledgerClosed = backlashLedgers.close(castId);
        boolean sessionClosed = sessions.close(castId);
        return ledgerClosed || sessionClosed;
    }

    public TickResult tick(long currentTick) {
        int ledgersPruned = backlashLedgers.pruneExpired(currentTick);
        int sessionsPruned = sessions.pruneExpired(currentTick);
        return new TickResult(sessionsPruned, ledgersPruned);
    }

    public ArcaneHazardSessionRegistry sessions() {
        return sessions;
    }

    public ArcaneBacklashLedgerRegistry backlashLedgers() {
        return backlashLedgers;
    }
}
