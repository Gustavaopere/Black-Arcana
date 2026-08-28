package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCasterMode;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaPaymentPolicy;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CostPolicyTest {
    private static ArcanaCastRequest request(ArcanaCasterMode mode) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:test"),
                "spell.black_arcana.test",
                "black_arcana:test",
                new ArcanaCost("black_arcana:mana", 5.0), false);
        return new ArcanaCastRequest(spell, new ArcanaCastContext(
                UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 20L, "minecraft:overworld", mode));
    }

    @Test
    void percentOfMaxCostIsBounded() {
        ArcanaCost cost = ArcanaCost.percentOfMax("black_arcana:health", 0.25);
        assertEquals(ArcanaCost.Unit.PERCENT_OF_MAX, cost.unit());
        assertEquals(0.25, cost.amount());
        assertThrows(IllegalArgumentException.class, () -> ArcanaCost.percentOfMax("black_arcana:health", 1.01));
    }

    @Test
    void creativeBypassDoesNotTouchDelegateButSurvivalPays() {
        AtomicInteger calls = new AtomicInteger();
        CostProvider delegate = new CostProvider() {
            public ArcanaDecision check(ArcanaCastRequest request) { calls.incrementAndGet(); return ArcanaDecision.allow(); }
            public CostReservation reserve(ArcanaCastRequest request) {
                calls.incrementAndGet();
                return new CostReservation() {
                    public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    public void commit() { }
                    public void refund() { }
                };
            }
        };
        PolicyAwareCostProvider provider = new PolicyAwareCostProvider(ArcanaPaymentPolicy.BYPASS_CREATIVE, delegate);

        assertTrue(provider.check(request(ArcanaCasterMode.CREATIVE)).allowed());
        provider.reserve(request(ArcanaCasterMode.CREATIVE)).commit();
        assertEquals(0, calls.get());

        assertTrue(provider.check(request(ArcanaCasterMode.SURVIVAL)).allowed());
        provider.reserve(request(ArcanaCasterMode.SURVIVAL)).commit();
        assertEquals(2, calls.get());
    }
}
