package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackArcanaGrandRitualsTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final RitualContext CONTEXT = new RitualContext(
            CASTER,
            List.of(),
            new RitualAnchor("minecraft:overworld", 42L));

    @Test
    void representativeGrandRitualCommitsOnceSurvivesRestartAndCannotRewardTwice() {
        AtomicInteger componentCommits = new AtomicInteger();
        AtomicInteger rewards = new AtomicInteger();
        AtomicBoolean completed = new AtomicBoolean();

        RitualComponentProvider components = new RitualComponentProvider() {
            @Override
            public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
                return ArcanaDecision.allow();
            }

            @Override
            public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
                return RitualComponentReservation.reserved(componentCommits::incrementAndGet, () -> { });
            }
        };

        var requirements = (RitualRequirementEvaluator) (definition, context, nowTick) -> completed.get()
                ? ArcanaDecision.deny("grand_ritual_already_completed", "grand ritual reward is already recorded")
                : ArcanaDecision.allow();
        var outcome = (RitualOutcomeExecutor) (definition, context, nowTick) -> {
            if (!completed.compareAndSet(false, true)) {
                return ArcanaDecision.deny("grand_ritual_duplicate_reward", "grand ritual reward already exists");
            }
            rewards.incrementAndGet();
            return ArcanaDecision.allow();
        };

        ArcanaServerRuntime first = ArcanaServerRuntime.createDefault();
        BlackArcanaGrandRituals.install(first, requirements, components, outcome);
        RitualActivationId activation = RitualActivationId.parse("22222222-2222-2222-2222-222222222222");

        assertEquals(
                RitualResult.Status.STARTED,
                first.rituals().start(
                        BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                        activation,
                        CONTEXT,
                        1_000L).status());
        first.rituals().tick(1_100L, 8);
        assertEquals(1, componentCommits.get());
        assertEquals(0, rewards.get());
        List<RitualSessionSnapshot> snapshot = first.rituals().snapshot(8);

        ArcanaServerRuntime restarted = ArcanaServerRuntime.createDefault();
        BlackArcanaGrandRituals.install(restarted, requirements, components, outcome);
        RitualRestoreResult restore = restarted.restoreRitualSessions(snapshot, 1_200L);
        assertEquals(1, restore.restored());
        assertEquals(0, restore.rejected());

        restarted.rituals().tick(1_400L, 8);
        assertEquals(1, componentCommits.get());
        assertEquals(1, rewards.get());

        assertEquals(
                RitualResult.Status.DENIED_REQUIREMENT,
                restarted.rituals().start(
                        BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                        RitualActivationId.parse("33333333-3333-3333-3333-333333333333"),
                        CONTEXT,
                        1_401L).status());
        assertEquals(1, componentCommits.get());
        assertEquals(1, rewards.get());
    }
}
