package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataDefinition;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneDangerProfileRuntimeStoreTest {
    @Test
    void reloadPublishesToExistingAndFutureRuntimeRegistries() {
        ArcanaSpellId id = ArcanaSpellId.parse("black_arcana:store_probe");
        ArcanaServerRuntime first = ArcanaServerRuntime.createDefault();
        ArcanaServerRuntime second = null;
        try {
            var firstRegistry = ArcaneDangerProfileRuntimeStore.forRuntime(first);
            ArcaneDangerProfileRuntimeStore.reload(Map.of(id, definition(id)));

            assertEquals(ArcaneDangerTier.DANGEROUS, firstRegistry.resolve(id).orElseThrow().tier());
            second = ArcanaServerRuntime.createDefault();
            assertEquals(
                ArcaneDangerTier.DANGEROUS,
                ArcaneDangerProfileRuntimeStore.forRuntime(second).resolve(id).orElseThrow().tier());
        } finally {
            ArcaneDangerProfileRuntimeStore.reload(Map.of());
            ArcaneDangerProfileRuntimeStore.remove(first);
            if (second != null) ArcaneDangerProfileRuntimeStore.remove(second);
        }
    }

    @Test
    void invalidReloadPreservesPreviouslyPublishedSnapshot() {
        ArcanaSpellId stable = ArcanaSpellId.parse("black_arcana:stable_hazard");
        try {
            ArcaneDangerProfileRuntimeStore.reload(Map.of(stable, definition(stable)));
            Map<ArcanaSpellId, ?> before = ArcaneDangerProfileRuntimeStore.currentSnapshot();

            LinkedHashMap<ArcanaSpellId, ArcaneDangerDataDefinition> invalid = new LinkedHashMap<>();
            invalid.put(ArcanaSpellId.parse("black_arcana:broken_hazard"), null);

            assertThrows(NullPointerException.class, () -> ArcaneDangerProfileRuntimeStore.reload(invalid));
            assertEquals(before, ArcaneDangerProfileRuntimeStore.currentSnapshot());
        } finally {
            ArcaneDangerProfileRuntimeStore.reload(Map.of());
        }
    }

    private static ArcaneDangerDataDefinition definition(ArcanaSpellId id) {
        return new ArcaneDangerDataDefinition(
            1, 1, id.canonical(), ArcaneDangerTier.DANGEROUS,
            1.0D, 1.0D, 1.0D, 100L, 8, 20.0D, 40.0D, true);
    }
}
