package dev.gustavopere.blackarcana.core.registry;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.config.SpellDataDefinition;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SpellDataCatalogTest {
    private static SpellDataDefinition definition(String id, String translationKey) {
        return new SpellDataDefinition(
                SpellDataDefinition.CURRENT_SCHEMA_VERSION,
                id,
                translationKey,
                "black_arcana:textures/spell/test.png");
    }

    @Test
    void malformedReloadFailsAtomically() {
        SpellDataCatalog catalog = new SpellDataCatalog();
        SpellDataDefinition valid = definition("black_arcana:test", "spell.black_arcana.test");
        catalog.replaceAll(List.of(valid));

        assertThrows(IllegalArgumentException.class, () -> catalog.replaceAll(List.of(
                definition("black_arcana:new", "spell.black_arcana.new"),
                new SpellDataDefinition(99, "Bad Id", "", ""))));

        assertEquals(valid, catalog.resolve(ArcanaSpellId.parse("black_arcana:test")).orElseThrow());
        assertEquals(1, catalog.snapshot().size());
    }

    @Test
    void presentationPayloadIsDeterministicallySorted() {
        SpellDataCatalog catalog = new SpellDataCatalog();
        catalog.replaceAll(List.of(
                definition("black_arcana:zeta", "spell.black_arcana.zeta"),
                definition("black_arcana:alpha", "spell.black_arcana.alpha")));

        assertEquals(
                List.of("black_arcana:alpha", "black_arcana:zeta"),
                catalog.presentationPayload().entries().stream().map(entry -> entry.spellId()).toList());
    }
}
