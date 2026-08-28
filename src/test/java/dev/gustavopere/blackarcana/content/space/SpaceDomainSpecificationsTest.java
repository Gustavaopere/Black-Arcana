package dev.gustavopere.blackarcana.content.space;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SpaceDomainSpecificationsTest {
    @Test
    void approvedLiminalMechanicsHaveCompleteSpecifications() {
        var specs = SpaceDomainSpecifications.all();
        assertEquals(5, specs.size());
        assertEquals(5, specs.stream().map(spec -> spec.spellId()).distinct().count());
        assertTrue(specs.stream().allMatch(spec -> spec.domain() == ArcanaDomain.SPACE_DISPLACEMENT));
        SpellImplementationSpecRegistry registry = new SpellImplementationSpecRegistry(8);
        SpaceDomainSpecifications.installInto(registry);
        assertEquals(5, registry.snapshot().size());
    }
}
