package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;

/** Runtime-scoped atomic publication store for Stage 05A containment set bonuses. */
public final class ArcaneEquipmentSetBonusRuntimeStore {
    private static final Map<ArcanaServerRuntime, ArcaneEquipmentSetBonusRegistry> REGISTRIES =
        Collections.synchronizedMap(new IdentityHashMap<>());
    private static volatile Map<String, ArcaneEquipmentSetBonus> CURRENT = Map.of();

    private ArcaneEquipmentSetBonusRuntimeStore() { }

    public static ArcaneEquipmentSetBonusRegistry forRuntime(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        synchronized (REGISTRIES) {
            ArcaneEquipmentSetBonusRegistry existing = REGISTRIES.get(runtime);
            if (existing != null) return existing;
            ArcaneEquipmentSetBonusRegistry registry = runtime.arcaneEquipmentSetBonuses();
            registry.replaceAll(CURRENT);
            REGISTRIES.put(runtime, registry);
            return registry;
        }
    }

    public static void reload(Map<String, ArcaneEquipmentSetBonus> bonuses) {
        Objects.requireNonNull(bonuses, "bonuses");
        ArcaneEquipmentSetBonusRegistry validator = new ArcaneEquipmentSetBonusRegistry();
        validator.replaceAll(bonuses);
        Map<String, ArcaneEquipmentSetBonus> published = validator.snapshot();
        synchronized (REGISTRIES) {
            REGISTRIES.values().forEach(registry -> registry.replaceAll(published));
            CURRENT = published;
        }
    }

    public static Map<String, ArcaneEquipmentSetBonus> currentSnapshot() { return CURRENT; }

    public static void remove(ArcanaServerRuntime runtime) {
        REGISTRIES.remove(Objects.requireNonNull(runtime, "runtime"));
    }
}
