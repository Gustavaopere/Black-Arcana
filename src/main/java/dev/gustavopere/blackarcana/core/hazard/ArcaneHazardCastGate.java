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

import java.util.Objects;

/**
 * Server-neutral Stage 05A gate that freezes the danger/resistance snapshot during
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
    private final HazardSessionActivator activator;

    public ArcaneHazardCastGate(
        ArcaneDangerProfileRegistry profiles,
        ArcaneResistanceProviderRegistry resistanceProviders,
        HazardSessionActivator activator
    ) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.resistanceProviders = Objects.requireNonNull(resistanceProviders, "resistanceProviders");
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
            return denied(
                ArcanaDecision.deny(
                    "hazard_minimum_resistance",
                    "effective Arcane Resistance is below the server-required minimum"));
        }

        ArcaneHazardSnapshot snapshot = new ArcaneHazardSnapshot(
            request.castId(),
            request.spell().id(),
            request.context().casterId(),
            request.context().dimensionId(),
            request.context().serverTick(),
            profile);
        return new Prepared(snapshot, resistance);
    }

    private static HazardPreparation denied(ArcanaDecision decision) {
        return new HazardPreparation() {
            @Override public ArcanaDecision decision() { return decision; }
            @Override public ArcanaDecision activate() { return decision; }
            @Override public void commit() { }
            @Override public void cancel() { }
        };
    }

    private final class Prepared implements HazardPreparation {
        private final ArcaneHazardSnapshot snapshot;
        private final ArcaneResistanceSnapshot resistance;
        private boolean activated;
        private boolean committed;
        private boolean cancelled;

        private Prepared(ArcaneHazardSnapshot snapshot, ArcaneResistanceSnapshot resistance) {
            this.snapshot = snapshot;
            this.resistance = resistance;
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

            ArcaneHazardRuntime.ActivationResult result = activator.activate(
                snapshot,
                resistance,
                ArcaneBacklashPolicy.canonical());
            if (!result.activated()) {
                return ArcanaDecision.deny(result.code(), "hazard session activation was denied");
            }
            activated = true;
            return ArcanaDecision.allow();
        }

        @Override
        public synchronized void commit() {
            if (cancelled) return;
            committed = true;
        }

        @Override
        public synchronized void cancel() {
            if (committed || cancelled) return;
            cancelled = true;
            if (activated) activator.close(snapshot.rootCastId());
        }
    }
}
