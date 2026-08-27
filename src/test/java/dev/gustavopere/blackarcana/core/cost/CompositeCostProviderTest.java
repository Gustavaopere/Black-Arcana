package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CompositeCostProviderTest {
    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
                ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
                new ArcanaSpellDefinition(
                        ArcanaSpellId.parse("black_arcana:test_spell"),
                        "spell.black_arcana.test_spell",
                        "black_arcana:textures/spell/test_spell.png",
                        new ArcanaCost("black_arcana:test", 1.0),
                        false),
                new ArcanaCastContext(UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"), 40L, "minecraft:overworld"));
    }

    @Test
    void reserveFailureRefundsEarlierReservationsInReverseOrder() {
        List<String> calls = new ArrayList<>();
        CompositeCostProvider provider = new CompositeCostProvider(List.of(
                provider("a", calls, true),
                provider("b", calls, true),
                provider("c", calls, false)));

        CostReservation reservation = provider.reserve(request());
        assertFalse(reservation.reserved());
        assertEquals("c_denied", reservation.decision().code());
        assertEquals(List.of("a-reserve", "b-reserve", "c-reserve", "b-refund", "a-refund"), calls);
    }

    @Test
    void successfulCompositeCommitsEveryReservationInProviderOrder() {
        List<String> calls = new ArrayList<>();
        CompositeCostProvider provider = new CompositeCostProvider(List.of(
                provider("a", calls, true), provider("b", calls, true)));

        CostReservation reservation = provider.reserve(request());
        assertTrue(reservation.reserved());
        reservation.commit();
        assertEquals(List.of("a-reserve", "b-reserve", "a-commit", "b-commit"), calls);
    }

    @Test
    void explicitRefundRunsInReverseOrder() {
        List<String> calls = new ArrayList<>();
        CompositeCostProvider provider = new CompositeCostProvider(List.of(
                provider("a", calls, true), provider("b", calls, true)));

        CostReservation reservation = provider.reserve(request());
        reservation.refund();
        assertEquals(List.of("a-reserve", "b-reserve", "b-refund", "a-refund"), calls);
    }

    private static CostProvider provider(String name, List<String> calls, boolean grants) {
        return new CostProvider() {
            @Override
            public ArcanaDecision check(ArcanaCastRequest request) {
                return grants ? ArcanaDecision.allow() : ArcanaDecision.deny(name + "_denied", "unavailable");
            }

            @Override
            public CostReservation reserve(ArcanaCastRequest request) {
                calls.add(name + "-reserve");
                if (!grants) {
                    return new CostReservation() {
                        public ArcanaDecision decision() { return ArcanaDecision.deny(name + "_denied", "unavailable"); }
                        public void commit() { throw new AssertionError("denied reservation cannot commit"); }
                        public void refund() { }
                    };
                }
                return new CostReservation() {
                    public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    public void commit() { calls.add(name + "-commit"); }
                    public void refund() { calls.add(name + "-refund"); }
                };
            }
        };
    }
}
