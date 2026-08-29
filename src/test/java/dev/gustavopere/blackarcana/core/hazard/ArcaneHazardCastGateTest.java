package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.config.ArcaneDangerDataDefinition;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneHazardCastGateTest {
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:test_hazard_gate");
    private static final UUID CASTER_ID = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");

    @Test
    void runtimeProfileRetainsAuthoritativePreflightFields() {
        ArcaneDangerProfile profile = definition().toRuntimeProfile();

        assertEquals(25.0D, profile.minimumArcaneResistance());
        assertEquals(50.0D, profile.recommendedArcaneResistance());
        assertTrue(profile.emergencyProtectionAllowed());
    }

    @Test
    void belowMinimumResistanceFailsClosedBeforeActivation() {
        ArcaneDangerProfileRegistry profiles = profiles(definition().toRuntimeProfile());
        ArcaneResistanceProviderRegistry resistance = ArcaneResistanceProviderRegistry.canonical(4);
        AtomicInteger activations = new AtomicInteger();
        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(profiles, resistance, new ArcaneHazardCastGate.HazardSessionActivator() {
            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                    ArcaneHazardSnapshot snapshot,
                    ArcaneResistanceSnapshot resistanceSnapshot,
                    ArcaneBacklashPolicy policy
            ) {
                activations.incrementAndGet();
                return ArcaneHazardRuntime.ActivationResult.success(true);
            }

            @Override
            public boolean close(ArcanaCastId castId) {
                return false;
            }
        });

        var preparation = gate.preflight(request(), TargetResolution.resolved("target"));

        assertFalse(preparation.decision().allowed());
        assertEquals("hazard_minimum_resistance", preparation.decision().code());
        assertEquals(0, activations.get());
    }

    @Test
    void sufficientResistanceIsSnapshottedAndActivationUsesSameRootCast() {
        ArcaneDangerProfileRegistry profiles = profiles(definition().toRuntimeProfile());
        ArcaneResistanceProviderRegistry resistance = ArcaneResistanceProviderRegistry.canonical(4);
        resistance.register(new dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider() {
            @Override
            public String providerId() {
                return "test:fixed";
            }

            @Override
            public java.util.List<ArcaneResistanceContribution> contributions(
                    dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery query
            ) {
                return java.util.List.of(new ArcaneResistanceContribution(
                        "test:amulet", ArcaneResistanceSourceCategory.CURIO, 40.0D));
            }
        });

        AtomicReference<ArcaneHazardSnapshot> activatedSnapshot = new AtomicReference<>();
        AtomicReference<ArcaneResistanceSnapshot> activatedResistance = new AtomicReference<>();
        AtomicInteger closes = new AtomicInteger();
        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(profiles, resistance, new ArcaneHazardCastGate.HazardSessionActivator() {
            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                    ArcaneHazardSnapshot snapshot,
                    ArcaneResistanceSnapshot resistanceSnapshot,
                    ArcaneBacklashPolicy policy
            ) {
                activatedSnapshot.set(snapshot);
                activatedResistance.set(resistanceSnapshot);
                return ArcaneHazardRuntime.ActivationResult.success(true);
            }

            @Override
            public boolean close(ArcanaCastId castId) {
                closes.incrementAndGet();
                return true;
            }
        });

        ArcanaCastRequest request = request();
        var preparation = gate.preflight(request, TargetResolution.resolved("target"));
        assertTrue(preparation.decision().allowed());

        ArcanaDecision activation = preparation.activate();
        assertTrue(activation.allowed());
        assertEquals(request.castId(), activatedSnapshot.get().rootCastId());
        assertEquals(SPELL_ID, activatedSnapshot.get().spellId());
        assertEquals(40.0D, activatedResistance.get().effectiveResistance());

        preparation.cancel();
        assertEquals(1, closes.get());
    }

    private static ArcaneDangerProfileRegistry profiles(ArcaneDangerProfile profile) {
        ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
        registry.replaceAll(Map.of(SPELL_ID, profile));
        return registry;
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
                SPELL_ID,
                "spell.black_arcana.test_hazard_gate",
                "black_arcana:textures/spell/test_hazard_gate.png",
                new ArcanaCost("black_arcana:test_resource", 1.0D),
                true);
        return new ArcanaCastRequest(
                ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
                spell,
                new ArcanaCastContext(CASTER_ID, 100L, "minecraft:overworld"));
    }

    private static ArcaneDangerDataDefinition definition() {
        return new ArcaneDangerDataDefinition(
                1,
                1,
                SPELL_ID.canonical(),
                ArcaneDangerTier.DANGEROUS,
                1.0D,
                2.0D,
                3.0D,
                100L,
                16,
                25.0D,
                50.0D,
                true);
    }
}
