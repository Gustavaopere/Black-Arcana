package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.AstralSeveranceNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.NoeticViewNetworkBridge;
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
        modEventBus.addListener(TargetAimPresentationLayer::register);
        modEventBus.addListener(CastPresentationEffectsLayer::register);
        modEventBus.addListener(DiscoverabilityHintLayer::register);
        modEventBus.addListener(SpellIconResolver::registerReloadListener);
        modEventBus.addListener(CastPresentationResources::registerReloadListener);
        modEventBus.addListener(AstralProjectionClientRegistration::register);
        ClientArcanaSyncState.installResultObserver(CastPresentationClientRuntime::acceptResult);
        ClientArcanaSyncState.installLoadoutObserver(DiscoverabilityClientRuntime::acceptLoadout);
        CastPresentationClientRuntime.installSink(CastPresentationEffectsLayer::accept);
        ClientInputController.register(NeoForge.EVENT_BUS);
        HazardResistanceForecastClientController.register(NeoForge.EVENT_BUS);
        BorrowedSightClientController.register(NeoForge.EVENT_BUS);
        AstralSeveranceClientController.register(NeoForge.EVENT_BUS);
        AstralSeveranceInputController.register(NeoForge.EVENT_BUS);
        NoeticViewNetworkBridge.installClientHandler(BorrowedSightClientController::accept);
        AstralSeveranceNetworkBridge.installViewHandler(AstralSeveranceClientController::accept);
        ClientInputController.installRadialOpener(BlackArcanaRadialScreen::open);
        ClientInputController.installLoadoutEditorOpener(BlackArcanaLoadoutScreen::open);
    }
}
