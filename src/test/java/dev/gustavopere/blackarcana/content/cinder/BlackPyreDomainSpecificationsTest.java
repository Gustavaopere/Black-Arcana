package dev.gustavopere.blackarcana.content.cinder;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackPyreDomainSpecificationsTest {
    @Test void blackPyreIsTemporaryByDefaultAndInCinderDomain() {
        var spec = BlackPyreDomainSpecifications.all().getFirst();
        assertEquals(ArcanaDomain.BLACK_FLAME, spec.domain());
        assertEquals(WorldEffectMode.TEMPORARY, spec.worldEffectMode());
    }
}
