package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.rpg.RpgSkillTreeBridge;
import net.minecraft.server.MinecraftServer;
import net.neoforged.fml.ModList;

import java.util.Objects;
import java.util.Optional;

/** Loaded reflectively after the server exists and only when Iron's is present. */
public final class IronsServerIntegrationBootstrap {
    private IronsServerIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        String version = ModList.get().getModContainerById(IronsIntegrationBridge.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("not-loaded");
        IronsIntegrationBridge bridge = IronsIntegrationBridge.probe(true, version, server);
        runtime.integrations().register(bridge);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} capabilities={}{}",
            bridge.integrationId(),
            bridge.availability(),
            bridge.implementationVersion(),
            bridge.capabilities(),
            bridge.diagnostic().isBlank() ? "" : " diagnostic=" + bridge.diagnostic());

        if (!bridge.available()) return;

        Optional<RpgSkillTreeBridge> rpg = runtime.integrations()
            .find(RpgSkillTreeBridge.MOD_ID)
            .filter(RpgSkillTreeBridge.class::isInstance)
            .map(RpgSkillTreeBridge.class::cast);
        IronsSyntheticContent.install(runtime, bridge.manaAccess(), rpg);
    }
}
