package dev.gustavopere.blackarcana;

import com.mojang.logging.LogUtils;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;

@Mod(BlackArcanaMod.MOD_ID)
public final class BlackArcanaMod {
    public static final String MOD_ID = "black_arcana";
    public static final Logger LOGGER = LogUtils.getLogger();

    public BlackArcanaMod(IEventBus modEventBus) {
        modEventBus.addListener(ArcanaNetworkBridge::register);
        LOGGER.info("Black Arcana foundation loaded");
    }
}
