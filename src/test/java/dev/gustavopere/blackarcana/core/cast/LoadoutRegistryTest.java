package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoadoutRegistryTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");

    private static ArcanaSpellDefinition spell(String path) {
        return new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:" + path),
                "spell.black_arcana." + path,
                "black_arcana:" + path,
                new ArcanaCost("black_arcana:test", 1.0), false);
    }

    private static ArcanaCastRequest request(ArcanaSpellDefinition spell, int slot) {
        return new ArcanaCastRequest(
                ArcanaCastId.random(), spell,
                new ArcanaCastContext(CASTER, 20L, "minecraft:overworld"), slot);
    }

    @Test
    void serverOwnedSlotMustMatchRequestedSpell() {
        LoadoutRegistry registry = new LoadoutRegistry();
        ArcanaSpellDefinition alpha = spell("alpha");
        ArcanaSpellDefinition beta = spell("beta");
        registry.setLoadout(CASTER, List.of(alpha.id(), beta.id()));

        assertTrue(registry.check(request(beta, 1)).allowed());
        var mismatch = registry.check(request(alpha, 1));
        assertFalse(mismatch.allowed());
        assertEquals("loadout_spell_mismatch", mismatch.code());
    }

    @Test
    void missingSlotIsDenied() {
        LoadoutRegistry registry = new LoadoutRegistry();
        registry.setLoadout(CASTER, List.of(spell("alpha").id()));
        assertEquals("loadout_slot_unavailable", registry.check(request(spell("alpha"), 2)).code());
    }
}
