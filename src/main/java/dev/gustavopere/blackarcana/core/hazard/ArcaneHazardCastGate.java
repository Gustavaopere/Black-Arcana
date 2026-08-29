package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastHazardGate;
import dev.gustavopere.blackarcana.api.ArcanaServices.HazardPreparation;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionAcquisitionProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSnapshot;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-neutral Stage 05A gate that freezes danger and resistance/state snapshots during
 * preflight and activates the root hazard session only after normal resources are reserved.
 */
public final class ArcaneHazardCastGate implements CastHazardGate {
    public interface HazardSessionActivator {
        ArcaneHazardRuntime.ActivationResult activate(
            ArcaneHazardSnapshot snapshot,
            ArcaneResistanceSnapshot resistance,
            ArcaneBacklashPolicy policy
        );

        boolean close(ArcanaCastId castId);
    }

    private final ArcaneDangerProfileRegistry profiles;
    private final ArcaneResistanceProviderRegistry resistanceProviders;
    private final CorruptionResistanceProviderRegistry corruptionResistanceProviders;
    private final CorruptionStateService corruptionState;
    private final ArcaneStrainStateService strainState;
    private final boolean stateSettlementEnabled;
    private final HazardSessionActivator activator;
    private final Object stateReservationLock = new Object();
    private final Set<UUID> activeStatefulCasters = new HashSet<>();

    /** Backwards-compatible hazard-only constructor for isolated core consumers/tests. */
    public ArcaneHazardCastGate(
        ArcaneDangerProfileRegistry profiles,
        ArcaneResistanceProviderRegistry resistanceProviders,
        HazardSessionActivator activator
    ) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.resistanceProviders = Objects.requireNonNull(resistanceProviders, "resistanceProviders");
        this.corruptionResistanceProviders = null;
        this.corruptionState = null;
        this.strainState = null;
        this.stateSettlementEnabled = false;
        this.activator = Objects.requireNonNull(activator, "activator");
    }

    /** Canonical server constructor with committed-cast Corruption/Strain settlement enabled. */
    public ArcaneHazardCastGate(
        ArcaneDangerProfileRegistry profiles,
        ArcaneResistanceProviderRegistry resistanceProviders,
        CorruptionResistanceProviderRegistry corruptionResistanceProviders,
        CorruptionStateService corruptionState,
        ArcaneStrainStateService strainState,
        int maxStatefulPlayers,
        HazardSessionActivator activator
    ) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.resistanceProviders = Objects.requireNonNull(resistanceProviders, "resistanceProviders");
        this.corruptionResistanceProviders = Objects.requireNonNull(
            corruptionResistanceProviders, "corruptionResistanceProviders");
        this.corruptionState = Objects.requireNonNull(corruptionState, "corruptionState");
        this.strainState = Objects.requireNonNull(strainState, "strainState");
        if (maxStatefulPlayers <= 0
            || maxStatefulPlayers > Math.min(
                CorruptionStateService.ABSOLUTE_MAX_TRACKED_PLAYERS,
                ArcaneStrainStateService.ABSOLUTE_MAX_TRACKED_PLAYERS)) {
            throw new IllegalArgumentException("maxStatefulPlayers outside absolute bounds");
        }
        this.stateSettlementEnabled = true;
        this.activator = Objects.requireNonNull(activator, "activator");
    }

    @Override
    public HazardPreparation preflight(ArcanaCastRequest request, TargetResolution target) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");

        ArcaneDangerProfile profile = profiles.resolve(request.spell().id()).orElse(ArcaneDangerProfile.normal());
        if (!profile.requiresHazardSession()) return HazardPreparation.noop();

        ArcaneResistanceSnapshot resistance = resistanceProviders.snapshot(new ArcaneResistanceQuery(
            request.castId(),
            request.spell().id(),
            request.context().casterId(),
            request.context().dimensionId(),
            request.context().serverTick(),
            profile));

        if (resistance.effectiveResistance() < profile.minimumArcaneResistance()) {
            return denied(ArcanaDecision.deny(
                "hazard_minimum_resistance",
                "effective Arcane Resistance is below the server-required minimum"));
        }

        PreparedStateSettlement stateSettlement = null;
        if (stateSettlementEnabled) {
            UUID casterId = request.context().casterId();
            if (!hasStateCapacity(casterId, profile)) {
                return denied(ArcanaDecision.deny(
                    "hazard_state_capacity",
                    "persistent hazard state capacity is exhausted"));
            }

            CorruptionResistanceSnapshot corruptionResistance = corruptionResistanceProviders.snapshot(
                new CorruptionResistanceQuery(
                    request.castId(),
                    request.spell().id(),
                    casterId,
                    request.context().dimensionId(),
                    request.context().serverTick(),
                    profile));
            CorruptionAcquisitionProfile corruptionProfile =
                CorruptionAcquisitionProfile.committedCastOnly(profile.corruptionCoefficient(), 0.0D);
            CorruptionStateService.CorruptionPreflight corruptionPreflight = corruptionState.preflightCommittedCast(
                casterId,
                request.context().serverTick(),
                corruptionProfile,
                corruptionResistance);
            ArcaneStrainProfile strainProfile = baseCommittedCastStrain(profile.strainCoefficient());
            ArcaneStrainStateService.StrainPreflight strainPreflight = strainState.preflight(
                casterId,
                request.context().serverTick(),
                strainProfile,
                1.0D,
                0.0D,
                0L);
            if (strainPreflight.hardGateActive() || strainPreflight.predictedHardGate()) {
                return denied(ArcanaDecision.deny(
                    "hazard_strain_gate",
                    "Arcane Strain hard gate denies this cast"));
            }
            stateSettlement = new PreparedStateSettlement(
                casterId,
                request.context().serverTick(),
                corruptionPreflight,
                strainPreflight);
        }

        ArcaneHazardSnapshot snapshot = new ArcaneHazardSnapshot(
            request.castId(),
            request.spell().id(),
            request.context().casterId(),
            request.context().dimensionId(),
            request.context().serverTick(),
            profile);
        return new Prepared(snapshot, resistance, stateSettlement);
    }

    private boolean hasStateCapacity(UUID casterId, ArcaneDangerProfile profile) {
        if (profile.corruptionCoefficient() > 0.0D && !corruptionState.canReserve(casterId)) return false;
        return profile.strainCoefficient() <= 0.0D || strainState.canReserve(casterId);
    }

    private ArcanaDecision claimStateReservation(PreparedStateSettlement settlement) {
        if (!settlement.requiresStateWrite()) return ArcanaDecision.allow();
        synchronized (stateReservationLock) {
            UUID casterId = settlement.casterId();
            if (!activeStatefulCasters.add(casterId)) {
                return ArcanaDecision.deny(
                    "hazard_state_busy",
                    "another stateful hazard cast for this caster is still active");
            }

            boolean corruptionReserved = false;
            if (settlement.needsCorruptionWrite()) {
                corruptionReserved = corruptionState.reserve(casterId);
                if (!corruptionReserved) {
                    activeStatefulCasters.remove(casterId);
                    return ArcanaDecision.deny(
                        "hazard_state_capacity",
                        "persistent corruption state capacity is exhausted");
                }
            }
            if (settlement.needsStrainWrite() && !strainState.reserve(casterId)) {
                if (corruptionReserved) corruptionState.releaseReservation(casterId);
                activeStatefulCasters.remove(casterId);
                return ArcanaDecision.deny(
                    "hazard_state_capacity",
                    "persistent strain state capacity is exhausted");
            }
            return ArcanaDecision.allow();
        }
    }

    private void releaseStateReservation(PreparedStateSettlement settlement) {
        if (settlement == null || !settlement.requiresStateWrite()) return;
        synchronized (stateReservationLock) {
            if (settlement.needsCorruptionWrite()) corruptionState.releaseReservation(settlement.casterId());
            if (settlement.needsStrainWrite()) strainState.releaseReservation(settlement.casterId());
            activeStatefulCasters.remove(settlement.casterId());
        }
    }

    private static ArcaneStrainProfile baseCommittedCastStrain(double units) {
        return new ArcaneStrainProfile(units, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D);
    }

    private static HazardPreparation denied(ArcanaDecision decision) {
        return new HazardPreparation() {
            @Override public ArcanaDecision decision() { return decision; }
            @Override public ArcanaDecision activate() { return decision; }
            @Override public void commit() { }
            @Override public void cancel() { }
        };
    }

    private record PreparedStateSettlement(
        UUID casterId,
        long serverTick,
        CorruptionStateService.CorruptionPreflight corruptionPreflight,
        ArcaneStrainStateService.StrainPreflight strainPreflight
    ) {
        boolean needsCorruptionWrite() {
            return corruptionPreflight.appliedCorruption() > 0.0D;
        }

        boolean needsStrainWrite() {
            return strainPreflight.appliedStrain() > 0.0D;
        }

        boolean requiresStateWrite() {
            return needsCorruptionWrite() || needsStrainWrite();
        }
    }

    private final class Prepared implements HazardPreparation {
        private final ArcaneHazardSnapshot snapshot;
        private final ArcaneResistanceSnapshot resistance;
        private final PreparedStateSettlement stateSettlement;
        private boolean activated;
        private boolean stateReservationClaimed;
        private boolean committed;
        private boolean cancelled;

        private Prepared(
            ArcaneHazardSnapshot snapshot,
            ArcaneResistanceSnapshot resistance,
            PreparedStateSettlement stateSettlement
        ) {
            this.snapshot = snapshot;
            this.resistance = resistance;
            this.stateSettlement = stateSettlement;
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public synchronized ArcanaDecision activate() {
            if (committed) return ArcanaDecision.allow();
            if (cancelled) {
                return ArcanaDecision.deny("hazard_preparation_cancelled", "hazard preparation is already cancelled");
            }
            if (activated) return ArcanaDecision.allow();

            ArcanaDecision reservationDecision = stateSettlement == null
                ? ArcanaDecision.allow()
                : claimStateReservation(stateSettlement);
            if (!reservationDecision.allowed()) return reservationDecision;
            stateReservationClaimed = stateSettlement != null && stateSettlement.requiresStateWrite();

            final ArcaneHazardRuntime.ActivationResult result;
            try {
                result = activator.activate(
                    snapshot,
                    resistance,
                    ArcaneBacklashPolicy.canonical());
            } catch (RuntimeException | Error failure) {
                releaseClaimedStateReservation();
                throw failure;
            }
            if (!result.activated()) {
                releaseClaimedStateReservation();
                return ArcanaDecision.deny(result.code(), "hazard session activation was denied");
            }
            activated = true;
            return ArcanaDecision.allow();
        }

        @Override
        public synchronized void commit() {
            if (cancelled || committed) return;
            try {
                if (stateSettlement != null) {
                    if (stateSettlement.needsCorruptionWrite()) {
                        corruptionState.commitPrepared(
                            stateSettlement.casterId(),
                            stateSettlement.serverTick(),
                            stateSettlement.corruptionPreflight());
                    }
                    if (stateSettlement.needsStrainWrite()) {
                        strainState.commitPrepared(
                            stateSettlement.casterId(),
                            stateSettlement.serverTick(),
                            stateSettlement.strainPreflight());
                    }
                }
                committed = true;
            } finally {
                releaseClaimedStateReservation();
            }
        }

        @Override
        public synchronized void cancel() {
            if (committed || cancelled) return;
            cancelled = true;
            try {
                if (activated) activator.close(snapshot.rootCastId());
            } finally {
                releaseClaimedStateReservation();
            }
        }

        private void releaseClaimedStateReservation() {
            if (!stateReservationClaimed) return;
            releaseStateReservation(stateSettlement);
            stateReservationClaimed = false;
        }
    }
}
