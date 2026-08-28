package dev.gustavopere.blackarcana.integration.eidolon;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;

import java.util.Objects;

/** Loaded reflectively only when Eidolon: Repraised is present. */
public final class EidolonOptionalModBootstrap {
    private EidolonOptionalModBootstrap() { }

    public static void register(IEventBus modEventBus) {
        Objects.requireNonNull(modEventBus, "modEventBus");
        modEventBus.addListener(EidolonOptionalModBootstrap::commonSetup);
    }

    private static void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(EidolonRitualRegistration::register);
    }
}
