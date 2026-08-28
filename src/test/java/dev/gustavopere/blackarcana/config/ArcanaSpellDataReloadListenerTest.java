package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcanaSpellDataReloadListenerTest {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath("black_arcana", "test_spell");

    @Test
    void parsesStrictPresentationOnlyDefinition() {
        var definition = ArcanaSpellDataReloadListener.parseDefinition(ID, JsonParser.parseString("""
                {
                  "schemaVersion": 1,
                  "id": "black_arcana:test_spell",
                  "translationKey": "spell.black_arcana.test_spell",
                  "iconId": "black_arcana:textures/spell/test_spell.png"
                }
                """));

        assertEquals("black_arcana:test_spell", definition.id());
        assertEquals("spell.black_arcana.test_spell", definition.translationKey());
    }

    @Test
    void rejectsUnknownGameplayLikeFields() {
        assertThrows(JsonParseException.class, () -> ArcanaSpellDataReloadListener.parseDefinition(ID, JsonParser.parseString("""
                {
                  "schemaVersion": 1,
                  "id": "black_arcana:test_spell",
                  "translationKey": "spell.black_arcana.test_spell",
                  "iconId": "black_arcana:test_spell",
                  "damage": 9999
                }
                """)));
    }

    @Test
    void rejectsDefinitionWhoseIdDoesNotMatchResourcePath() {
        assertThrows(JsonParseException.class, () -> ArcanaSpellDataReloadListener.parseDefinition(ID, JsonParser.parseString("""
                {
                  "schemaVersion": 1,
                  "id": "black_arcana:other_spell",
                  "translationKey": "spell.black_arcana.test_spell",
                  "iconId": "black_arcana:test_spell"
                }
                """)));
    }

    @Test
    void rejectsUnsupportedSchemaBeforePublication() {
        assertThrows(JsonParseException.class, () -> ArcanaSpellDataReloadListener.parseDefinition(ID, JsonParser.parseString("""
                {
                  "schemaVersion": 2,
                  "id": "black_arcana:test_spell",
                  "translationKey": "spell.black_arcana.test_spell",
                  "iconId": "black_arcana:test_spell"
                }
                """)));
    }
}
