package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.content.blood.BloodPriceHealthAccess;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IronsBloodPriceCostProviderTest {
    private static final UUID CASTER = UUID.fromString("77777777-7777-7777-7777-777777777777");

    @Test
    void percentOfMaximumIsResolvedBeforeBloodSubstitutionAndRefundsAtomically() throws Exception {
        FakeManaAccess mana = new FakeManaAccess(90.0F, 200.0F);
        FakeHealthAccess health = new FakeHealthAccess(30.0D);

        Class<?> type = Class.forName(
            "dev.gustavopere.blackarcana.integration.irons.IronsBloodPriceCostProvider");
        var constructor = type.getConstructor(
            IronsManaAccess.class,
            BloodPriceHealthAccess.class,
            Predicate.class,
            double.class,
            double.class,
            double.class);

        @SuppressWarnings("unchecked")
        Predicate<ArcanaCastRequest> enabled = request -> true;
        CostProvider provider = (CostProvider) constructor.newInstance(
            mana,
            health,
            enabled,
            0.40D,
            0.50D,
            1.0D);

        ArcanaCastRequest request = request(ArcanaCost.percentOfMax(IronsManaCostProvider.RESOURCE_ID, 0.25D));
        assertTrue(provider.check(request).allowed());

        CostReservation reservation = provider.reserve(request);
        assertTrue(reservation.reserved());
        assertEquals(60.0F, mana.current, 1.0E-6F,
            "25% of max 200 is 50 mana; 40% substitution leaves 30 mana to reserve");
        assertEquals(20.0D, health.current, 1.0E-9,
            "40% of resolved 50 mana is 20 units, converted at 0.5 health per mana");

        reservation.refund();
        assertEquals(90.0F, mana.current, 1.0E-6F);
        assertEquals(30.0D, health.current, 1.0E-9);
    }

    private static ArcanaCastRequest request(ArcanaCost cost) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:irons_blood_price_test"),
            "spell.black_arcana.irons_blood_price_test",
            "black_arcana:textures/spell/irons_blood_price_test.png",
            cost,
            false);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("88888888-8888-8888-8888-888888888888"),
            spell,
            new ArcanaCastContext(CASTER, 80L, "minecraft:overworld"));
    }

    private static final class FakeManaAccess implements IronsManaAccess {
        private float current;
        private final float maximum;

        private FakeManaAccess(float current, float maximum) {
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
                return ArcanaDecision.deny("fake_mana_adjustment_rejected", "out of bounds");
            }
            current = next;
            return ArcanaDecision.allow();
        }
    }

    private static final class FakeHealthAccess implements BloodPriceHealthAccess {
        private double current;

        private FakeHealthAccess(double current) {
            this.current = current;
        }

        @Override
        public double currentHealth(UUID casterId) {
            assertEquals(CASTER, casterId);
            return current;
        }

        @Override
        public CostReservation reserve(UUID casterId, double amount, double minimumRemainingHealth) {
            assertEquals(CASTER, casterId);
            double before = current;
            if (before - amount < minimumRemainingHealth) {
                return denied("insufficient_blood_price_health");
            }
            current = before - amount;
            return new CostReservation() {
                private boolean terminal;

                @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                @Override public void commit() { terminal = true; }
                @Override public void refund() {
                    if (terminal) return;
                    terminal = true;
                    current += amount;
                }
            };
        }
    }

    private static CostReservation denied(String code) {
        return new CostReservation() {
            private final ArcanaDecision decision = ArcanaDecision.deny(code, code);
            @Override public ArcanaDecision decision() { return decision; }
            @Override public void commit() { throw new IllegalStateException("denied"); }
            @Override public void refund() { }
        };
    }
}
