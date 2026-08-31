package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaCastGatePreflightTest {
    @Test
    void previewStopsAtProgressionWithoutInvokingMutatingOrContextualStages() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
            req -> { calls.add("identity"); return ArcanaDecision.allow(); },
            req -> { throw new AssertionError("preview must not claim replay state"); },
            req -> { calls.add("progression"); return ArcanaDecision.deny("progression_locked", "progression requirement not met"); },
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { throw new AssertionError("must stop before cooldown"); }
                @Override public void start(ArcanaCastRequest req) { throw new AssertionError("preview must not start cooldown"); }
            },
            req -> { throw new AssertionError("preview must not resolve targets"); },
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { throw new AssertionError("must stop before cost"); }
                @Override public CostReservation reserve(ArcanaCastRequest req) { throw new AssertionError("preview must not reserve cost"); }
            },
            (req, target) -> { throw new AssertionError("preview must not authorize world effects"); },
            (req, target) -> { throw new AssertionError("preview must not execute effects"); },
            ArcanaServices.CastSuccessObserver.noop(),
            (req, target) -> { throw new AssertionError("preview must not prepare hazard state"); });

        ArcanaGatePreflight result = engine.previewReadOnlyGates(request());

        assertFalse(result.allowed());
        assertEquals(ArcanaGatePreflight.Gate.PROGRESSION, result.gate());
        assertEquals("progression_locked", result.decision().code());
        assertEquals(List.of("identity", "progression"), calls);
    }

    @Test
    void previewChecksOnlyPredictableReadOnlyGatesWhenClear() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
            req -> { calls.add("identity"); return ArcanaDecision.allow(); },
            req -> { throw new AssertionError("preview must not claim replay state"); },
            req -> { calls.add("progression"); return ArcanaDecision.allow(); },
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cooldown"); return ArcanaDecision.allow(); }
                @Override public void start(ArcanaCastRequest req) { throw new AssertionError("preview must not start cooldown"); }
            },
            req -> { throw new AssertionError("preview must not resolve targets"); },
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cost"); return ArcanaDecision.allow(); }
                @Override public CostReservation reserve(ArcanaCastRequest req) { throw new AssertionError("preview must not reserve cost"); }
            },
            (req, target) -> { throw new AssertionError("preview must not authorize world effects"); },
            (req, target) -> { throw new AssertionError("preview must not execute effects"); },
            ArcanaServices.CastSuccessObserver.noop(),
            (req, target) -> { throw new AssertionError("preview must not prepare hazard state"); });

        ArcanaGatePreflight result = engine.previewReadOnlyGates(request());

        assertTrue(result.allowed());
        assertEquals(ArcanaGatePreflight.Gate.CLEAR, result.gate());
        assertEquals(List.of("identity", "progression", "cooldown", "cost"), calls);
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:preflight_test"),
            "spell.black_arcana.preflight_test",
            "black_arcana:textures/spell/preflight_test.png",
            new ArcanaCost("black_arcana:test_resource", 4.0D),
            true);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
            spell,
            new ArcanaCastContext(UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 40L, "minecraft:overworld"));
    }
}
