package dev.gustavopere.blackarcana.content.blood;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Proxy;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Predicate;
import java.util.function.ToDoubleFunction;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BloodPriceCostProviderContractTest {
    @Test
    void reservesReducedResourceAndRealHealthAsOneRefundableTransaction() throws Exception {
        AtomicReference<Double> resource = new AtomicReference<>(10.0D);
        AtomicReference<Double> health = new AtomicReference<>(20.0D);
        CostProvider delegate = new InMemoryResourceProvider(resource);

        Class<?> healthAccessType = Class.forName(
            "dev.gustavopere.blackarcana.content.blood.BloodPriceHealthAccess");
        Object healthAccess = Proxy.newProxyInstance(
            getClass().getClassLoader(),
            new Class<?>[] { healthAccessType },
            (proxy, method, args) -> switch (method.getName()) {
                case "currentHealth" -> health.get();
                case "reserve" -> reserveHealth(
                    health,
                    (double) args[1],
                    (double) args[2]);
                case "toString" -> "test-health-access";
                case "hashCode" -> System.identityHashCode(proxy);
                case "equals" -> proxy == args[0];
                default -> throw new UnsupportedOperationException(method.getName());
            });

        Class<?> providerType = Class.forName(
            "dev.gustavopere.blackarcana.content.blood.BloodPriceCostProvider");
        var constructor = providerType.getConstructor(
            CostProvider.class,
            healthAccessType,
            Predicate.class,
            ToDoubleFunction.class,
            double.class,
            double.class,
            double.class);

        @SuppressWarnings("unchecked")
        Predicate<ArcanaCastRequest> enabled = request -> true;
        ToDoubleFunction<ArcanaCastRequest> resolvedCost = request -> request.spell().cost().amount();
        CostProvider provider = (CostProvider) constructor.newInstance(
            delegate,
            healthAccess,
            enabled,
            resolvedCost,
            0.40D,
            1.0D,
            1.0D);

        ArcanaCastRequest request = request(10.0D);
        assertTrue(provider.check(request).allowed());

        CostReservation reservation = provider.reserve(request);
        assertTrue(reservation.reserved());
        assertEquals(4.0D, resource.get(), 1.0E-9);
        assertEquals(16.0D, health.get(), 1.0E-9);

        reservation.refund();
        assertEquals(10.0D, resource.get(), 1.0E-9);
        assertEquals(20.0D, health.get(), 1.0E-9);
    }

    private static ArcanaCastRequest request(double cost) {
        UUID caster = UUID.randomUUID();
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:blood_price_contract_test"),
            "spell.black_arcana.blood_price_contract_test",
            "black_arcana:textures/gui/spell_icons/blood_price_contract_test.png",
            new ArcanaCost("test:resource", cost),
            false);
        return new ArcanaCastRequest(spell, new ArcanaCastContext(caster, 1L, "minecraft:overworld"));
    }

    private static CostReservation reserveHealth(
        AtomicReference<Double> health,
        double amount,
        double minimumRemainingHealth
    ) {
        double before = health.get();
        if (before - amount < minimumRemainingHealth) {
            return denied("insufficient_blood_price_health");
        }
        health.set(before - amount);
        return new CostReservation() {
            private boolean terminal;

            @Override
            public ArcanaDecision decision() {
                return ArcanaDecision.allow();
            }

            @Override
            public void commit() {
                terminal = true;
            }

            @Override
            public void refund() {
                if (terminal) return;
                terminal = true;
                health.set(health.get() + amount);
            }
        };
    }

    private static CostReservation denied(String code) {
        return new CostReservation() {
            private final ArcanaDecision decision = ArcanaDecision.deny(code, code);
            @Override public ArcanaDecision decision() { return decision; }
            @Override public void commit() { throw new IllegalStateException("denied"); }
            @Override public void refund() { }
        };
    }

    private static final class InMemoryResourceProvider implements CostProvider {
        private final AtomicReference<Double> resource;

        private InMemoryResourceProvider(AtomicReference<Double> resource) {
            this.resource = resource;
        }

        @Override
        public ArcanaDecision check(ArcanaCastRequest request) {
            double amount = request.spell().cost().amount();
            return resource.get() >= amount
                ? ArcanaDecision.allow()
                : ArcanaDecision.deny("insufficient_resource", "insufficient_resource");
        }

        @Override
        public CostReservation reserve(ArcanaCastRequest request) {
            ArcanaDecision decision = check(request);
            if (!decision.allowed()) return denied(decision.code());
            double amount = request.spell().cost().amount();
            resource.set(resource.get() - amount);
            return new CostReservation() {
                private boolean terminal;

                @Override
                public ArcanaDecision decision() {
                    return ArcanaDecision.allow();
                }

                @Override
                public void commit() {
                    terminal = true;
                }

                @Override
                public void refund() {
                    if (terminal) return;
                    terminal = true;
                    resource.set(resource.get() + amount);
                }
            };
        }
    }
}
