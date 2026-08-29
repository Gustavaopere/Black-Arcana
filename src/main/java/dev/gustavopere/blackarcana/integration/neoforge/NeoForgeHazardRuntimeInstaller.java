package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDangerProfileRuntimeStore;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardCastGate;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;

import java.util.Objects;

/** Connects the server-neutral Stage 05A cast gate to the NeoForge damage pipeline. */
public final class NeoForgeHazardRuntimeInstaller {
    private NeoForgeHazardRuntimeInstaller() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        runtime.installHazardGate(new ArcaneHazardCastGate(
            ArcaneDangerProfileRuntimeStore.forRuntime(runtime),
            runtime.arcaneResistanceProviders(),
            new ArcaneHazardCastGate.HazardSessionActivator() {
                @Override
                public ArcaneHazardRuntime.ActivationResult activate(
                    ArcaneHazardSnapshot snapshot,
                    ArcaneResistanceSnapshot resistance,
                    ArcaneBacklashPolicy policy
                ) {
                    return MinecraftArcaneDamagePipeline.activate(server, snapshot, resistance, policy);
                }

                @Override
                public boolean close(ArcanaCastId castId) {
                    return MinecraftArcaneDamagePipeline.hazardRuntime(server)
                        .map(hazards -> hazards.close(castId))
                        .orElse(false);
                }
            }));
    }

    public static void remove(ArcanaServerRuntime runtime) {
        if (runtime != null) ArcaneDangerProfileRuntimeStore.remove(runtime);
    }
}
