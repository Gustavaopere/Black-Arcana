package dev.gustavopere.blackarcana.content.blood;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BloodDomainSpecificationsTest {
    @Test
    void allApprovedBloodMechanicsHaveCompleteUniqueSpecifications() {
        var specs = BloodDomainSpecifications.all();
        assertEquals(5, specs.size());
        assertEquals(5, specs.stream().map(spec -> spec.spellId()).distinct().count());
        assertTrue(specs.stream().allMatch(spec -> spec.domain() == ArcanaDomain.BLOOD_CURSES));
        assertTrue(specs.stream().allMatch(spec -> !spec.provenance().isBlank()));

        SpellImplementationSpecRegistry registry = new SpellImplementationSpecRegistry(8);
        BloodDomainSpecifications.installInto(registry);
        assertEquals(5, registry.snapshot().size());
    }
}
