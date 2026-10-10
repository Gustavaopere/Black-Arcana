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
    void boundedTickFairlyServesReadyRitualBehindAnEarlierSlowRitual() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);
        RitualDefinition slow = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:slow_altar"), 100L, 200L);
        RitualDefinition fast = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:fast_altar"), 5L, 10L);
        RitualAnchor fastAnchor = new RitualAnchor("minecraft:overworld", 43L);

        assertEquals(RitualResult.Status.STARTED,
                engine.start(slow, activation("d1000000-0000-0000-0000-000000000001"),
                        context(), 1_000L).status());
        assertEquals(RitualResult.Status.STARTED,
                engine.start(fast, activation("d1000000-0000-0000-0000-000000000002"),
                        new RitualContext(CASTER, List.of(), fastAnchor), 1_000L).status());

        assertEquals(0, engine.tick(1_005L, 1).committed()); // older ritual not due
        assertEquals(1, engine.tick(1_006L, 1).committed()); // younger one gets a turn
        assertEquals(1, components.commitCount.get());
        assertEquals(0, engine.tick(1_010L, 1).completed());
        assertEquals(1, engine.tick(1_011L, 1).completed());
        assertEquals(1, outcomes.get());
        assertEquals(1, engine.activeSessionCount());
        assertEquals(slow.id(), engine.snapshot(8).getFirst().ritualId());
    }

    @Test
    void roundRobinRespectsPerTickBudgetWhileAllThreeRitualsProgress() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);

        for (int i = 0; i < 3; i++) {
            RitualActivationId activation = new RitualActivationId(
                    UUID.nameUUIDFromBytes(("fair-ritual-" + i).getBytes()));
            RitualAnchor anchor = new RitualAnchor("minecraft:overworld", 100L + i);
            assertEquals(RitualResult.Status.STARTED,
                    engine.start(DEFINITION, activation,
                            new RitualContext(CASTER, List.of(), anchor), 100L).status());
        }

        int committed = 0;
        for (int i = 0; i < 3; i++) {
            RitualEngine.TickSummary summary = engine.tick(120L, 1);
            assertTrue(summary.committed() <= 1);
            committed += summary.committed();
        }
        assertEquals(3, committed);
        assertEquals(3, components.commitCount.get());

        int completed = 0;
        for (int i = 0; i < 3; i++) {
            RitualEngine.TickSummary summary = engine.tick(140L, 1);
            assertTrue(summary.completed() <= 1);
            completed += summary.completed();
        }
        assertEquals(3, completed);
        assertEquals(3, outcomes.get());
        assertEquals(0, engine.activeSessionCount());
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
    void requirementRevokedBeforeCommitCancelsWithoutSpendingComponents() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        java.util.concurrent.atomic.AtomicBoolean online = new java.util.concurrent.atomic.AtomicBoolean(true);
        RitualEngine engine = new RitualEngine(
                new RitualSessionRegistry(8),
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> online.get()
                        ? ArcanaDecision.allow()
                        : ArcanaDecision.deny("grand_ritual_caster_offline", "caster disconnected"),
                components,
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });
        RitualActivationId activation = activation("f0000000-0000-0000-0000-000000000001");

        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation, context(), 100L).status());
        online.set(false);

        RitualEngine.TickSummary summary = engine.tick(120L, 8);
        assertEquals(1, summary.cancelled());
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, components.commitCount.get());
        assertEquals(0, components.refundCount.get());
        assertEquals(0, outcomes.get());
        assertEquals(0, engine.activeSessionCount());
    }

    @Test
    void requirementRevokedAfterCommitPreventsOutcomeWithoutRefund() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        java.util.concurrent.atomic.AtomicBoolean chunkLoaded = new java.util.concurrent.atomic.AtomicBoolean(true);
        RitualEngine engine = new RitualEngine(
                new RitualSessionRegistry(8),
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> chunkLoaded.get()
                        ? ArcanaDecision.allow()
                        : ArcanaDecision.deny("grand_ritual_chunk_unloaded", "anchor unloaded"),
                components,
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });

        engine.start(DEFINITION, activation("f0000000-0000-0000-0000-000000000002"), context(), 100L);
        assertEquals(1, engine.tick(120L, 8).committed());
        assertEquals(1, components.commitCount.get());
        chunkLoaded.set(false);

        RitualEngine.TickSummary summary = engine.tick(140L, 8);
        assertEquals(1, summary.cancelled());
        assertEquals(0, summary.completed());
        assertEquals(0, outcomes.get());
        assertEquals(0, components.refundCount.get());
        assertEquals(0, engine.activeSessionCount());
    }

    @Test
    void requirementRecheckExceptionFailsClosedAtCommit() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        AtomicInteger checks = new AtomicInteger();
        RitualEngine engine = new RitualEngine(
                new RitualSessionRegistry(8),
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> {
                    if (checks.incrementAndGet() > 1) throw new IllegalStateException("provider unavailable");
                    return ArcanaDecision.allow();
                },
                components,
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });
        engine.start(DEFINITION, activation("f0000000-0000-0000-0000-000000000003"), context(), 100L);
        RitualEngine.TickSummary summary = engine.tick(120L, 8);
        assertEquals(1, summary.cancelled());
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, outcomes.get());
    }

    @Test
    void casterDisconnectBeforeCommitCannotBeHiddenByImmediateReconnect() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);
        RitualActivationId activation = activation("f1000000-0000-0000-0000-000000000001");

        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation, context(), 100L).status());
        assertEquals(1, engine.interruptCaster(CASTER, "ritual_caster_disconnected"));
        assertEquals(0, engine.interruptCaster(CASTER, "ritual_caster_disconnected"));
        assertEquals(0, engine.activeSessionCount());
        assertTrue(engine.snapshot(8).isEmpty());

        // Requirements may be valid again on the next tick; the interrupted activation
        // must not resume or commit resources after a fast reconnect.
        engine.tick(120L, 8);
        engine.tick(140L, 8);
        assertEquals(0, components.reserveCount.get());
        assertEquals(0, components.commitCount.get());
        assertEquals(0, outcomes.get());
        assertEquals(RitualResult.Status.DENIED_REPLAY,
                engine.start(DEFINITION, activation, context(), 141L).status());
    }

    @Test
    void dimensionChangeAfterCommitDoesNotRefundOrCompleteOnReturn() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);
        RitualActivationId activation = activation("f1000000-0000-0000-0000-000000000002");
        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation, context(), 100L).status());
        assertEquals(1, engine.tick(120L, 8).committed());
        assertEquals(1, components.commitCount.get());

        assertEquals(1, engine.interruptCaster(CASTER, "ritual_caster_changed_dimension"));
        assertEquals(0, engine.activeSessionCount());
        assertTrue(engine.snapshot(8).isEmpty());
        engine.tick(140L, 8);
        assertEquals(1, components.commitCount.get());
        assertEquals(0, components.refundCount.get());
        assertEquals(0, outcomes.get());
    }

    @Test
    void casterInterruptionIsScopedAndReleasesAllOwnedAnchors() {
        FakeComponents components = new FakeComponents();
        AtomicInteger outcomes = new AtomicInteger();
        RitualEngine engine = engine(components, outcomes);
        UUID other = UUID.fromString("22222222-2222-2222-2222-222222222222");
        RitualAnchor secondAnchor = new RitualAnchor("minecraft:overworld", 43L);
        RitualAnchor otherAnchor = new RitualAnchor("minecraft:overworld", 44L);

        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation("f1000000-0000-0000-0000-000000000003"),
                        context(), 100L).status());
        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation("f1000000-0000-0000-0000-000000000004"),
                        new RitualContext(CASTER, List.of(), secondAnchor), 100L).status());
        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation("f1000000-0000-0000-0000-000000000005"),
                        new RitualContext(other, List.of(), otherAnchor), 100L).status());

        assertEquals(2, engine.interruptCaster(CASTER, "ritual_caster_died"));
        assertEquals(1, engine.activeSessionCount());
        assertEquals(other, engine.snapshot(8).getFirst().context().casterId());

        // A second player may immediately use the released anchor with a fresh server nonce.
        assertEquals(RitualResult.Status.STARTED,
                engine.start(DEFINITION, activation("f1000000-0000-0000-0000-000000000006"),
                        new RitualContext(other, List.of(), ANCHOR), 101L).status());
        assertEquals(1, engine.tick(120L, 8).committed());
        assertEquals(1, engine.tick(140L, 8).committed());
        assertEquals(1, outcomes.get());
        assertEquals(1, engine.tick(141L, 8).completed());
        assertEquals(2, outcomes.get());
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
