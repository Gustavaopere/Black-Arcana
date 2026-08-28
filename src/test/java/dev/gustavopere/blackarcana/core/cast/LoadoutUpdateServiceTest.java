package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoadoutUpdateServiceTest {
    private static final UUID CASTER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static final ArcanaSpellId FIRST = ArcanaSpellId.parse("black_arcana:first");
    private static final ArcanaSpellId SECOND = ArcanaSpellId.parse("black_arcana:second");

    @Test
    void acceptedUpdateBecomesServerOwnedLoadout() {
        var spells = registry();
        var loadouts = new LoadoutRegistry();
        var service = new LoadoutUpdateService(spells, loadouts, id -> true);

        var result = service.apply(CASTER, List.of(FIRST, SECOND));

        assertTrue(result.decision().allowed());
        assertEquals(List.of(FIRST, SECOND), loadouts.getLoadout(CASTER));
    }

    @Test
    void unknownSpellRejectsWholeUpdateWithoutOverwritingPriorState() {
        var loadouts = new LoadoutRegistry();
        loadouts.setLoadout(CASTER, List.of(FIRST));
        var service = new LoadoutUpdateService(registry(), loadouts, id -> true);

        var result = service.apply(CASTER, List.of(FIRST, ArcanaSpellId.parse("black_arcana:missing")));

        assertFalse(result.decision().allowed());
        assertEquals("loadout_unknown_spell", result.decision().code());
        assertEquals(List.of(FIRST), result.loadout());
        assertEquals(List.of(FIRST), loadouts.getLoadout(CASTER));
    }

    @Test
    void unavailableSpellRejectsWholeUpdate() {
        var loadouts = new LoadoutRegistry();
        var service = new LoadoutUpdateService(registry(), loadouts, id -> !id.equals(SECOND));

        var result = service.apply(CASTER, List.of(FIRST, SECOND));

        assertFalse(result.decision().allowed());
        assertEquals("loadout_spell_unavailable", result.decision().code());
        assertTrue(loadouts.getLoadout(CASTER).isEmpty());
    }

    @Test
    void duplicateSpellRejectsWholeUpdate() {
        var loadouts = new LoadoutRegistry();
        var service = new LoadoutUpdateService(registry(), loadouts, id -> true);

        var result = service.apply(CASTER, List.of(FIRST, FIRST));

        assertFalse(result.decision().allowed());
        assertEquals("loadout_duplicate_spell", result.decision().code());
        assertTrue(loadouts.getLoadout(CASTER).isEmpty());
    }

    private static ArcanaSpellRegistry registry() {
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        registry.replaceAll(List.of(definition(FIRST), definition(SECOND)));
        return registry;
    }

    private static ArcanaSpellDefinition definition(ArcanaSpellId id) {
        return new ArcanaSpellDefinition(
                id,
                "spell." + id.namespace() + "." + id.path(),
                id.canonical(),
                ArcanaCost.none(),
                false);
    }
}
