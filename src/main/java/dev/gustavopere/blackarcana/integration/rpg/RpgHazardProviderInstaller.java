package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.core.hazard.ArcaneResistancePreviewRuntimeStore;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Objects;

/** Installs the read-only RPG hazard adapter into both Black Arcana resistance channels. */
public final class RpgHazardProviderInstaller {
    private RpgHazardProviderInstaller() { }

    public static void install(ArcanaServerRuntime runtime, RpgSkillTreeBridge bridge) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(bridge, "bridge");

        RpgHazardResistanceProvider provider = new RpgHazardResistanceProvider(
            bridge,
            RpgHazardResistanceConfig.canonical());
        runtime.arcaneResistanceProviders().register(provider);
        runtime.corruptionResistanceProviders().register(provider);
        // This adapter is already a pure read-only query over the RPG public snapshot boundary.
        ArcaneResistancePreviewRuntimeStore.register(runtime, provider);
    }
}
