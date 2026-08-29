package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDangerProfileRuntimeStore;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentProfileRuntimeStore;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardCastGate;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;

import java.util.Objects;

/** Connects the server-neutral Stage 05A cast gate to the NeoForge damage pipeline. */
public final class NeoForgeHazardRuntimeInstaller {
    @FunctionalInterface
    interface ActivationTarget {
        ArcaneHazardRuntime.ActivationResult activate(
            ArcaneHazardSnapshot snapshot,
            ArcaneResistanceSnapshot resistance,
            ArcaneBacklashPolicy policy,
            ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
        );
    }

    @FunctionalInterface
    interface CloseTarget {
        boolean close(ArcanaCastId castId);
    }

    private NeoForgeHazardRuntimeInstaller() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        runtime.installHazardGate(new ArcaneHazardCastGate(
            ArcaneDangerProfileRuntimeStore.forRuntime(runtime),
            runtime.arcaneResistanceProviders(),
            runtime.corruptionResistanceProviders(),
            runtime.corruption(),
            runtime.strain(),
            ArcanaServerRuntime.DEFAULT_MAX_TRACKED_HAZARD_PLAYERS,
            createActivator(
                (snapshot, resistance, policy, emergencyProtectionSnapshot) ->
                    MinecraftArcaneDamagePipeline.activate(
                        server,
                        snapshot,
                        resistance,
                        policy,
                        emergencyProtectionSnapshot),
                castId -> MinecraftArcaneDamagePipeline.hazardRuntime(server)
                    .map(hazards -> hazards.close(castId))
                    .orElse(false))));
    }

    static ArcaneHazardCastGate.HazardSessionActivator createActivator(
        ActivationTarget activationTarget,
        CloseTarget closeTarget
    ) {
        Objects.requireNonNull(activationTarget, "activationTarget");
        Objects.requireNonNull(closeTarget, "closeTarget");
        return new ArcaneHazardCastGate.HazardSessionActivator() {
            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                ArcaneHazardSnapshot snapshot,
                ArcaneResistanceSnapshot resistance,
                ArcaneBacklashPolicy policy
            ) {
                return activationTarget.activate(
                    snapshot,
                    resistance,
                    policy,
                    ArcaneEmergencyProtectionSnapshot.empty());
            }

            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                ArcaneHazardSnapshot snapshot,
                ArcaneResistanceSnapshot resistance,
                ArcaneBacklashPolicy policy,
                ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
            ) {
                return activationTarget.activate(
                    snapshot,
                    resistance,
                    policy,
                    Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot"));
            }

            @Override
            public boolean close(ArcanaCastId castId) {
                return closeTarget.close(Objects.requireNonNull(castId, "castId"));
            }
        };
    }

    public static void remove(ArcanaServerRuntime runtime) {
        if (runtime == null) return;
        ArcaneDangerProfileRuntimeStore.remove(runtime);
        ArcaneEquipmentProfileRuntimeStore.remove(runtime);
    }
}
