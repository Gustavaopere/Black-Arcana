package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.Objects;

/** Loads adapter classes only after NeoForge confirms their provider mod exists. */
public final class OptionalModEntrypoints {
    private static final Map<String, String> MOD_BUS_ENTRYPOINTS = Map.of(
        "irons_spellbooks",
        "dev.gustavopere.blackarcana.integration.irons.IronsOptionalModBootstrap"
    );
    private static final Map<String, String> SERVER_ENTRYPOINTS = Map.of(
        "irons_spellbooks",
        "dev.gustavopere.blackarcana.integration.irons.IronsServerIntegrationBootstrap",
        "ars_nouveau",
        "dev.gustavopere.blackarcana.integration.ars.ArsServerIntegrationBootstrap"
    );

    private OptionalModEntrypoints() { }

    public static void install(IEventBus modEventBus) {
        Objects.requireNonNull(modEventBus, "modEventBus");
        ModList mods = ModList.get();
        MOD_BUS_ENTRYPOINTS.forEach((modId, className) -> {
            if (!mods.isLoaded(modId)) return;
            invokeModBus(modId, className, modEventBus);
        });
    }

    public static void installServer(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");
        ModList mods = ModList.get();
        SERVER_ENTRYPOINTS.forEach((modId, className) -> {
            if (!mods.isLoaded(modId)) return;
            invokeServer(modId, className, server, runtime);
        });
    }

    private static void invokeModBus(String modId, String className, IEventBus modEventBus) {
        try {
            Class<?> entrypoint = load(className);
            Method register = entrypoint.getMethod("register", IEventBus.class);
            register.invoke(null, modEventBus);
            BlackArcanaMod.LOGGER.info("Installed optional Black Arcana mod-bus adapter for {}", modId);
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | LinkageError failure) {
            BlackArcanaMod.LOGGER.error("Could not install optional Black Arcana mod-bus adapter for {}", modId, failure);
        } catch (InvocationTargetException failure) {
            logInvocationFailure(modId, "mod-bus registration", failure);
        }
    }

    private static void invokeServer(
        String modId,
        String className,
        MinecraftServer server,
        ArcanaServerRuntime runtime
    ) {
        try {
            Class<?> entrypoint = load(className);
            Method install = entrypoint.getMethod("install", MinecraftServer.class, ArcanaServerRuntime.class);
            install.invoke(null, server, runtime);
            BlackArcanaMod.LOGGER.info("Installed optional Black Arcana server adapter for {}", modId);
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | LinkageError failure) {
            BlackArcanaMod.LOGGER.error("Could not install optional Black Arcana server adapter for {}", modId, failure);
        } catch (InvocationTargetException failure) {
            logInvocationFailure(modId, "server installation", failure);
        }
    }

    private static Class<?> load(String className) throws ClassNotFoundException {
        return Class.forName(className, true, OptionalModEntrypoints.class.getClassLoader());
    }

    private static void logInvocationFailure(String modId, String phase, InvocationTargetException failure) {
        Throwable cause = failure.getCause() == null ? failure : failure.getCause();
        BlackArcanaMod.LOGGER.error("Optional Black Arcana adapter for {} failed during {}", modId, phase, cause);
    }
}
