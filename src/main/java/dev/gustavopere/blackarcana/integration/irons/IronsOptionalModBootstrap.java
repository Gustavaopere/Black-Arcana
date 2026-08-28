package dev.gustavopere.blackarcana.integration.irons;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.NeoForge;

import java.util.Objects;
import java.util.concurrent.atomic.AtomicBoolean;

/** Loaded reflectively only when Iron's is present. */
public final class IronsOptionalModBootstrap {
    private static final AtomicBoolean REGISTERED = new AtomicBoolean();

    private IronsOptionalModBootstrap() { }

    public static void register(IEventBus modEventBus) {
        Objects.requireNonNull(modEventBus, "modEventBus");
        if (!REGISTERED.compareAndSet(false, true)) return;
        IronsSpellRegistryBridge.register(modEventBus);
        NeoForge.EVENT_BUS.register(IronsHostedSpellEvents.class);
    }
}
