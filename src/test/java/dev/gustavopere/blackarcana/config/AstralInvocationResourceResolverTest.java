package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralInvocationResourceResolverTest {
    @AfterEach
    void resetAuthority() {
        AstralInvocationConfigAuthority.reload(List.of());
    }

    @Test
    void absentInvocationFailsClosedWithoutPartialResolution() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        AstralInvocationResourceResolver.Resolution resolution =
                AstralInvocationResourceResolver.resolve(runtime);

        assertEquals("astral_invocation_not_configured", resolution.decision().code());
        assertTrue(resolution.invocation().isEmpty());
        assertTrue(resolution.resourceProvider().isEmpty());
    }

    @Test
    void configuredInvocationWithMissingProviderFailsClosedWithoutPartialResolution() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralInvocationConfigAuthority.reload(List.of(fixtureDefinition("black_arcana:missing_resource")));

        AstralInvocationResourceResolver.Resolution resolution =
                AstralInvocationResourceResolver.resolve(runtime);

        assertEquals("astral_resource_provider_missing", resolution.decision().code());
        assertTrue(resolution.invocation().isEmpty());
        assertTrue(resolution.resourceProvider().isEmpty());
    }

    @Test
    void exactConfiguredResourceResolvesExactRegisteredProvider() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeProvider provider = new FakeProvider("black_arcana:test_resource");
        runtime.resourceCosts().register(provider);
        AstralInvocationConfigAuthority.reload(List.of(fixtureDefinition(provider.resourceId())));

        AstralInvocationResourceResolver.Resolution resolution =
                AstralInvocationResourceResolver.resolve(runtime);

        assertTrue(resolution.decision().allowed());
        assertEquals("ok", resolution.decision().code());
        assertEquals(provider.resourceId(), resolution.invocation().orElseThrow().cost().resourceId());
        assertSame(provider, resolution.resourceProvider().orElseThrow());
    }

    @Test
    void providerResolutionRemainsIsolatedPerServerRuntime() {
        ArcanaServerRuntime configuredRuntime = ArcanaServerRuntime.createDefault();
        ArcanaServerRuntime emptyRuntime = ArcanaServerRuntime.createDefault();
        FakeProvider provider = new FakeProvider("black_arcana:test_resource");
        configuredRuntime.resourceCosts().register(provider);
        AstralInvocationConfigAuthority.reload(List.of(fixtureDefinition(provider.resourceId())));

        assertTrue(AstralInvocationResourceResolver.resolve(configuredRuntime).decision().allowed());
        assertEquals(
                "astral_resource_provider_missing",
                AstralInvocationResourceResolver.resolve(emptyRuntime).decision().code());
    }

    private static AstralInvocationDataDefinition fixtureDefinition(String resourceId) {
        return new AstralInvocationDataDefinition(
                AstralInvocationDataDefinition.CURRENT_SCHEMA_VERSION,
                AstralInvocationDataDefinition.ASTRAL_SEVERANCE_ID,
                ConfigScope.SERVER,
                resourceId,
                7.5D,
                ArcanaCost.Unit.FLAT,
                "black_arcana:test_astral",
                60L,
                true,
                6L,
                40L,
                80,
                12.5D);
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
            return new ArcanaServices.CostReservation() {
                @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                @Override public void commit() { }
                @Override public void refund() { }
            };
        }
    }
}
