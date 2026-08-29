package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RitualRegistryTest {
    private static final ArcanaRitualId ID = ArcanaRitualId.parse("black_arcana:registry_test");
    private static final RitualDefinition DEFINITION = new RitualDefinition(ID, 20L, 40L);
    private static final RitualContext CONTEXT = new RitualContext(
            UUID.fromString("11111111-1111-1111-1111-111111111111"),
            List.of(),
            new RitualAnchor("minecraft:overworld", 42L));

    @Test
    void definitionRegistryIsBoundedAndRejectsDuplicates() {
        RitualDefinitionRegistry registry = new RitualDefinitionRegistry(1);
        registry.register(DEFINITION);

        assertEquals(DEFINITION, registry.resolve(ID).orElseThrow());
        assertThrows(IllegalStateException.class, () -> registry.register(DEFINITION));
        assertThrows(IllegalStateException.class, () -> registry.register(
                new RitualDefinition(ArcanaRitualId.parse("black_arcana:second"), 0L, 1L)));
        assertEquals(List.of(DEFINITION), registry.snapshot());
    }

    @Test
    void missingBindingFailsClosedInsteadOfMakingRitualFree() {
        RitualBindingRegistry bindings = new RitualBindingRegistry(4);

        ArcanaDecision requirement = bindings.requirements().check(DEFINITION, CONTEXT, 100L);
        ArcanaDecision componentCheck = bindings.components().check(DEFINITION, CONTEXT, 100L);
        RitualComponentReservation reservation = bindings.components().reserve(DEFINITION, CONTEXT, 100L);
        ArcanaDecision outcome = bindings.outcomes().execute(DEFINITION, CONTEXT, 140L);

        assertEquals("ritual_binding_missing", requirement.code());
        assertEquals("ritual_binding_missing", componentCheck.code());
        assertEquals("ritual_binding_missing", reservation.decision().code());
        assertEquals("ritual_binding_missing", outcome.code());
    }

    @Test
    void explicitBindingRoutesAllThreePhases() {
        RitualBindingRegistry bindings = new RitualBindingRegistry(4);
        AtomicInteger requirementCalls = new AtomicInteger();
        AtomicInteger componentCommits = new AtomicInteger();
        AtomicInteger outcomes = new AtomicInteger();

        bindings.register(
                ID,
                (definition, context, now) -> {
                    requirementCalls.incrementAndGet();
                    return ArcanaDecision.allow();
                },
                new RitualComponentProvider() {
                    @Override
                    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
                        return RitualComponentReservation.reserved(componentCommits::incrementAndGet, () -> { });
                    }
                },
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });

        RitualEngine engine = new RitualEngine(
                new RitualSessionRegistry(4),
                new RitualActivationGuard(16, 1_200L),
                bindings.requirements(),
                bindings.components(),
                bindings.outcomes());
        RitualActivationId activation = RitualActivationId.parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");

        assertEquals(RitualResult.Status.STARTED, engine.start(DEFINITION, activation, CONTEXT, 100L).status());
        engine.tick(120L, 4);
        engine.tick(140L, 4);

        assertEquals(1, requirementCalls.get());
        assertEquals(1, componentCommits.get());
        assertEquals(1, outcomes.get());
        assertTrue(bindings.contains(ID));
    }
}
