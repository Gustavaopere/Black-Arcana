package dev.gustavopere.blackarcana.core.domain;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SpellImplementationSpecRegistryTest {
    @Test
    void completeSpecRegistersAndDuplicateFails() {
        SpellImplementationSpec spec = new SpellImplementationSpec(
            ArcanaSpellId.parse("black_arcana:sympathetic_wound"),
            ArcanaDomain.BLOOD_CURSES,
            "Mirror a bounded fraction of direct wounds through an occult link.",
            "Malum/Eidolon + Black Arcana core",
            "active cast after occult unlock",
            "one server-resolved living target",
            "health/spirit",
            200L,
            "mirror=min(damage*fraction,eventCap,lifetimeRemaining)",
            "T3 Sanguine",
            WorldEffectMode.OFF,
            "separate player/boss multipliers and entity protection admission",
            "fraction/event/lifetime caps, duration, player/boss policy",
            "docs/design/candidate-specifications.md#sympathetic-wound");

        SpellImplementationSpecRegistry registry = new SpellImplementationSpecRegistry(2);
        registry.register(spec);
        assertEquals(spec, registry.find(spec.spellId()).orElseThrow());
        assertThrows(IllegalStateException.class, () -> registry.register(spec));
    }

    @Test
    void incompleteSpecIsRejectedAtConstruction() {
        assertThrows(IllegalArgumentException.class, () -> new SpellImplementationSpec(
            ArcanaSpellId.parse("black_arcana:bad"), ArcanaDomain.BLOOD_CURSES,
            "", "host", "invoke", "target", "cost", 0L, "scale", "gate",
            WorldEffectMode.OFF, "policy", "config", "provenance"));
    }
}
