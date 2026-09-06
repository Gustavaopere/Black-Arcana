package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftNoeticRuntime;
import dev.gustavopere.blackarcana.integration.rpg.RpgSkillTreeBridge;
import net.minecraft.server.MinecraftServer;
import net.neoforged.fml.ModList;

import java.util.Objects;
import java.util.Optional;

/** Loaded reflectively only when Ars Nouveau is present. */
public final class ArsServerIntegrationBootstrap {
    private ArsServerIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        String version = ModList.get().getModContainerById(ArsIntegrationBridge.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("not-loaded");
        ArsIntegrationBridge bridge = ArsIntegrationBridge.probe(true, version, server);
        runtime.integrations().register(bridge);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} capabilities={}{}",
            bridge.integrationId(),
            bridge.availability(),
            bridge.implementationVersion(),
            bridge.capabilities(),
            bridge.diagnostic().isBlank() ? "" : " diagnostic=" + bridge.diagnostic());

        if (!bridge.available()) return;

        bridge.familiarOwnershipProvider().ifPresent(provider -> {
            boolean registered = MinecraftNoeticRuntime.registerFamiliarOwnershipProvider(server, provider);
            if (!registered) {
                BlackArcanaMod.LOGGER.warn(
                    "Black Arcana did not register duplicate/capacity-limited familiar ownership provider {}",
                    provider.providerId());
            }
        });

        Optional<RpgSkillTreeBridge> rpg = runtime.integrations()
            .find(RpgSkillTreeBridge.MOD_ID)
            .filter(RpgSkillTreeBridge.class::isInstance)
            .map(RpgSkillTreeBridge.class::cast);
        ArsSyntheticContent.install(runtime, bridge.manaAccess(), rpg);
    }
}
