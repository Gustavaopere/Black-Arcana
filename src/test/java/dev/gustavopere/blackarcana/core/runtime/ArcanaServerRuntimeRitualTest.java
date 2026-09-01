package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualActivationId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentProvider;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentReservation;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualDefinition;
import dev.gustavopere.blackarcana.core.ritual.RitualResult;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaServerRuntimeRitualTest {
    @Test
    void runtimeOwnsAndTicksOneBoundedRitualEngine() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaRitualId id = ArcanaRitualId.parse("black_arcana:runtime_rite");
        RitualDefinition definition = new RitualDefinition(id, 20L, 40L);
        AtomicInteger commits = new AtomicInteger();
        AtomicInteger outcomes = new AtomicInteger();

        runtime.ritualDefinitions().register(definition);
        runtime.ritualBindings().register(
                id,
                (def, context, now) -> ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    @Override
                    public ArcanaDecision check(RitualDefinition def, RitualContext context, long nowTick) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public RitualComponentReservation reserve(RitualDefinition def, RitualContext context, long nowTick) {
                        return RitualComponentReservation.reserved(commits::incrementAndGet, () -> { });
                    }
                },
                (def, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });

        RitualContext context = new RitualContext(
                UUID.fromString("11111111-1111-1111-1111-111111111111"),
                List.of(),
                new RitualAnchor("minecraft:overworld", 42L));
        RitualResult started = runtime.rituals().start(
                definition,
                RitualActivationId.parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                context,
                100L);

        assertEquals(RitualResult.Status.STARTED, started.status());
        runtime.tick(120L);
        assertEquals(1, commits.get());
        assertEquals(1, runtime.rituals().activeSessionCount());
        runtime.tick(140L);
        assertEquals(1, outcomes.get());
        assertEquals(0, runtime.rituals().activeSessionCount());
        assertNotNull(runtime.lastRitualTickSummary());
    }
}
