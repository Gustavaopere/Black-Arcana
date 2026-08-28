package dev.gustavopere.blackarcana.api;

import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcanaCastEngineTest {
    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:test_spell"),
                "spell.black_arcana.test_spell",
                "black_arcana:textures/spell/test_spell.png",
                new ArcanaCost("black_arcana:test_resource", 4.0),
                true);
        return new ArcanaCastRequest(
                ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
                spell,
                new ArcanaCastContext(UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 40L, "minecraft:overworld"));
    }

    private static CostReservation grantedReservation(List<String> calls) {
        return new CostReservation() {
            public ArcanaDecision decision() { return ArcanaDecision.allow(); }
            public void commit() { calls.add("cost-commit"); }
            public void refund() { calls.add("cost-refund"); }
        };
    }

    @Test
    void identityDenialStopsBeforeReplay() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> { calls.add("identity"); return ArcanaDecision.deny("identity", "not in loadout"); },
                req -> { throw new AssertionError("replay must not run"); },
                req -> { throw new AssertionError("progression must not run"); },
                noCooldown(),
                req -> TargetResolution.resolved("target"),
                noCost(),
                (req, target) -> ArcanaDecision.allow(),
                (req, target) -> ArcanaServices.EffectResult.ok());

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.DENIED_IDENTITY, result.status());
        assertEquals(List.of("identity"), calls);
    }

    @Test
    void validationStopsAtFirstExpectedDenial() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> { calls.add("identity"); return ArcanaDecision.allow(); },
                req -> { calls.add("replay"); return ArcanaDecision.allow(); },
                req -> { calls.add("progression"); return ArcanaDecision.allow(); },
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cooldown"); return ArcanaDecision.deny("cooldown", "still cooling down"); }
                    public void start(ArcanaCastRequest req) { throw new AssertionError("must not start"); }
                },
                req -> { throw new AssertionError("target must not run"); },
                noCost(),
                (req, target) -> { throw new AssertionError("world policy must not run"); },
                (req, target) -> { throw new AssertionError("effect must not run"); });

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.DENIED_COOLDOWN, result.status());
        assertEquals(List.of("identity", "replay", "progression", "cooldown"), calls);
    }

    @Test
    void fakeSpellExecutesWithoutAnyExternalMagicMod() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> { calls.add("identity"); return ArcanaDecision.allow(); },
                req -> { calls.add("replay"); return ArcanaDecision.allow(); },
                req -> { calls.add("progression"); return ArcanaDecision.allow(); },
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cooldown-check"); return ArcanaDecision.allow(); }
                    public void start(ArcanaCastRequest req) { calls.add("cooldown-start"); }
                },
                req -> { calls.add("target"); return TargetResolution.resolved("fake-target"); },
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cost-check"); return ArcanaDecision.allow(); }
                    public CostReservation reserve(ArcanaCastRequest req) { calls.add("cost-reserve"); return grantedReservation(calls); }
                },
                (req, target) -> { calls.add("world-policy"); return ArcanaDecision.allow(); },
                (req, target) -> { calls.add("effect"); return ArcanaServices.EffectResult.ok(); });

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.SUCCESS, result.status());
        assertFalse(request().spell().translationKey().isBlank());
        assertEquals(List.of("identity", "replay", "progression", "cooldown-check", "target", "cost-check", "world-policy", "cost-reserve", "effect", "cost-commit", "cooldown-start"), calls);
    }

    @Test
    void effectFailureRefundsReservationAndDoesNotStartCooldown() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(), req -> ArcanaDecision.allow(), req -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public void start(ArcanaCastRequest req) { throw new AssertionError("failed effect must not start cooldown"); }
                },
                req -> TargetResolution.resolved("fake-target"),
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public CostReservation reserve(ArcanaCastRequest req) { calls.add("cost-reserve"); return grantedReservation(calls); }
                },
                (req, target) -> ArcanaDecision.allow(),
                (req, target) -> { calls.add("effect"); return ArcanaServices.EffectResult.failed("rejected by runtime"); });

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.EFFECT_FAILED, result.status());
        assertEquals(List.of("cost-reserve", "effect", "cost-refund"), calls);
    }

    @Test
    void unexpectedEffectExceptionStillRefundsReservation() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(), req -> ArcanaDecision.allow(), req -> ArcanaDecision.allow(), noCooldown(),
                req -> TargetResolution.resolved("fake-target"),
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public CostReservation reserve(ArcanaCastRequest req) { return grantedReservation(calls); }
                },
                (req, target) -> ArcanaDecision.allow(),
                (req, target) -> { throw new IllegalStateException("broken invariant"); });

        assertThrows(IllegalStateException.class, () -> engine.execute(request()));
        assertEquals(List.of("cost-refund"), calls);
    }

    private static ArcanaServices.CooldownService noCooldown() {
        return new ArcanaServices.CooldownService() {
            public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
            public void start(ArcanaCastRequest req) { }
        };
    }

    private static ArcanaServices.CostProvider noCost() {
        return new ArcanaServices.CostProvider() {
            public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
            public CostReservation reserve(ArcanaCastRequest req) { return grantedReservation(new ArrayList<>()); }
        };
    }
}
