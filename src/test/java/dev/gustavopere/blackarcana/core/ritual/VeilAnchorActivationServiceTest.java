package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

class VeilAnchorActivationServiceTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final UUID OTHER = UUID.fromString("44444444-4444-4444-4444-444444444444");
    private static final RitualAnchor ANCHOR = new RitualAnchor("minecraft:overworld", 42L);

    @Test
    void unavailableProviderAndMissingBindingNeverCreateFreeRitual() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        assertEquals("grand_ritual_provider_missing",
                VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 100L).code());
        runtime.ritualDefinitions().register(BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION);
        assertEquals("grand_ritual_provider_missing",
                VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 101L).code());
        assertEquals(0, runtime.rituals().activeSessionCount());
    }

    @Test
    void unavailableSpiritsAreRejectedBeforeSessionAndConsumeNothing() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AtomicInteger reserves = new AtomicInteger();
        BlackArcanaGrandRituals.install(runtime,
                (definition, context, now) -> ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long tick) {
                        return ArcanaDecision.deny("ritual_spirits_missing", "spirits unavailable");
                    }
                    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long tick) {
                        reserves.incrementAndGet();
                        return RitualComponentReservation.denied("ritual_spirits_missing", "spirits unavailable");
                    }
                },
                (definition, context, now) -> ArcanaDecision.allow());
        RitualResult result = VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 1_000L);
        assertEquals(RitualResult.Status.DENIED_REQUIREMENT, result.status());
        assertEquals("ritual_spirits_missing", result.code());
        assertEquals(0, reserves.get());
        assertEquals(0, runtime.rituals().activeSessionCount());
    }

    @Test
    void providerPreflightExceptionDeniesWithoutClaimingAnchorOrConsumingSpirits() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AtomicInteger reserves = new AtomicInteger();
        BlackArcanaGrandRituals.install(runtime,
                (definition, context, now) -> ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    @Override
                    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long now) {
                        throw new IllegalStateException("Malum resource API became unavailable");
                    }

                    @Override
                    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long now) {
                        reserves.incrementAndGet();
                        return RitualComponentReservation.denied("not_reserved", "should never reserve");
                    }
                },
                (definition, context, now) -> ArcanaDecision.allow());

        RitualResult result = VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 1_000L);

        assertEquals(RitualResult.Status.DENIED_REQUIREMENT, result.status());
        assertEquals("grand_ritual_component_preflight_failed", result.code());
        assertEquals(0, runtime.rituals().activeSessionCount());
        assertEquals(0, reserves.get());
    }

    @Test
    void nullAndLinkageFailureFromProviderPreflightDenyWithoutAnyNewSession() {
        for (boolean linkageError : new boolean[]{false, true}) {
            ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
            AtomicInteger reserves = new AtomicInteger();
            BlackArcanaGrandRituals.install(runtime,
                    (definition, context, now) -> ArcanaDecision.allow(),
                    new RitualComponentProvider() {
                        @Override
                        public ArcanaDecision check(RitualDefinition definition, RitualContext context, long now) {
                            if (linkageError) throw new NoClassDefFoundError("malum/spirit/Api");
                            return null;
                        }

                        @Override
                        public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long now) {
                            reserves.incrementAndGet();
                            return RitualComponentReservation.denied("not_reserved", "should never reserve");
                        }
                    },
                    (definition, context, now) -> ArcanaDecision.allow());

            RitualResult result = VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 1_000L);

            assertEquals(RitualResult.Status.DENIED_REQUIREMENT, result.status());
            assertEquals("grand_ritual_component_preflight_failed", result.code());
            assertEquals(0, runtime.rituals().activeSessionCount());
            assertEquals(0, reserves.get());
        }
    }

    @Test
    void authenticatedActivationStartsOneSessionAndCompetingPlayerCannotTakeSameAltar() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AtomicInteger commits = new AtomicInteger();
        AtomicInteger rewards = new AtomicInteger();
        AtomicBoolean completed = new AtomicBoolean();
        BlackArcanaGrandRituals.install(runtime,
                (definition, context, now) -> completed.get()
                        ? ArcanaDecision.deny("grand_ritual_already_completed", "already completed")
                        : ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long tick) {
                        return ArcanaDecision.allow();
                    }
                    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long tick) {
                        return RitualComponentReservation.reserved(commits::incrementAndGet, () -> { });
                    }
                },
                (definition, context, now) -> {
                    rewards.incrementAndGet();
                    completed.set(true);
                    return ArcanaDecision.allow();
                });
        assertEquals(RitualResult.Status.STARTED,
                VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 1_000L).status());
        RitualResult competing = VeilAnchorActivationService.start(runtime, OTHER, ANCHOR, 1_001L);
        assertEquals(RitualResult.Status.DENIED_ANCHOR_BUSY, competing.status());
        assertEquals(1, runtime.rituals().activeSessionCount());
        assertEquals(0, commits.get());
        assertEquals(1, runtime.rituals().tick(1_100L, 8).committed());
        assertEquals(1, commits.get());
        assertEquals(0, rewards.get());
        assertEquals(1, runtime.rituals().tick(1_400L, 8).completed());
        assertEquals(1, rewards.get());
        assertEquals(0, runtime.rituals().activeSessionCount());
        assertEquals("grand_ritual_already_completed",
                VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 1_401L).code());
        assertEquals(1, commits.get());
        assertEquals(1, rewards.get());
    }

    @Test
    void interruptionBeforeCommitStillSpendsNothing() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AtomicInteger commits = new AtomicInteger();
        BlackArcanaGrandRituals.install(runtime,
                (d, c, t) -> ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    public ArcanaDecision check(RitualDefinition d, RitualContext c, long t) {
                        return ArcanaDecision.allow();
                    }
                    public RitualComponentReservation reserve(RitualDefinition d, RitualContext c, long t) {
                        return RitualComponentReservation.reserved(commits::incrementAndGet, () -> { });
                    }
                },
                (d, c, t) -> ArcanaDecision.allow());
        VeilAnchorActivationService.start(runtime, CASTER, ANCHOR, 100L);
        RitualSessionSnapshot snapshot = runtime.rituals().snapshot(8).getFirst();
        assertEquals(RitualResult.Status.INTERRUPTED_PRECOMMIT,
                runtime.rituals().interrupt(snapshot.activationId(), "altar dismantled").status());
        assertEquals(0, commits.get());
        assertEquals(0, runtime.rituals().activeSessionCount());
    }
}
