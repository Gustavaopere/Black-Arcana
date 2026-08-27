package dev.gustavopere.blackarcana.core.registry;

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
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaSpellRegistryTest {
    private static ArcanaSpellDefinition spell(double cost) {
        return new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:test_spell"),
                "spell.black_arcana.test_spell",
                "black_arcana:textures/spell/test_spell.png",
                new ArcanaCost("black_arcana:test", cost), false);
    }

    private static ArcanaCastRequest request(ArcanaSpellDefinition spell) {
        return new ArcanaCastRequest(
                ArcanaCastId.random(), spell,
                new ArcanaCastContext(UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 20L, "minecraft:overworld"));
    }

    @Test
    void canonicalDefinitionIsAcceptedButSpoofedDefinitionIsRejected() {
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        ArcanaSpellDefinition canonical = spell(5.0);
        registry.replaceAll(List.of(canonical));

        assertTrue(registry.check(request(canonical)).allowed());
        var denied = registry.check(request(spell(0.0)));
        assertFalse(denied.allowed());
        assertEquals("spell_definition_mismatch", denied.code());
    }

    @Test
    void duplicateReloadFailsAtomicallyAndKeepsPreviousSnapshot() {
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        ArcanaSpellDefinition canonical = spell(5.0);
        registry.replaceAll(List.of(canonical));

        assertThrows(IllegalArgumentException.class, () -> registry.replaceAll(List.of(spell(1.0), spell(2.0))));
        assertEquals(canonical, registry.resolve(canonical.id()).orElseThrow());
        assertEquals(1, registry.snapshot().size());
    }
}
