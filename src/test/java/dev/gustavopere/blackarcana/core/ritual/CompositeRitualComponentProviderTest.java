package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class CompositeRitualComponentProviderTest {
    private static final RitualDefinition DEFINITION = new RitualDefinition(
            ArcanaRitualId.parse("black_arcana:composite_test"), 0L, 20L);
    private static final RitualContext CONTEXT = new RitualContext(
            UUID.fromString("11111111-1111-1111-1111-111111111111"),
            List.of(),
            new RitualAnchor("minecraft:overworld", 42L));

    @Test
    void laterReservationFailureRefundsEarlierReservationsInReverse() {
        AtomicInteger firstReserved = new AtomicInteger();
        AtomicInteger firstRefunded = new AtomicInteger();
        RitualComponentProvider first = provider(
                ArcanaDecision.allow(),
                () -> {
                    firstReserved.incrementAndGet();
                    return RitualComponentReservation.reserved(() -> { }, firstRefunded::incrementAndGet);
                });
        RitualComponentProvider denied = provider(
                ArcanaDecision.allow(),
                () -> RitualComponentReservation.denied("missing_item", "second component unavailable"));

        CompositeRitualComponentProvider composite = new CompositeRitualComponentProvider(List.of(first, denied));
        RitualComponentReservation reservation = composite.reserve(DEFINITION, CONTEXT, 100L);

        assertFalse(reservation.decision().allowed());
        assertEquals("missing_item", reservation.decision().code());
        assertEquals(1, firstReserved.get());
        assertEquals(1, firstRefunded.get());
    }

    private static RitualComponentProvider provider(
            ArcanaDecision check,
            java.util.function.Supplier<RitualComponentReservation> reservation
    ) {
        return new RitualComponentProvider() {
            @Override public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
                return check;
            }
            @Override public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
                return reservation.get();
            }
        };
    }
}
