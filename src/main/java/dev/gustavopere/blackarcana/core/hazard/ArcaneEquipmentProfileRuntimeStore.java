package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;

/** Runtime-scoped atomic publication store for explicit Stage 05A containment equipment profiles. */
public final class ArcaneEquipmentProfileRuntimeStore {
    private static final Map<ArcanaServerRuntime, ArcaneEquipmentProfileRegistry> REGISTRIES =
        Collections.synchronizedMap(new IdentityHashMap<>());
    private static volatile Map<String, ArcaneEquipmentProfile> CURRENT = Map.of();

    private ArcaneEquipmentProfileRuntimeStore() { }

    public static ArcaneEquipmentProfileRegistry forRuntime(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        synchronized (REGISTRIES) {
            ArcaneEquipmentProfileRegistry existing = REGISTRIES.get(runtime);
            if (existing != null) return existing;
            ArcaneEquipmentProfileRegistry registry = runtime.arcaneEquipmentProfiles();
            registry.replaceAll(CURRENT);
            REGISTRIES.put(runtime, registry);
            return registry;
        }
    }

    public static void reload(Map<String, ArcaneEquipmentProfile> profiles) {
        Objects.requireNonNull(profiles, "profiles");
        ArcaneEquipmentProfileRegistry validator = new ArcaneEquipmentProfileRegistry();
        validator.replaceAll(profiles);
        Map<String, ArcaneEquipmentProfile> published = validator.snapshot();
        synchronized (REGISTRIES) {
            REGISTRIES.values().forEach(registry -> registry.replaceAll(published));
            CURRENT = published;
        }
    }

    public static Map<String, ArcaneEquipmentProfile> currentSnapshot() {
        return CURRENT;
    }

    public static void remove(ArcanaServerRuntime runtime) {
        REGISTRIES.remove(Objects.requireNonNull(runtime, "runtime"));
    }
}
