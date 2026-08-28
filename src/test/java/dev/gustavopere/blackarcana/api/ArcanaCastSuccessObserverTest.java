package dev.gustavopere.blackarcana.api;

import static org.junit.jupiter.api.Assertions.assertEquals;

import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class ArcanaCastSuccessObserverTest {
    @Test
    void observerRunsOnlyAfterCommitAndCooldown() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(
            req -> ArcanaDecision.allow(),
            calls,
            (request, target, effect) -> calls.add("observer"));

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.SUCCESS, result.status());
        assertEquals(List.of("effect", "commit", "cooldown", "observer"), calls);
    }

    @Test
    void deniedCastNeverNotifiesObserver() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(
            req -> ArcanaDecision.deny("locked", "locked"),
            calls,
            (request, target, effect) -> calls.add("observer"));

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.DENIED_PROGRESSION, result.status());
        assertEquals(List.of(), calls);
    }

    @Test
    void observerFailureCannotRefundOrInvalidateCommittedCast() {
        List<String> calls = new ArrayList<>();
        ArcanaCastEngine engine = engine(
            req -> ArcanaDecision.allow(),
            calls,
            (request, target, effect) -> {
                calls.add("observer");
                throw new IllegalStateException("optional adapter failure");
            });

        ArcanaCastResult result = engine.execute(request());

        assertEquals(ArcanaCastResult.Status.SUCCESS, result.status());
        assertEquals(List.of("effect", "commit", "cooldown", "observer"), calls);
    }

    private static ArcanaCastEngine engine(
        ArcanaServices.ProgressionGate progression,
        List<String> calls,
        ArcanaServices.CastSuccessObserver observer
    ) {
        return new ArcanaCastEngine(
            req -> ArcanaDecision.allow(),
            req -> ArcanaDecision.allow(),
            progression,
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
                @Override public void start(ArcanaCastRequest request) { calls.add("cooldown"); }
            },
            req -> TargetResolution.resolved("target"),
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
                @Override public CostReservation reserve(ArcanaCastRequest request) {
                    return new CostReservation() {
                        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                        @Override public void commit() { calls.add("commit"); }
                        @Override public void refund() { calls.add("refund"); }
                    };
                }
            },
            (req, target) -> ArcanaDecision.allow(),
            (req, target) -> {
                calls.add("effect");
                return ArcanaServices.EffectResult.ok();
            },
            observer);
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:observer_test"),
            "spell.black_arcana.observer_test",
            "black_arcana:textures/spell/observer_test.png",
            ArcanaCost.none(),
            false);
        return new ArcanaCastRequest(
            spell,
            new ArcanaCastContext(UUID.randomUUID(), 20L, "minecraft:overworld"));
    }
}
