package dev.gustavopere.blackarcana;

import com.mojang.logging.LogUtils;
import dev.gustavopere.blackarcana.config.ArcanaSpellDataReloadListener;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.integration.neoforge.OptionalModEntrypoints;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
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
        LoadoutNetworkBridge.installServerHandler(ArcanaServerRuntimeManager::handleLoadoutUpdate);
        LoadoutNetworkBridge.installClientHandler(ClientArcanaSyncState::acceptLoadout);
        ArcanaServerRuntimeManager.register(NeoForge.EVENT_BUS);
        ArcanaSpellDataReloadListener.register(NeoForge.EVENT_BUS);
        LOGGER.info("Black Arcana foundation loaded");
    }
}
