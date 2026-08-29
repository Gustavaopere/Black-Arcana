package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentSetBonusDataReloadListenerTest {
    private static final ResourceLocation ID =
        ResourceLocation.fromNamespaceAndPath("black_arcana", "sets/veil_2pc");

    @Test
    void parsesStrictDeclarativeSetThreshold() {
        var definition = ArcaneEquipmentSetBonusDataReloadListener.parseDefinition(
            ID, JsonParser.parseString(validJson()));

        assertEquals("black_arcana:sets/veil_2pc", definition.id());
        assertEquals("black_arcana:veil", definition.bonus().setId());
        assertEquals(2, definition.bonus().requiredPieces());
        assertEquals(7.0D, definition.bonus().arcaneResistance(), 0.0D);
        assertEquals(4.0D, definition.bonus().corruptionResistance(), 0.0D);
        assertEquals(3.0D, definition.bonus().strainCapacityBonus(), 0.0D);
        assertEquals(0.2D, definition.bonus().strainRecoveryPerTick(), 0.0D);
        assertTrue(definition.bonus().containmentTags().contains("black_arcana:ward"));
    }

    @Test
    void rejectsExecutableLikeOrUnknownFields() {
        String json = validJson().replace("\n}", ",\n  \"command\": \"kill @e\"\n}");
        assertThrows(JsonParseException.class, () ->
            ArcaneEquipmentSetBonusDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsResourceIdMismatchAndImpossibleThreshold() {
        String mismatch = validJson().replace("black_arcana:sets/veil_2pc", "black_arcana:sets/other");
        assertThrows(JsonParseException.class, () ->
            ArcaneEquipmentSetBonusDataReloadListener.parseDefinition(ID, JsonParser.parseString(mismatch)));

        String impossible = validJson().replace("\"requiredPieces\": 2", "\"requiredPieces\": 33");
        assertThrows(JsonParseException.class, () ->
            ArcaneEquipmentSetBonusDataReloadListener.parseDefinition(ID, JsonParser.parseString(impossible)));
    }

    private static String validJson() {
        return """
            {
              "schemaVersion": 1,
              "id": "black_arcana:sets/veil_2pc",
              "setId": "black_arcana:veil",
              "requiredPieces": 2,
              "arcaneResistance": 7.0,
              "corruptionResistance": 4.0,
              "strainCapacityBonus": 3.0,
              "strainRecoveryPerTick": 0.2,
              "containmentTags": ["black_arcana:ward", "black_arcana:set/veil"]
            }
            """;
    }
}
