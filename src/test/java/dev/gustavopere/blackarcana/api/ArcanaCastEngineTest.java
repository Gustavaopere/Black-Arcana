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
        return new ArcanaCastRequest(spell, new ArcanaCastContext(UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 40L, "minecraft:overworld"));
    }

    private static CostReservation grantedReservation(List<String> calls) {
        return new CostReservation() {
            @Override
            public ArcanaDecision decision() {
                return ArcanaDecision.allow();
            }

            @Override
            public void commit() {
                calls.add("cost-commit");
            }

            @Override
            public void refund() {
                calls.add("cost-refund");
            }
        };
    }

    @Test
    void spellIdsAreStrictAndCanonical() {
        assertEquals("black_arcana:test/spell", ArcanaSpellId.parse("black_arcana:test/spell").canonical());
        assertThrows(IllegalArgumentException.class, () -> ArcanaSpellId.parse("Black_Arcana:test"));
        assertThrows(IllegalArgumentException.class, () -> ArcanaSpellId.parse("black_arcana:test:extra"));
        assertThrows(IllegalArgumentException.class, () -> new ArcanaCost("mana", Double.POSITIVE_INFINITY));
    }

    @Test
    void validationStopsAtFirstExpectedDenial() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> { calls.add("progression"); return ArcanaDecision.allow(); },
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { calls.add("cooldown"); return ArcanaDecision.deny("cooldown", "still cooling down"); }
                    public void start(ArcanaCastRequest req) { throw new AssertionError("must not start"); }
                },
                req -> { throw new AssertionError("target must not run"); },
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(ArcanaCastRequest req) { throw new AssertionError("cost must not run"); }
                    public CostReservation reserve(ArcanaCastRequest req) { throw new AssertionError("reserve must not run"); }
                },
                (req, target) -> { throw new AssertionError("world policy must not run"); },
                (req, target) -> { throw new AssertionError("effect must not run"); });

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.DENIED_COOLDOWN, result.status());
        assertEquals(List.of("progression", "cooldown"), calls);
    }

    @Test
    void fakeSpellExecutesWithoutAnyExternalMagicMod() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
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
        assertEquals(List.of("progression", "cooldown-check", "target", "cost-check", "world-policy", "cost-reserve", "effect", "cost-commit", "cooldown-start"), calls);
    }

    @Test
    void effectFailureRefundsReservationAndDoesNotStartCooldown() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(),
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
    void reservationRaceDeniesBeforeEffect() {
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public void start(ArcanaCastRequest req) { throw new AssertionError("must not start"); }
                },
                req -> TargetResolution.resolved("fake-target"),
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public CostReservation reserve(ArcanaCastRequest req) {
                        return new CostReservation() {
                            public ArcanaDecision decision() { return ArcanaDecision.deny("cost_race", "resource changed before reservation"); }
                            public void commit() { throw new AssertionError("must not commit"); }
                            public void refund() { throw new AssertionError("nothing was reserved"); }
                        };
                    }
                },
                (req, target) -> ArcanaDecision.allow(),
                (req, target) -> { throw new AssertionError("effect must not run"); });

        ArcanaCastResult result = engine.execute(request());
        assertEquals(ArcanaCastResult.Status.DENIED_COST, result.status());
        assertEquals("cost_race", result.code());
    }

    @Test
    void unexpectedEffectExceptionStillRefundsReservation() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public void start(ArcanaCastRequest req) { throw new AssertionError("must not start"); }
                },
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
}
