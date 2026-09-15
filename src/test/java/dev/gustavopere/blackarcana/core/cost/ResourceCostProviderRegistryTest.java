package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ResourceCostProviderRegistryTest {
    @Test
    void registryResolvesOnlyExplicitNamedProvider() {
        ResourceCostProviderRegistry registry = new ResourceCostProviderRegistry(2);
        FakeProvider provider = new FakeProvider("ars_nouveau:mana");

        registry.register(provider);

        assertSame(provider, registry.resolve("ars_nouveau:mana").orElseThrow());
        assertTrue(registry.resolve("irons_spellbooks:mana").isEmpty());
        assertEquals(1, registry.size());
    }

    @Test
    void duplicateResourceIdFailsClosedWithoutReplacingAuthority() {
        ResourceCostProviderRegistry registry = new ResourceCostProviderRegistry(2);
        FakeProvider original = new FakeProvider("ars_nouveau:mana");
        registry.register(original);

        assertThrows(IllegalArgumentException.class,
            () -> registry.register(new FakeProvider("ars_nouveau:mana")));
        assertSame(original, registry.resolve("ars_nouveau:mana").orElseThrow());
        assertEquals(1, registry.size());
    }

    @Test
    void capacityAndInvalidIdsFailClosed() {
        ResourceCostProviderRegistry registry = new ResourceCostProviderRegistry(1);
        registry.register(new FakeProvider("ars_nouveau:mana"));

        assertThrows(IllegalStateException.class,
            () -> registry.register(new FakeProvider("irons_spellbooks:mana")));
        assertThrows(IllegalArgumentException.class,
            () -> new FakeProvider("not namespaced"));
    }

    @Test
    void defaultServerRuntimeOwnsIsolatedEmptyResourceRegistry() {
        ArcanaServerRuntime first = ArcanaServerRuntime.createDefault();
        ArcanaServerRuntime second = ArcanaServerRuntime.createDefault();
        FakeProvider provider = new FakeProvider("ars_nouveau:mana");

        first.resourceCosts().register(provider);

        assertSame(provider, first.resourceCosts().resolve("ars_nouveau:mana").orElseThrow());
        assertTrue(second.resourceCosts().resolve("ars_nouveau:mana").isEmpty());
    }

    private static final class FakeProvider implements ResourceCostProvider {
        private final String resourceId;

        private FakeProvider(String resourceId) {
            this.resourceId = ResourceCostProvider.requireResourceId(resourceId);
        }

        @Override
        public String resourceId() {
            return resourceId;
        }

        @Override
        public ArcanaDecision check(ArcanaCastRequest request) {
            return ArcanaDecision.allow();
        }

        @Override
        public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
            return Reservation.INSTANCE;
        }
    }

    private enum Reservation implements ArcanaServices.CostReservation {
        INSTANCE;
        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { }
        @Override public void refund() { }
    }
}
