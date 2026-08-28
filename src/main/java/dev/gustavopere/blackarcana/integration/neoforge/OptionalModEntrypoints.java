package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.integration.irons.IronsIntegrationBridge;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.Objects;

/** Loads adapter classes only after NeoForge confirms their provider mod exists. */
public final class OptionalModEntrypoints {
    private static final Map<String, String> ENTRYPOINTS = Map.of(
        IronsIntegrationBridge.MOD_ID,
        "dev.gustavopere.blackarcana.integration.irons.IronsOptionalModBootstrap"
    );

    private OptionalModEntrypoints() { }

    public static void install(IEventBus modEventBus) {
        Objects.requireNonNull(modEventBus, "modEventBus");
        ModList mods = ModList.get();
        ENTRYPOINTS.forEach((modId, className) -> {
            if (!mods.isLoaded(modId)) return;
            installOne(modId, className, modEventBus);
        });
    }

    private static void installOne(String modId, String className, IEventBus modEventBus) {
        try {
            Class<?> entrypoint = Class.forName(className, true, OptionalModEntrypoints.class.getClassLoader());
            Method register = entrypoint.getMethod("register", IEventBus.class);
            register.invoke(null, modEventBus);
            BlackArcanaMod.LOGGER.info("Installed optional Black Arcana mod-bus adapter for {}", modId);
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | LinkageError failure) {
            BlackArcanaMod.LOGGER.error("Could not install optional Black Arcana adapter for {}", modId, failure);
        } catch (InvocationTargetException failure) {
            Throwable cause = failure.getCause() == null ? failure : failure.getCause();
            BlackArcanaMod.LOGGER.error("Optional Black Arcana adapter for {} failed during registration", modId, cause);
        }
    }
}
