package dev.gustavopere.blackarcana;

import com.mojang.logging.LogUtils;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcaneEquipmentDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcaneEquipmentSetBonusDataReloadListener;
import dev.gustavopere.blackarcana.config.ArcanaSpellDataReloadListener;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftAnchorRecallRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftArcaneDamagePipeline;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftEchoArmamentRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftEphemeralTemperingRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftLawOfRecurrenceRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftRiftBladesRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftSoulAnchorRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftSpectralArsenalRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftSpiritSightRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftSympatheticWoundRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.OptionalModEntrypoints;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.HazardPreflightSyncService;
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
        modEventBus.addListener(LoadoutNetworkBridge::register);
        ArcanaNetworkBridge.installServerHandler(ArcanaServerRuntimeManager::handleCastIntent);
        ArcanaNetworkBridge.installClientResultHandler(ClientArcanaSyncState::acceptResult);
        ArcanaNetworkBridge.installClientCooldownHandler(ClientArcanaSyncState::acceptCooldowns);
        ArcanaNetworkBridge.installClientPresentationHandler(ClientArcanaSyncState::acceptPresentation);
        ArcanaNetworkBridge.installClientHazardPreflightHandler(ClientArcanaSyncState::acceptHazardPreflight);
        LoadoutNetworkBridge.installServerHandler(ArcanaServerRuntimeManager::handleLoadoutUpdate);
        LoadoutNetworkBridge.installClientHandler(ClientArcanaSyncState::acceptLoadout);
        ArcanaServerRuntimeManager.register(NeoForge.EVENT_BUS);
        MinecraftAnchorRecallRuntime.register(NeoForge.EVENT_BUS);
        MinecraftArcaneDamagePipeline.register(NeoForge.EVENT_BUS);
        MinecraftEchoArmamentRuntime.register(NeoForge.EVENT_BUS);
        MinecraftEphemeralTemperingRuntime.register(NeoForge.EVENT_BUS);
        MinecraftLawOfRecurrenceRuntime.register(NeoForge.EVENT_BUS);
        MinecraftRiftBladesRuntime.register(NeoForge.EVENT_BUS);
        MinecraftSoulAnchorRuntime.register(NeoForge.EVENT_BUS);
        MinecraftSpectralArsenalRuntime.register(NeoForge.EVENT_BUS);
        MinecraftSpiritSightRuntime.register(NeoForge.EVENT_BUS);
        MinecraftSympatheticWoundRuntime.register(NeoForge.EVENT_BUS);
        HazardPreflightSyncService.register(NeoForge.EVENT_BUS);
        ArcanaSpellDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneDangerDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneEquipmentDataReloadListener.register(NeoForge.EVENT_BUS);
        ArcaneEquipmentSetBonusDataReloadListener.register(NeoForge.EVENT_BUS);
        LOGGER.info("Black Arcana foundation loaded");
    }
}
