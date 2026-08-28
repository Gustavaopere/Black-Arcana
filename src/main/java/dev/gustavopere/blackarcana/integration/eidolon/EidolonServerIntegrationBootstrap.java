package dev.gustavopere.blackarcana.integration.eidolon;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;
import net.neoforged.fml.ModList;

import java.util.Objects;

/** Loaded reflectively only when Eidolon: Repraised is present. */
public final class EidolonServerIntegrationBootstrap {
    private EidolonServerIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        String version = ModList.get().getModContainerById(EidolonIntegrationIds.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("not-loaded");
        EidolonIntegrationBridge bridge = EidolonIntegrationBridge.probe(
            true,
            version,
            EidolonRitualRegistration::isRegistered);
        runtime.integrations().register(bridge);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} capabilities={}{}",
            bridge.integrationId(),
            bridge.availability(),
            bridge.implementationVersion(),
            bridge.capabilities(),
            bridge.diagnostic().isBlank() ? "" : " diagnostic=" + bridge.diagnostic());
    }
}
