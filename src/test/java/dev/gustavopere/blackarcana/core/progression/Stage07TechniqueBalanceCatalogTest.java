package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.content.blood.BloodDomainSpecifications;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreDomainSpecifications;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSpecifications;
import dev.gustavopere.blackarcana.content.noetic.FamiliarsDivinationSpecifications;
import dev.gustavopere.blackarcana.content.projection.ProjectionDomainSpecifications;
import dev.gustavopere.blackarcana.content.souls.SoulDomainSpecifications;
import dev.gustavopere.blackarcana.content.space.SpaceDomainSpecifications;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import org.junit.jupiter.api.Test;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Stage07TechniqueBalanceCatalogTest {
    @Test
    void everyProductionTechniqueHasExactlyOneExplicitBudget() {
        Set<ArcanaSpellId> productionIds = new LinkedHashSet<>();
        addAll(productionIds, BloodDomainSpecifications.all());
        addAll(productionIds, SoulDomainSpecifications.all());
        addAll(productionIds, ProjectionDomainSpecifications.all());
        addAll(productionIds, SpaceDomainSpecifications.all());
        addAll(productionIds, BlackPyreDomainSpecifications.all());
        addAll(productionIds, ForbiddenDomainSpecifications.all());
        addAll(productionIds, FamiliarsDivinationSpecifications.all());

        assertEquals(26, productionIds.size(), "Stage 07 production inventory changed; budget review must be updated deliberately");
        assertEquals(productionIds, Stage07TechniqueBalanceCatalog.ids());
    }

    @Test
    void everyBudgetStaysInsideItsTierAndCarriesBenchmarkEvidence() {
        Stage07TechniqueBalanceCatalog.snapshot().values().forEach(profile -> {
            assertTrue(profile.assess().withinBudget(), profile.spellId().canonical() + " exceeded its tier budget");
            assertFalse(profile.benchmark().source().isBlank());
            assertFalse(profile.benchmark().version().isBlank());
            assertFalse(profile.benchmark().note().isBlank());
        });
    }

    @Test
    void unknownProductionTechniqueFailsClosedInsteadOfUsingTierDefaults() {
        ArcanaSpellId unknown = ArcanaSpellId.parse("black_arcana:unreviewed_spell");
        assertThrows(IllegalStateException.class, () -> Stage07TechniqueBalanceCatalog.require(unknown));
    }

    private static void addAll(Set<ArcanaSpellId> target, List<SpellImplementationSpec> specs) {
        specs.forEach(spec -> assertTrue(target.add(spec.spellId()), "duplicate Stage 07 production id: " + spec.spellId().canonical()));
    }
}
