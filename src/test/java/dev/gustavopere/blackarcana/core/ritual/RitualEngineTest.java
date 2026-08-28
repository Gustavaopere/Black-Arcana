package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RitualEngineTest {
    private static final ArcanaRitualId RITUAL = ArcanaRitualId.parse("black_arcana:test_rite");
    private static final RitualAnchor ANCHOR = new RitualAnchor("minecraft:overworld", 42L);
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final RitualDefinition DEFINITION = new RitualDefinition(RITUAL, 20L, 40L);

    @Test
    void interruptionBeforeCommitConsumesNothing() {
        FakeComponents components = new FakeComponents();
        RitualEngine engine = engine(components, new AtomicInteger());
        RitualActivationId activation = activation("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");

        assertEquals(RitualResult.Status.STARTED, engine.start(DEFINITION, activation, context(), 100L).status());
        assertEquals(0, components.reserveCount.get());

        assertEquals(RitualResult.Status.INTERRUPTED_PRECOMMIT,
                engine.interrupt(activation, "layout_broken").status());
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, components.commitCount.get());
        assertEquals(0, components.refundCount.get());
        assertEquals(0, engine.activeSessionCount());
    }

    @Test
    void commitAndOutcomeRunExactlyOnceAndActivationCannotReplay() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);
        RitualActivationId activation = activation("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb");

        assertEquals(RitualResult.Status.STARTED, engine.start(DEFINITION, activation, context(), 100L).status());
        engine.tick(119L, 16);
        assertEquals(0, components.reserveCount.get());

        RitualEngine.TickSummary committed = engine.tick(120L, 16);
        assertEquals(1, committed.committed());
        assertEquals(1, components.reserveCount.get());
        assertEquals(1, components.commitCount.get());
        assertEquals(0, outcomes.get());

        engine.tick(120L, 16);
        assertEquals(1, components.commitCount.get());

        RitualEngine.TickSummary completed = engine.tick(140L, 16);
        assertEquals(1, completed.completed());
        assertEquals(1, outcomes.get());
        assertEquals(0, engine.activeSessionCount());

        assertEquals(RitualResult.Status.DENIED_REPLAY,
                engine.start(DEFINITION, activation, context(), 141L).status());
        assertEquals(1, components.commitCount.get());
        assertEquals(1, outcomes.get());
    }

    @Test
    void missingComponentsAtCommitCancelWithoutConsumption() {
        FakeComponents components = new FakeComponents();
        RitualEngine engine = engine(components, new AtomicInteger());
        RitualActivationId activation = activation("cccccccc-cccc-cccc-cccc-cccccccccccc");

        assertEquals(RitualResult.Status.STARTED, engine.start(DEFINITION, activation, context(), 100L).status());
        components.available = false;

        RitualEngine.TickSummary summary = engine.tick(120L, 16);
        assertEquals(1, summary.cancelled());
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, components.commitCount.get());
        assertEquals(0, engine.activeSessionCount());
    }

    @Test
    void sameAnchorMultiplayerRaceAdmitsExactlyOneSession() throws Exception {
        FakeComponents components = new FakeComponents();
        RitualEngine engine = engine(components, new AtomicInteger());
        CountDownLatch ready = new CountDownLatch(2);
        CountDownLatch go = new CountDownLatch(1);
        AtomicInteger started = new AtomicInteger();
        AtomicInteger busy = new AtomicInteger();

        try (var executor = Executors.newFixedThreadPool(2)) {
            for (int index = 0; index < 2; index++) {
                final int actor = index;
                executor.submit(() -> {
                    ready.countDown();
                    go.await(5, TimeUnit.SECONDS);
                    RitualContext contender = new RitualContext(
                            UUID.nameUUIDFromBytes(("caster-" + actor).getBytes()),
                            List.of(),
                            ANCHOR);
                    RitualResult result = engine.start(
                            DEFINITION,
                            new RitualActivationId(UUID.nameUUIDFromBytes(("activation-" + actor).getBytes())),
                            contender,
                            100L);
                    if (result.status() == RitualResult.Status.STARTED) started.incrementAndGet();
                    if (result.status() == RitualResult.Status.DENIED_ANCHOR_BUSY) busy.incrementAndGet();
                    return null;
                });
            }
            assertTrue(ready.await(5, TimeUnit.SECONDS));
            go.countDown();
            executor.shutdown();
            assertTrue(executor.awaitTermination(5, TimeUnit.SECONDS));
        }

        assertEquals(1, started.get());
        assertEquals(1, busy.get());
        assertEquals(1, engine.activeSessionCount());
    }

    @Test
    void committedSessionRestoresWithoutConsumingComponentsTwice() {
        FakeComponents beforeRestart = new FakeComponents();
        AtomicInteger preRestartOutcomes = new AtomicInteger();
        RitualEngine first = engine(beforeRestart, preRestartOutcomes);
        RitualActivationId activation = activation("dddddddd-dddd-dddd-dddd-dddddddddddd");

        first.start(DEFINITION, activation, context(), 100L);
        first.tick(120L, 16);
        assertEquals(1, beforeRestart.commitCount.get());
        List<RitualSessionSnapshot> snapshot = first.snapshot(16);
        assertEquals(RitualSessionState.COMMITTED, snapshot.getFirst().state());

        FakeComponents afterRestart = new FakeComponents();
        AtomicInteger postRestartOutcomes = new AtomicInteger();
        RitualEngine restored = engine(afterRestart, postRestartOutcomes);
        RitualRestoreResult restore = restored.restore(List.of(DEFINITION), snapshot, 125L);
        assertEquals(1, restore.restored());
        assertEquals(0, restore.rejected());

        restored.tick(140L, 16);
        assertEquals(0, afterRestart.reserveCount.get());
        assertEquals(0, afterRestart.commitCount.get());
        assertEquals(1, postRestartOutcomes.get());
        assertEquals(0, restored.activeSessionCount());
    }

    @Test
    void failedInitialRequirementNeverClaimsAnchorOrComponents() {
        FakeComponents components = new FakeComponents();
        RitualSessionRegistry sessions = new RitualSessionRegistry(8);
        RitualEngine engine = new RitualEngine(
                sessions,
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> ArcanaDecision.deny("layout_invalid", "sigil incomplete"),
                components,
                (definition, context, now) -> ArcanaDecision.allow());

        RitualResult result = engine.start(
                DEFINITION,
                activation("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),
                context(),
                100L);

        assertEquals(RitualResult.Status.DENIED_REQUIREMENT, result.status());
        assertEquals("layout_invalid", result.code());
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, engine.activeSessionCount());
    }

    private static RitualEngine engine(FakeComponents components, AtomicInteger outcomes) {
        return new RitualEngine(
                new RitualSessionRegistry(8),
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> ArcanaDecision.allow(),
                components,
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });
    }

    private static RitualContext context() {
        return new RitualContext(CASTER, List.of(), ANCHOR);
    }

    private static RitualActivationId activation(String uuid) {
        return new RitualActivationId(UUID.fromString(uuid));
    }

    private static final class FakeComponents implements RitualComponentProvider {
        final AtomicInteger reserveCount = new AtomicInteger();
        final AtomicInteger commitCount = new AtomicInteger();
        final AtomicInteger refundCount = new AtomicInteger();
        volatile boolean available = true;

        @Override
        public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
            return available
                    ? ArcanaDecision.allow()
                    : ArcanaDecision.deny("components_missing", "required components are not present");
        }

        @Override
        public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
            reserveCount.incrementAndGet();
            if (!available) {
                return RitualComponentReservation.denied("components_missing", "required components are not present");
            }
            return RitualComponentReservation.reserved(
                    commitCount::incrementAndGet,
                    refundCount::incrementAndGet);
        }
    }
}
