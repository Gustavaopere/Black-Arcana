package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.rpg.ReflectiveRpgSkillTreeBridge;
import dev.gustavopere.blackarcana.integration.rpg.RpgHazardProviderInstaller;
import dev.gustavopere.blackarcana.integration.rpg.RpgSkillTreeBridge;
import java.util.Objects;
import net.minecraft.server.MinecraftServer;
import net.neoforged.fml.ModList;

/** Installs server-scoped optional integration descriptors before gameplay initialization. */
public final class NeoForgeIntegrationBootstrap {
    private NeoForgeIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        StandardEquipmentHazardProviderInstaller.install(server, runtime);

        ModList mods = ModList.get();
        boolean rpgLoaded = mods.isLoaded(RpgSkillTreeBridge.MOD_ID);
        String rpgVersion = mods.getModContainerById(RpgSkillTreeBridge.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("not-loaded");
        ReflectiveRpgSkillTreeBridge rpg = ReflectiveRpgSkillTreeBridge.probe(
            rpgLoaded,
            rpgVersion,
            server.getPlayerList()::getPlayer);
        runtime.integrations().register(rpg);
        RpgHazardProviderInstaller.install(runtime, rpg);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} capabilities={}{}",
            rpg.integrationId(),
            rpg.availability(),
            rpg.implementationVersion(),
            rpg.capabilities(),
            rpg.diagnostic().isBlank() ? "" : " diagnostic=" + rpg.diagnostic());

        // Provider-specific classes are loaded only after ModList confirms presence.
        OptionalModEntrypoints.installServer(server, runtime);
    }
}
