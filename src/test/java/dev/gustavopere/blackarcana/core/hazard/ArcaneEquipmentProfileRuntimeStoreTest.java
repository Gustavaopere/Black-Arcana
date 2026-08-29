package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentProfileRuntimeStoreTest {
    @Test
    void reloadPublishesAtomicallyToExistingAndFutureRuntimes() {
        ArcanaServerRuntimeRuntimePair pair = new ArcanaServerRuntimeRuntimePair(
            ArcanaServerRuntime.createDefault(), ArcanaServerRuntime.createDefault());
        try {
            ArcaneEquipmentProfileRuntimeStore.reload(Map.of(
                "minecraft:golden_helmet",
                ArcaneEquipmentProfile.resistanceOnly("black_arcana:first", 20.0D, 10.0D)));

            var first = ArcaneEquipmentProfileRuntimeStore.forRuntime(pair.first());
            assertEquals(20.0D, first.resolve("minecraft:golden_helmet").orElseThrow().arcaneResistance());

            ArcaneEquipmentProfileRuntimeStore.reload(Map.of(
                "minecraft:diamond_helmet",
                ArcaneEquipmentProfile.resistanceOnly("black_arcana:second", 35.0D, 12.0D)));

            assertTrue(first.resolve("minecraft:golden_helmet").isEmpty());
            assertEquals(35.0D, first.resolve("minecraft:diamond_helmet").orElseThrow().arcaneResistance());
            var second = ArcaneEquipmentProfileRuntimeStore.forRuntime(pair.second());
            assertEquals(35.0D, second.resolve("minecraft:diamond_helmet").orElseThrow().arcaneResistance());
        } finally {
            ArcaneEquipmentProfileRuntimeStore.remove(pair.first());
            ArcaneEquipmentProfileRuntimeStore.remove(pair.second());
            ArcaneEquipmentProfileRuntimeStore.reload(Map.of());
        }
    }

    private record ArcanaServerRuntimeRuntimePair(ArcanaServerRuntime first, ArcanaServerRuntime second) { }
}
