package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;
import dev.gustavopere.blackarcana.integration.ars.ArsManaAccess;
import dev.gustavopere.blackarcana.integration.ars.ArsManaCostProvider;
import dev.gustavopere.blackarcana.integration.ars.ArsManaSnapshot;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralResourceAuthorityWiringTest {
    @Test
    void arsManaProviderExposesItsCanonicalResourceIdentity() {
        ResourceCostProvider provider = new ArsManaCostProvider(new ArsManaAccess() {
            @Override public ArsManaSnapshot snapshot(UUID playerId) {
                return new ArsManaSnapshot(100.0D, 100.0D);
            }

            @Override public ArcanaDecision adjust(UUID playerId, double delta) {
                return ArcanaDecision.allow();
            }
        });

        assertEquals(ArsManaCostProvider.RESOURCE_ID, provider.resourceId());
        assertInstanceOf(ArsManaCostProvider.class, provider);
    }

    @Test
    void astralAuthoritiesAcceptGenericNamedResourceProvider() {
        ResourceCostProvider provider = new ResourceCostProvider() {
            @Override public String resourceId() { return "black_arcana:test_resource"; }
            @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
            @Override public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
                return new ArcanaServices.CostReservation() {
                    @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    @Override public void commit() { }
                    @Override public void refund() { }
                };
            }
        };

        AstralSeveranceCastBinding.Authorities authorities = new AstralSeveranceCastBinding.Authorities(
            provider,
            request -> ArcanaDecision.allow(),
            request -> ArcanaDecision.allow(),
            ArcanaServices.CastSuccessObserver.noop());

        assertNotNull(authorities.resourceAuthority());
        assertEquals("black_arcana:test_resource", authorities.resourceAuthority().resourceId());
    }

    @Test
    void arsBootstrapRegistersProviderNativeManaAuthorityWithoutInstallingAstral() throws IOException {
        String source = Files.readString(repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsServerIntegrationBootstrap.java"));

        assertTrue(source.contains(
            "runtime.resourceCosts().register(new ArsManaCostProvider(bridge.manaAccess()));"));
        assertTrue(!source.contains("AstralSeveranceCastBinding.install("),
            "provider registration must not choose Astral's production resource/profile");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);
        return Path.of("").toAbsolutePath();
    }
}
