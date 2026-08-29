package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneDangerDataReloadListenerTest {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath("black_arcana", "test_dangerous");

    @Test
    void parsesBoundedDeclarativeProfile() {
        var definition = ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(validJson()));
        assertEquals("black_arcana:test_dangerous", definition.id());
        assertEquals(ArcaneDangerTier.DANGEROUS, definition.tier());
        assertEquals(1.0D, definition.backlashMultiplier());
        assertEquals(25.0D, definition.minimumArcaneResistance());
    }

    @Test
    void rejectsUnknownExecutableLikeFields() {
        String json = validJson().replace("\n}", ",\n  \"command\": \"kill @e\"\n}");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsResourceIdMismatch() {
        String json = validJson().replace("black_arcana:test_dangerous", "black_arcana:other");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsImpossibleResistanceHints() {
        String json = validJson().replace("\"minimumArcaneResistance\": 25.0", "\"minimumArcaneResistance\": 75.0")
            .replace("\"recommendedArcaneResistance\": 50.0", "\"recommendedArcaneResistance\": 50.0");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsDangerousProfileThatConfiguresAwayBacklash() {
        String json = validJson().replace("\"backlashMultiplier\": 1.0", "\"backlashMultiplier\": 0.0");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    private static String validJson() {
        return """
            {
              "schemaVersion": 1,
              "profileVersion": 1,
              "id": "black_arcana:test_dangerous",
              "tier": "DANGEROUS",
              "backlashMultiplier": 1.0,
              "corruptionCoefficient": 2.0,
              "strainCoefficient": 3.0,
              "damageLeaseTicks": 100,
              "maxDamageInstances": 16,
              "minimumArcaneResistance": 25.0,
              "recommendedArcaneResistance": 50.0,
              "emergencyProtectionAllowed": true
            }
            """;
    }
}
