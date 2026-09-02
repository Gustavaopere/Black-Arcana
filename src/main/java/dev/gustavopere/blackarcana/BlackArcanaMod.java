package dev.gustavopere.blackarcana;

import com.mojang.logging.LogUtils;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcaneEquipmentDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcaneEquipmentSetBonusDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcanaSpellDataReloadListener;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftArcaneDamagePipeline;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftLawOfRecurrenceRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.OptionalModEntrypoints;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.HazardPreflightSyncService;
import dev.gustavopere.blackarcana.network.neoforge.HazardResistanceForecastNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.HazardResistanceForecastService;
import dev.gustavopere.blackarcana.network.neoforge.LoadoutNetworkBridge;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;

@Mod(BlackArcanaMod.MOD_ID)
public final class BlackArcanaMod {
    public static final String MOD_ID = "black_arcana";
    public static final Logger LOGGER = LogUtils.getLogger();

    public BlackArcanaMod(IEventBus modEventBus) {
        OptionalModEntrypoints.install(modEventBus);
        modEventBus.addListener(ArcanaNetworkBridge::register);
        modEventBus.addListener(HazardResistanceForecastNetworkBridge::register);
        modEventBus.addListener(LoadoutNetworkBridge::register);
        ArcanaNetworkBridge.installServerHandler(ArcanaServerRuntimeManager::handleCastIntent);
        ArcanaNetworkBridge.installClientResultHandler(ClientArcanaSyncState::acceptResult);
        ArcanaNetworkBridge.installClientCooldownHandler(ClientArcanaSyncState::acceptCooldowns);
        ArcanaNetworkBridge.installClientPresentationHandler(ClientArcanaSyncState::acceptPresentation);
        ArcanaNetworkBridge.installClientHazardPreflightHandler(ClientArcanaSyncState::acceptHazardPreflight);
        HazardResistanceForecastNetworkBridge.installServerHandler(HazardResistanceForecastService::handle);
        HazardResistanceForecastNetworkBridge.installClientHandler(ClientArcanaSyncState::acceptHazardResistanceForecast);
        LoadoutNetworkBridge.installServerHandler(ArcanaServerRuntimeManager::handleLoadoutUpdate);
        LoadoutNetworkBridge.installClientHandler(ClientArcanaSyncState::acceptLoadout);
        ArcanaServerRuntimeManager.register(NeoForge.EVENT_BUS);
        MinecraftArcaneDamagePipeline.register(NeoForge.EVENT_BUS);
        MinecraftLawOfRecurrenceRuntime.register(NeoForge.EVENT_BUS);
        HazardPreflightSyncService.register(NeoForge.EVENT_BUS);
        HazardResistanceForecastService.register(NeoForge.EVENT_BUS);
        ArcanaSpellDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneDangerDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneEquipmentDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneEquipmentSetBonusDataReloadListener.register(NeoForge.EVENT_BUS);
        LOGGER.info("Black Arcana foundation loaded");
    }
}
