package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaServerRuntimeHazardGateTest {
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:runtime_hazard_gate");
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");

    @Test
    void runtimeOwnsHazardProviderRegistries() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        assertNotNull(runtime.arcaneResistanceProviders());
        assertNotNull(runtime.corruptionResistanceProviders());
        assertNotNull(runtime.arcaneEquipmentProfiles());
    }

    @Test
    void gateInstalledAfterEngineWrapsExistingEngine() {
        ArcanaServerRuntime runtime = runtimeWithSpell();
        runtime.installEngine(SPELL_ID, engine());
        AtomicInteger preflights = new AtomicInteger();

        runtime.installHazardGate(countingGate(preflights));
        ArcanaCastResult.Status status = status(runtime, "11111111-1111-1111-1111-111111111111");

        assertEquals(ArcanaCastResult.Status.SUCCESS, status);
        assertEquals(1, preflights.get());
    }

    @Test
    void gateInstalledBeforeEngineWrapsFutureEngine() {
        ArcanaServerRuntime runtime = runtimeWithSpell();
        AtomicInteger preflights = new AtomicInteger();
        runtime.installHazardGate(countingGate(preflights));

        runtime.installEngine(SPELL_ID, engine());
        ArcanaCastResult.Status status = status(runtime, "22222222-2222-2222-2222-222222222222");

        assertEquals(ArcanaCastResult.Status.SUCCESS, status);
        assertEquals(1, preflights.get());
    }

    private static ArcanaServerRuntime runtimeWithSpell() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.spells().replaceAll(List.of(spell()));
        return runtime;
    }

    private static ArcanaSpellDefinition spell() {
        return new ArcanaSpellDefinition(
                SPELL_ID,
                "spell.black_arcana.runtime_hazard_gate",
                "black_arcana:textures/spell/runtime_hazard_gate.png",
                new ArcanaCost("black_arcana:test_resource", 1.0D),
                true);
    }

    private static ArcanaCastEngine engine() {
        return new ArcanaCastEngine(
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    @Override public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) { return ArcanaDecision.allow(); }
                    @Override public void start(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) { }
                },
                request -> ArcanaServices.TargetResolution.resolved("target"),
                new ArcanaServices.CostProvider() {
                    @Override public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) { return ArcanaDecision.allow(); }
                    @Override public ArcanaServices.CostReservation reserve(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) {
                        return new ArcanaServices.CostReservation() {
                            @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                            @Override public void commit() { }
                            @Override public void refund() { }
                        };
                    }
                },
                (request, target) -> ArcanaDecision.allow(),
                (request, target) -> ArcanaServices.EffectResult.ok());
    }

    private static ArcanaServices.CastHazardGate countingGate(AtomicInteger preflights) {
        return (request, target) -> {
            preflights.incrementAndGet();
            return ArcanaServices.HazardPreparation.noop();
        };
    }

    private static ArcanaCastResult.Status status(ArcanaServerRuntime runtime, String castId) {
        var result = runtime.handle(
                new ArcanaCastContext(CASTER, 100L, "minecraft:overworld"),
                new CastIntentPayload(
                        ArcanaProtocol.VERSION,
                        castId,
                        SPELL_ID.canonical(),
                        0,
                        "target"));
        return ArcanaCastResult.Status.valueOf(result.status());
    }
}
