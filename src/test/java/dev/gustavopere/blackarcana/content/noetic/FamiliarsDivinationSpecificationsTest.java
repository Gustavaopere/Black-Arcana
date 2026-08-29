package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FamiliarsDivinationSpecificationsTest {
    @Test void allNoeticCandidatesAreExplicitlySpecified() {
        var specs = FamiliarsDivinationSpecifications.all();
        assertEquals(7, specs.size());
        assertTrue(specs.stream().allMatch(spec -> spec.domain() == ArcanaDomain.FAMILIARS_DIVINATION));
    }
}
