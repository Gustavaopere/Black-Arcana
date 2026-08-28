package dev.gustavopere.blackarcana.core.integration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import java.util.Set;
import org.junit.jupiter.api.Test;

class ArcanaIntegrationRegistryTest {
    @Test
    void availableCapabilityIsAllowedAndVisibleInSnapshot() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        registry.register(integration(
            "rpgskilltree",
            ArcanaIntegrationAvailability.AVAILABLE,
            Set.of(ArcanaIntegrationCapability.PROGRESSION_QUERY),
            "1.0.0"));

        assertTrue(registry.requireCapability(
            "rpgskilltree", ArcanaIntegrationCapability.PROGRESSION_QUERY).allowed());
        assertEquals(1, registry.snapshot().size());
        assertEquals(ArcanaIntegrationAvailability.AVAILABLE, registry.snapshot().getFirst().availability());
    }

    @Test
    void missingOrIncompatibleProvidersFailClosed() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        registry.register(integration(
            "rpgskilltree",
            ArcanaIntegrationAvailability.API_INCOMPATIBLE,
            Set.of(),
            "unknown"));

        var incompatible = registry.requireCapability(
            "rpgskilltree", ArcanaIntegrationCapability.PROGRESSION_QUERY);
        assertFalse(incompatible.allowed());
        assertEquals("integration_unavailable", incompatible.code());

        var absent = registry.requireCapability(
            "ars_nouveau", ArcanaIntegrationCapability.SOURCE_RESOURCE);
        assertFalse(absent.allowed());
        assertEquals("integration_missing", absent.code());
    }

    @Test
    void capabilityMustBeExplicitlyAdvertised() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        registry.register(integration(
            "irons_spellbooks",
            ArcanaIntegrationAvailability.AVAILABLE,
            Set.of(ArcanaIntegrationCapability.SPELL_HOST),
            "3.16.3"));

        var decision = registry.requireCapability(
            "irons_spellbooks", ArcanaIntegrationCapability.MANA_RESOURCE);
        assertFalse(decision.allowed());
        assertEquals("integration_capability_missing", decision.code());
    }

    @Test
    void duplicateAndInconsistentDescriptorsAreRejected() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        ArcanaIntegration first = integration(
            "malum",
            ArcanaIntegrationAvailability.AVAILABLE,
            Set.of(ArcanaIntegrationCapability.SOUL_RESOURCE),
            "1.8.2");
        registry.register(first);
        assertThrows(IllegalArgumentException.class, () -> registry.register(first));

        ArcanaIntegration inconsistent = new ArcanaIntegration() {
            @Override public String integrationId() { return "broken"; }
            @Override public boolean available() { return true; }
            @Override public String implementationVersion() { return "1"; }
            @Override public ArcanaIntegrationAvailability availability() {
                return ArcanaIntegrationAvailability.API_INCOMPATIBLE;
            }
        };
        assertThrows(IllegalArgumentException.class, () -> new ArcanaIntegrationRegistry().register(inconsistent));
    }

    private static ArcanaIntegration integration(
        String id,
        ArcanaIntegrationAvailability availability,
        Set<ArcanaIntegrationCapability> capabilities,
        String version
    ) {
        return new ArcanaIntegration() {
            @Override public String integrationId() { return id; }
            @Override public boolean available() { return availability.usable(); }
            @Override public String implementationVersion() { return version; }
            @Override public ArcanaIntegrationAvailability availability() { return availability; }
            @Override public Set<ArcanaIntegrationCapability> capabilities() { return capabilities; }
            @Override public String diagnostic() { return availability.usable() ? "" : "provider unavailable"; }
        };
    }
}
