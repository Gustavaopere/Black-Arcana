package dev.gustavopere.blackarcana.integration.ars;

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

class ArsManaCostProviderTest {
    private static final UUID CASTER = UUID.fromString("99999999-9999-9999-9999-999999999999");

    @Test
    void reserveCommitDebitsExactlyOnce() {
        FakeAccess access = new FakeAccess(80.0D, 100.0D);
        ArsManaCostProvider provider = new ArsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(new ArcanaCost(ArsManaCostProvider.RESOURCE_ID, 22.5D)));
        assertTrue(reservation.reserved());
        assertEquals(57.5D, access.current, 0.000001D);
        reservation.commit();
        reservation.refund();
        assertEquals(57.5D, access.current, 0.000001D);
        assertEquals(1, access.adjustments);
    }

    @Test
    void refundRestoresExactlyOnce() {
        FakeAccess access = new FakeAccess(80.0D, 100.0D);
        ArsManaCostProvider provider = new ArsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(new ArcanaCost(ArsManaCostProvider.RESOURCE_ID, 20.0D)));
        reservation.refund();
        reservation.refund();
        assertEquals(80.0D, access.current, 0.000001D);
        assertEquals(2, access.adjustments);
    }

    @Test
    void percentOfMaxUsesCurrentProviderMaximum() {
        FakeAccess access = new FakeAccess(150.0D, 200.0D);
        ArsManaCostProvider provider = new ArsManaCostProvider(access);

        CostReservation reservation = provider.reserve(request(ArcanaCost.percentOfMax(ArsManaCostProvider.RESOURCE_ID, 0.25D)));
        assertTrue(reservation.reserved());
        assertEquals(100.0D, access.current, 0.000001D);
    }

    @Test
    void insufficientManaFailsWithoutMutation() {
        FakeAccess access = new FakeAccess(10.0D, 100.0D);
        ArsManaCostProvider provider = new ArsManaCostProvider(access);

        ArcanaDecision decision = provider.check(request(new ArcanaCost(ArsManaCostProvider.RESOURCE_ID, 20.0D)));
        assertFalse(decision.allowed());
        assertEquals("insufficient_ars_mana", decision.code());
        assertEquals(0, access.adjustments);
    }

    private static ArcanaCastRequest request(ArcanaCost cost) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:ars_cost_test"),
            "spell.black_arcana.ars_cost_test",
            "black_arcana:textures/spell/ars_cost_test.png",
            cost,
            false);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            spell,
            new ArcanaCastContext(CASTER, 40L, "minecraft:overworld"));
    }

    private static final class FakeAccess implements ArsManaAccess {
        private double current;
        private final double maximum;
        private int adjustments;

        private FakeAccess(double current, double maximum) {
            this.current = current;
            this.maximum = maximum;
        }

        @Override
        public ArsManaSnapshot snapshot(UUID playerId) {
            assertEquals(CASTER, playerId);
            return new ArsManaSnapshot(current, maximum);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, double delta) {
            assertEquals(CASTER, playerId);
            double next = current + delta;
            if (next < 0.0D || next > maximum) {
                return ArcanaDecision.deny("fake_bounds", "out of bounds");
            }
            current = next;
            adjustments++;
            return ArcanaDecision.allow();
        }
    }
}
