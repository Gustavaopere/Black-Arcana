package dev.gustavopere.blackarcana.core.integration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import org.junit.jupiter.api.Test;

class FailClosedProgressionGateTest {
    @Test
    void unavailableProviderNeverInvokesDelegate() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        registry.register(integration(ArcanaIntegrationAvailability.MISSING_MOD));
        AtomicBoolean invoked = new AtomicBoolean();
        FailClosedProgressionGate gate = new FailClosedProgressionGate(
            registry,
            "rpgskilltree",
            ArcanaIntegrationCapability.PROGRESSION_QUERY,
            request -> {
                invoked.set(true);
                return ArcanaDecision.allow();
            });

        ArcanaDecision decision = gate.check(request());
        assertFalse(decision.allowed());
        assertEquals("integration_unavailable", decision.code());
        assertFalse(invoked.get());
    }

    @Test
    void availableProviderDelegatesNormally() {
        ArcanaIntegrationRegistry registry = new ArcanaIntegrationRegistry();
        registry.register(integration(ArcanaIntegrationAvailability.AVAILABLE));
        FailClosedProgressionGate gate = new FailClosedProgressionGate(
            registry,
            "rpgskilltree",
            ArcanaIntegrationCapability.PROGRESSION_QUERY,
            request -> ArcanaDecision.deny("rank_too_low", "Requires intelligence 10"));

        ArcanaDecision decision = gate.check(request());
        assertFalse(decision.allowed());
        assertEquals("rank_too_low", decision.code());
    }

    private static ArcanaIntegration integration(ArcanaIntegrationAvailability availability) {
        return new ArcanaIntegration() {
            @Override public String integrationId() { return "rpgskilltree"; }
            @Override public boolean available() { return availability.usable(); }
            @Override public String implementationVersion() { return "1.0.0-alpha.6-dev"; }
            @Override public ArcanaIntegrationAvailability availability() { return availability; }
            @Override public Set<ArcanaIntegrationCapability> capabilities() {
                return availability.usable()
                    ? Set.of(ArcanaIntegrationCapability.PROGRESSION_QUERY)
                    : Set.of();
            }
        };
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            new ArcanaSpellId("black_arcana:test"),
            "spell.black_arcana.test",
            "black_arcana:test",
            ArcanaCost.none(),
            false);
        return new ArcanaCastRequest(
            spell,
            new ArcanaCastContext(UUID.randomUUID(), 10L, "minecraft:overworld"));
    }
}
