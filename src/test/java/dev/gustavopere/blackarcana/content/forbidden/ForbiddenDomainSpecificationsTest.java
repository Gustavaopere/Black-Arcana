package dev.gustavopere.blackarcana.content.forbidden;

import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ForbiddenDomainSpecificationsTest {
    @Test void innerDominionUsesBoundedLocalizedSessionContract() {
        var spec = ForbiddenDomainSpecifications.all().getFirst();
        assertEquals(ArcanaDomain.FORBIDDEN_DOMAINS, spec.domain());
        assertEquals(2_400L, spec.cooldownTicks());
    }
}
