package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IronsManaCostProviderTest {
    private static final UUID CASTER = UUID.fromString("44444444-4444-4444-4444-444444444444");

    @Test
    void insufficientManaDeniesWithoutMutation() {
        FakeAccess access = new FakeAccess(20.0F, 100.0F);
        IronsManaCostProvider provider = new IronsManaCostProvider(access);

        ArcanaDecision decision = provider.check(request(new ArcanaCost(IronsManaCostProvider.RESOURCE_ID, 30.0D)));
        assertFalse(decision.allowed());
        assertEquals("insufficient_irons_mana", decision.code());
        assertEquals(20.0F, access.current);
        assertEquals(0, access.adjustments);
    }

    @Test
    void reservationDeductsAndRefundRestoresExactlyOnce() {
        FakeAccess access = new FakeAccess(80.0F, 100.0F);
        IronsManaCostProvider provider = new IronsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(new ArcanaCost(IronsManaCostProvider.RESOURCE_ID, 30.0D)));
        assertTrue(reservation.reserved());
        assertEquals(50.0F, access.current);

        reservation.refund();
        reservation.refund();
        assertEquals(80.0F, access.current);
        assertEquals(2, access.adjustments);
    }

    @Test
    void committedReservationCannotRefundLater() {
        FakeAccess access = new FakeAccess(80.0F, 100.0F);
        IronsManaCostProvider provider = new IronsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(new ArcanaCost(IronsManaCostProvider.RESOURCE_ID, 30.0D)));
        reservation.commit();
        reservation.refund();

        assertEquals(50.0F, access.current);
        assertEquals(1, access.adjustments);
    }

    @Test
    void percentOfMaximumUsesProviderMaximum() {
        FakeAccess access = new FakeAccess(90.0F, 200.0F);
        IronsManaCostProvider provider = new IronsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(ArcanaCost.percentOfMax(IronsManaCostProvider.RESOURCE_ID, 0.25D)));
        assertTrue(reservation.reserved());
        assertEquals(40.0F, access.current);
    }

    @Test
    void wrongResourceFailsClosed() {
        FakeAccess access = new FakeAccess(90.0F, 200.0F);
        IronsManaCostProvider provider = new IronsManaCostProvider(access);

        ArcanaDecision decision = provider.check(request(new ArcanaCost("ars_nouveau:source", 10.0D)));
        assertFalse(decision.allowed());
        assertEquals("irons_mana_resource_mismatch", decision.code());
        assertEquals(0, access.adjustments);
    }

    private static ArcanaCastRequest request(ArcanaCost cost) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:irons_cost_test"),
            "spell.black_arcana.irons_cost_test",
            "black_arcana:textures/spell/irons_cost_test.png",
            cost,
            false);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("55555555-5555-5555-5555-555555555555"),
            spell,
            new ArcanaCastContext(CASTER, 40L, "minecraft:overworld"));
    }

    private static final class FakeAccess implements IronsManaAccess {
        private float current;
        private final float maximum;
        private int adjustments;

        private FakeAccess(float current, float maximum) {
            this.current = current;
            this.maximum = maximum;
        }

        @Override
        public IronsManaSnapshot snapshot(UUID playerId) {
            assertEquals(CASTER, playerId);
            return new IronsManaSnapshot(current, maximum);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, float delta) {
            assertEquals(CASTER, playerId);
            float next = current + delta;
            if (next < 0.0F || next > maximum) {
                return ArcanaDecision.deny("fake_adjustment_rejected", "out of bounds");
            }
            current = next;
            adjustments++;
            return ArcanaDecision.allow();
        }
    }
}
