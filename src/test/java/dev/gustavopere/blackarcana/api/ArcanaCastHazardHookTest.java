package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaServices.CastHazardGate;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.HazardPreparation;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcanaCastHazardHookTest {
    @Test
    void hazardPreflightRunsBeforeReservationAndActivationBeforeEffect() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(calls, (request, target) -> new HazardPreparation() {
            @Override public ArcanaDecision decision() { calls.add("hazard-preflight"); return ArcanaDecision.allow(); }
            @Override public ArcanaDecision activate() { calls.add("hazard-activate"); return ArcanaDecision.allow(); }
            @Override public void commit() { calls.add("hazard-commit"); }
            @Override public void cancel() { calls.add("hazard-cancel"); }
        }, ArcanaServices.EffectResult.ok());

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.SUCCESS, result.status());
        assertEquals(List.of(
            "cost-check", "world-policy", "hazard-preflight", "cost-reserve",
            "hazard-activate", "effect", "cost-commit", "cooldown-start", "hazard-commit"), calls);
    }

    @Test
    void hazardPreflightDenialStopsBeforeResourceReservation() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(calls, (request, target) -> new HazardPreparation() {
            @Override public ArcanaDecision decision() { calls.add("hazard-preflight"); return ArcanaDecision.deny("hazard_gate", "insufficient resistance"); }
            @Override public ArcanaDecision activate() { throw new AssertionError("denied preflight must not activate"); }
            @Override public void commit() { throw new AssertionError("denied preflight must not commit"); }
            @Override public void cancel() { calls.add("hazard-cancel"); }
        }, ArcanaServices.EffectResult.ok());

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.DENIED_HAZARD, result.status());
        assertEquals(List.of("cost-check", "world-policy", "hazard-preflight", "hazard-cancel"), calls);
    }

    @Test
    void activationFailureRefundsReservedCostAndCancelsHazard() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(calls, (request, target) -> new HazardPreparation() {
            @Override public ArcanaDecision decision() { calls.add("hazard-preflight"); return ArcanaDecision.allow(); }
            @Override public ArcanaDecision activate() { calls.add("hazard-activate"); return ArcanaDecision.deny("hazard_capacity", "runtime full"); }
            @Override public void commit() { throw new AssertionError("failed activation must not commit"); }
            @Override public void cancel() { calls.add("hazard-cancel"); }
        }, ArcanaServices.EffectResult.ok());

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.DENIED_HAZARD, result.status());
        assertEquals(List.of(
            "cost-check", "world-policy", "hazard-preflight", "cost-reserve",
            "hazard-activate", "hazard-cancel", "cost-refund"), calls);
    }

    @Test
    void failedEffectCancelsHazardAndRefundsCost() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(calls, (request, target) -> new HazardPreparation() {
            @Override public ArcanaDecision decision() { calls.add("hazard-preflight"); return ArcanaDecision.allow(); }
            @Override public ArcanaDecision activate() { calls.add("hazard-activate"); return ArcanaDecision.allow(); }
            @Override public void commit() { throw new AssertionError("failed effect must not commit hazard"); }
            @Override public void cancel() { calls.add("hazard-cancel"); }
        }, ArcanaServices.EffectResult.failed("synthetic"));

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.EFFECT_FAILED, result.status());
        assertEquals(List.of(
            "cost-check", "world-policy", "hazard-preflight", "cost-reserve",
            "hazard-activate", "effect", "hazard-cancel", "cost-refund"), calls);
    }

    private static ArcanaCastEngine engine(
        List<String> calls,
        CastHazardGate hazardGate,
        ArcanaServices.EffectResult effectResult
    ) {
        return new ArcanaCastEngine(
            request -> ArcanaDecision.allow(),
            request -> ArcanaDecision.allow(),
            request -> ArcanaDecision.allow(),
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
                @Override public void start(ArcanaCastRequest request) { calls.add("cooldown-start"); }
            },
            request -> TargetResolution.resolved("target"),
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest request) { calls.add("cost-check"); return ArcanaDecision.allow(); }
                @Override public CostReservation reserve(ArcanaCastRequest request) {
                    calls.add("cost-reserve");
                    return new CostReservation() {
                        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                        @Override public void commit() { calls.add("cost-commit"); }
                        @Override public void refund() { calls.add("cost-refund"); }
                    };
                }
            },
            (request, target) -> { calls.add("world-policy"); return ArcanaDecision.allow(); },
            (request, target) -> { calls.add("effect"); return effectResult; },
            ArcanaServices.CastSuccessObserver.noop(),
            hazardGate);
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:hazard_hook_probe"),
            "spell.black_arcana.hazard_hook_probe",
            "black_arcana:textures/spell/hazard_hook_probe.png",
            new ArcanaCost("black_arcana:test", 1.0D),
            true);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("70000000-0000-0000-0000-000000000001"),
            spell,
            new ArcanaCastContext(
                UUID.fromString("70000000-0000-0000-0000-000000000002"),
                100L,
                "minecraft:overworld"));
    }
}
