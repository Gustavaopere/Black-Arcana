package dev.gustavopere.blackarcana.content.souls;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SoulDomainSpecificationsTest {
    @Test
    void approvedSoulMechanicsHaveUniqueCompleteSpecifications() {
        var specs = SoulDomainSpecifications.all();
        assertEquals(2, specs.size());
        assertEquals(2, specs.stream().map(spec -> spec.spellId()).distinct().count());
        assertTrue(specs.stream().allMatch(spec -> spec.domain() == ArcanaDomain.SOULS_DEATH));
        SpellImplementationSpecRegistry registry = new SpellImplementationSpecRegistry(8);
        SoulDomainSpecifications.installInto(registry);
        assertEquals(2, registry.snapshot().size());
    }
}
