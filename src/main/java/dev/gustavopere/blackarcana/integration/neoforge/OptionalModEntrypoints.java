package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.core.integration.UnavailableOptionalIntegration;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;

/** Loads adapter classes only after NeoForge confirms their provider mod exists. */
public final class OptionalModEntrypoints {
    private static final Map<String, String> MOD_BUS_ENTRYPOINTS = Map.of(
        "irons_spellbooks",
        "dev.gustavopere.blackarcana.integration.irons.IronsOptionalModBootstrap",
        "eidolon_repraised",
        "dev.gustavopere.blackarcana.integration.eidolon.EidolonOptionalModBootstrap"
    );
    private static final Map<String, String> SERVER_ENTRYPOINTS = Map.of(
        "irons_spellbooks",
        "dev.gustavopere.blackarcana.integration.irons.IronsServerIntegrationBootstrap",
        "ars_nouveau",
        "dev.gustavopere.blackarcana.integration.ars.ArsServerIntegrationBootstrap",
        "malum",
        "dev.gustavopere.blackarcana.integration.malum.MalumServerIntegrationBootstrap",
        "eidolon_repraised",
        "dev.gustavopere.blackarcana.integration.eidolon.EidolonServerIntegrationBootstrap",
        "curios",
        "dev.gustavopere.blackarcana.integration.curios.CuriosServerIntegrationBootstrap"
    );
    private static final Map<String, String> MOD_BUS_FAILURES = new ConcurrentHashMap<>();

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
            if (!mods.isLoaded(modId)) {
                registerUnavailable(runtime, modId, ArcanaIntegrationAvailability.MISSING_MOD,
                    "not-loaded", "Optional integration mod is not loaded: " + modId);
                return;
            }

            String version = mods.getModContainerById(modId)
                .map(container -> container.getModInfo().getVersion().toString())
                .orElse("unknown");
            String modBusFailure = MOD_BUS_FAILURES.get(modId);
            if (modBusFailure != null) {
                registerUnavailable(runtime, modId, ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                    version, modBusFailure);
                return;
            }
            invokeServer(modId, className, version, server, runtime);
        });
    }

    private static void invokeModBus(String modId, String className, IEventBus modEventBus) {
        try {
            Class<?> entrypoint = load(className);
            Method register = entrypoint.getMethod("register", IEventBus.class);
            register.invoke(null, modEventBus);
            BlackArcanaMod.LOGGER.info("Installed optional Black Arcana mod-bus adapter for {}", modId);
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | LinkageError failure) {
            recordModBusFailure(modId, failure);
            BlackArcanaMod.LOGGER.error("Could not install optional Black Arcana mod-bus adapter for {}", modId, failure);
        } catch (InvocationTargetException failure) {
            Throwable cause = failure.getCause() == null ? failure : failure.getCause();
            recordModBusFailure(modId, cause);
            BlackArcanaMod.LOGGER.error("Optional Black Arcana adapter for {} failed during mod-bus registration", modId, cause);
        }
    }

    private static void invokeServer(
        String modId,
        String className,
        String version,
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
            registerUnavailable(runtime, modId, ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version, diagnostic("server adapter linkage failed", failure));
        } catch (InvocationTargetException failure) {
            Throwable cause = failure.getCause() == null ? failure : failure.getCause();
            BlackArcanaMod.LOGGER.error("Optional Black Arcana adapter for {} failed during server installation", modId, cause);
            registerUnavailable(runtime, modId, ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version, diagnostic("server adapter installation failed", cause));
        }
    }

    private static void registerUnavailable(
        ArcanaServerRuntime runtime,
        String modId,
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic
    ) {
        if (runtime.integrations().find(modId).isPresent()) return;
        runtime.integrations().register(new UnavailableOptionalIntegration(modId, availability, version, diagnostic));
    }

    private static void recordModBusFailure(String modId, Throwable failure) {
        MOD_BUS_FAILURES.put(modId, diagnostic("mod-bus adapter registration failed", failure));
    }

    private static String diagnostic(String phase, Throwable failure) {
        return phase + ": " + failure.getClass().getSimpleName();
    }

    private static Class<?> load(String className) throws ClassNotFoundException {
        return Class.forName(className, true, OptionalModEntrypoints.class.getClassLoader());
    }
}
