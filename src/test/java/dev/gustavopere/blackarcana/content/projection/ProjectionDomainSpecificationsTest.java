package dev.gustavopere.blackarcana.content.projection;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProjectionDomainSpecificationsTest {
    @Test
    void approvedProjectionMechanicsHaveCompleteSpecifications() {
        var specs = ProjectionDomainSpecifications.all();
        assertEquals(5, specs.size());
        assertEquals(5, specs.stream().map(spec -> spec.spellId()).distinct().count());
        assertTrue(specs.stream().allMatch(spec -> spec.domain() == ArcanaDomain.PROJECTION_ARSENAL));
        SpellImplementationSpecRegistry registry = new SpellImplementationSpecRegistry(8);
        ProjectionDomainSpecifications.installInto(registry);
        assertEquals(5, registry.snapshot().size());
    }
}
