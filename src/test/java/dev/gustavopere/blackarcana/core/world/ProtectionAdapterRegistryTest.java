package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProtectionAdapterRegistryTest {
    private static final ProtectionQuery QUERY = new ProtectionQuery(
        UUID.fromString("11111111-1111-1111-1111-111111111111"),
        "minecraft:overworld",
        "entity:target",
        EntityInteractionType.CONTROL);

    @Test
    void noAdaptersMeansCoreDoesNotInventClaimRestrictions() {
        assertTrue(new ProtectionAdapterRegistry(4).authorize(QUERY).allowed());
    }

    @Test
    void providerDenialStopsAuthorization() {
        var registry = new ProtectionAdapterRegistry(4);
        registry.register("claims", query -> ArcanaDecision.deny("claim_protected", "protected"));

        assertEquals("claim_protected", registry.authorize(QUERY).code());
    }

    @Test
    void brokenProtectionAdapterFailsClosed() {
        var registry = new ProtectionAdapterRegistry(4);
        registry.register("claims", query -> { throw new IllegalStateException("provider unavailable"); });

        var decision = registry.authorize(QUERY);
        assertFalse(decision.allowed());
        assertEquals("protection_adapter_failed", decision.code());
    }
}
