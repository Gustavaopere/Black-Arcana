package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentDataReloadListenerTest {
    private static final ResourceLocation ID =
        ResourceLocation.fromNamespaceAndPath("black_arcana", "containment/test_helm");

    @Test
    void parsesExplicitItemProfileWithoutImplicitVanillaStats() {
        var definition = ArcaneEquipmentDataReloadListener.parseDefinition(ID, JsonParser.parseString(validJson()));

        assertEquals("black_arcana:containment/test_helm", definition.id());
        assertEquals("minecraft:golden_helmet", definition.itemId());
        assertEquals(25.0D, definition.profile().arcaneResistance());
        assertEquals(15.0D, definition.profile().corruptionResistance());
        assertEquals("black_arcana:test_set", definition.profile().setId());
        assertTrue(definition.profile().containmentTags().contains("black_arcana:ward"));
    }

    @Test
    void rejectsUnknownExecutableLikeFields() {
        String json = validJson().replace("\n}", ",\n  \"command\": \"kill @e\"\n}");
        assertThrows(JsonParseException.class, () ->
            ArcaneEquipmentDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsResourceIdMismatch() {
        String json = validJson().replace(
            "black_arcana:containment/test_helm",
            "black_arcana:containment/other");
        assertThrows(JsonParseException.class, () ->
            ArcaneEquipmentDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    private static String validJson() {
        return """
            {
              "schemaVersion": 1,
              "id": "black_arcana:containment/test_helm",
              "itemId": "minecraft:golden_helmet",
              "arcaneResistance": 25.0,
              "corruptionResistance": 15.0,
              "strainCapacityBonus": 8.0,
              "strainRecoveryPerTick": 0.25,
              "setId": "black_arcana:test_set",
              "containmentTags": ["black_arcana:ward", "black_arcana:helm"]
            }
            """;
    }
}
