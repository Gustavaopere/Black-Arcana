package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryQuery;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcaneStrainRecoveryProviderRegistryTest {
    @Test
    void providersAreDeterministicBoundedAndFailureIsIsolated() {
        ArcaneStrainRecoveryProviderRegistry registry = new ArcaneStrainRecoveryProviderRegistry(4);
        registry.register(new TestProvider("z_buff", List.of(new ArcaneStrainRecoveryContribution("buff:rest", 0.20D)), false));
        registry.register(new TestProvider("a_ritual", List.of(new ArcaneStrainRecoveryContribution("ritual:purge", 0.30D)), false));
        registry.register(new TestProvider("broken", List.of(), true));

        var snapshot = registry.snapshot(new ArcaneStrainRecoveryQuery(UUID.randomUUID(), 100L, 50.0D), 0.05D);
        assertEquals(0.50D, snapshot.bonusUnitsPerTick(), 1.0E-9D);
        assertEquals(0.55D, snapshot.totalUnitsPerTick(), 1.0E-9D);
        assertEquals("a_ritual", snapshot.contributions().getFirst().providerId());
        assertEquals(1, snapshot.diagnostics().size());
    }

    private record TestProvider(
        String providerId,
        List<ArcaneStrainRecoveryContribution> values,
        boolean fail
    ) implements dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryProvider {
        @Override
        public List<ArcaneStrainRecoveryContribution> contributions(ArcaneStrainRecoveryQuery query) {
            if (fail) throw new IllegalStateException("synthetic provider failure");
            return values;
        }
    }
}
