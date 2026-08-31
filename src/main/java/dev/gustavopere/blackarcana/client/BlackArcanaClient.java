package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.NeoForge;

/** Physical-client entrypoint; no class in this package is loaded by a dedicated server. */
@Mod(value = BlackArcanaMod.MOD_ID, dist = Dist.CLIENT)
public final class BlackArcanaClient {
    public BlackArcanaClient(IEventBus modEventBus, ModContainer container) {
        container.registerConfig(ModConfig.Type.CLIENT, BlackArcanaClientConfig.SPEC);
        modEventBus.addListener(BlackArcanaKeyMappings::register);
        modEventBus.addListener(BlackArcanaHudLayer::register);
        ArcanaNetworkBridge.installClientBorrowedSightCameraHandler(BorrowedSightClientCamera::accept);
        ClientInputController.register(NeoForge.EVENT_BUS);
        ClientInputController.installRadialOpener(BlackArcanaRadialScreen::open);
        ClientInputController.installLoadoutEditorOpener(BlackArcanaLoadoutScreen::open);
    }
}
