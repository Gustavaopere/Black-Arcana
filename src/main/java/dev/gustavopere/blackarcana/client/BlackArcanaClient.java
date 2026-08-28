package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;

/** Physical-client entrypoint; no class in this package is loaded by a dedicated server. */
@Mod(value = BlackArcanaMod.MOD_ID, dist = Dist.CLIENT)
public final class BlackArcanaClient {
    public BlackArcanaClient(IEventBus modEventBus) {
        modEventBus.addListener(BlackArcanaKeyMappings::register);
        ClientInputController.register(NeoForge.EVENT_BUS);
    }
}
