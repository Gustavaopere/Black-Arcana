package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataDefinition;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/**
 * Stage 05A hazard state keyed by runtime identity, intentionally outside the frozen Stage 02 runtime API.
 * Reload publication is atomic and never depends on client state.
 */
public final class ArcaneDangerProfileRuntimeStore {
    private static final Map<ArcanaServerRuntime, ArcaneDangerProfileRegistry> REGISTRIES =
        Collections.synchronizedMap(new IdentityHashMap<>());
    private static volatile Map<ArcanaSpellId, ArcaneDangerProfile> CURRENT = Map.of();

    private ArcaneDangerProfileRuntimeStore() { }

    public static ArcaneDangerProfileRegistry forRuntime(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        synchronized (REGISTRIES) {
            return REGISTRIES.computeIfAbsent(runtime, ignored -> {
                ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
                registry.replaceAll(CURRENT);
                return registry;
            });
        }
    }

    public static void reload(Map<ArcanaSpellId, ArcaneDangerDataDefinition> definitions) {
        Objects.requireNonNull(definitions, "definitions");
        LinkedHashMap<ArcanaSpellId, ArcaneDangerProfile> converted = new LinkedHashMap<>();
        definitions.forEach((id, definition) -> {
            Objects.requireNonNull(id, "danger profile id");
            Objects.requireNonNull(definition, "danger profile definition");
            if (converted.putIfAbsent(id, definition.toRuntimeProfile()) != null) {
                throw new IllegalArgumentException("duplicate danger profile: " + id.canonical());
            }
        });
        ArcaneDangerProfileRegistry validator = new ArcaneDangerProfileRegistry();
        validator.replaceAll(converted);
        Map<ArcanaSpellId, ArcaneDangerProfile> published = validator.snapshot();
        synchronized (REGISTRIES) {
            REGISTRIES.values().forEach(registry -> registry.replaceAll(published));
            CURRENT = published;
        }
    }

    public static Map<ArcanaSpellId, ArcaneDangerProfile> currentSnapshot() {
        return CURRENT;
    }

    public static void remove(ArcanaServerRuntime runtime) {
        REGISTRIES.remove(Objects.requireNonNull(runtime, "runtime"));
    }
}
