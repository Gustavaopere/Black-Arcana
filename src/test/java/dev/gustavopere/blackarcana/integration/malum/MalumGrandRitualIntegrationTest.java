package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.BlackArcanaGrandRituals;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import dev.gustavopere.blackarcana.persistence.RitualCompletionSavedData;
import dev.gustavopere.blackarcana.core.ritual.RitualActivationId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualResult;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class MalumGrandRitualIntegrationTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");

    @Test
    void grandRitualConsumesConfiguredSpiritsAndCompletesOnce() {
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 3));
        MalumRitualSpiritComponentProvider components = new MalumRitualSpiritComponentProvider(
                access,
                Map.of(
                        BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
                        List.of(
                                new MalumRitualSpiritRequirement("arcane", 4),
                                new MalumRitualSpiritRequirement("wicked", 2))));
        AtomicInteger rewards = new AtomicInteger();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        BlackArcanaGrandRituals.install(
                runtime,
                (definition, context, nowTick) -> ArcanaDecision.allow(),
                components,
                (definition, context, nowTick) -> {
                    rewards.incrementAndGet();
                    return ArcanaDecision.allow();
                });

        RitualContext context = new RitualContext(
                CASTER,
                List.of(),
                new RitualAnchor("minecraft:overworld", 42L));
        RitualResult started = runtime.rituals().start(
                BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                RitualActivationId.parse("22222222-2222-2222-2222-222222222222"),
                context,
                1_000L);
        assertEquals(RitualResult.Status.STARTED, started.status());

        runtime.rituals().tick(1_100L, 8);
        assertEquals(1, access.count(CASTER, "arcane"));
        assertEquals(1, access.count(CASTER, "wicked"));
        assertEquals(0, rewards.get());

        runtime.rituals().tick(1_400L, 8);
        assertEquals(1, rewards.get());
    }

    @Test
    void losingGrandRitualRequirementsAfterSpiritCommitSuppressesCompletion() {
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 3));
        MalumRitualSpiritComponentProvider components = new MalumRitualSpiritComponentProvider(
                access,
                Map.of(BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
                        List.of(new MalumRitualSpiritRequirement("arcane", 4),
                                new MalumRitualSpiritRequirement("wicked", 2))));
        java.util.concurrent.atomic.AtomicBoolean casterOnline = new java.util.concurrent.atomic.AtomicBoolean(true);
        AtomicInteger recordedCompletions = new AtomicInteger();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        BlackArcanaGrandRituals.install(
                runtime,
                (definition, context, nowTick) -> casterOnline.get()
                        ? ArcanaDecision.allow()
                        : ArcanaDecision.deny("grand_ritual_caster_offline", "caster logged out"),
                components,
                (definition, context, nowTick) -> {
                    recordedCompletions.incrementAndGet();
                    return ArcanaDecision.allow();
                });

        RitualContext context = new RitualContext(
                CASTER, List.of(), new RitualAnchor("minecraft:overworld", 42L));
        assertEquals(RitualResult.Status.STARTED,
                runtime.rituals().start(
                        BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                        RitualActivationId.parse("22222222-2222-2222-2222-222222222223"),
                        context, 1_000L).status());
        assertEquals(1, runtime.rituals().tick(1_100L, 8).committed());
        assertEquals(1, access.count(CASTER, "arcane"));
        assertEquals(1, access.count(CASTER, "wicked"));

        casterOnline.set(false);
        assertEquals(1, runtime.rituals().tick(1_400L, 8).cancelled());
        assertEquals(0, recordedCompletions.get());
        assertEquals(1, access.count(CASTER, "arcane"));
        assertEquals(1, access.count(CASTER, "wicked"));
        assertEquals(0, runtime.rituals().activeSessionCount());
    }

    @Test
    void fullCompletionLedgerDeniesGrandRitualBeforeAnyMalumSpiritsAreTaken() {
        RitualCompletionSavedData completions = new RitualCompletionSavedData();
        fillCompletionLedger(completions);
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 3));
        ArcanaServerRuntime runtime = completionCapacityRuntime(access, completions);

        RitualResult result = runtime.rituals().start(
                BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                RitualActivationId.parse("33333333-3333-3333-3333-333333333331"),
                new RitualContext(CASTER, List.of(), new RitualAnchor("minecraft:overworld", 42L)),
                1_000L);

        assertEquals(RitualResult.Status.DENIED_REQUIREMENT, result.status());
        assertEquals("grand_ritual_completion_capacity", result.code());
        assertEquals(5, access.count(CASTER, "arcane"));
        assertEquals(3, access.count(CASTER, "wicked"));
        assertEquals(0, runtime.rituals().activeSessionCount());
    }

    @Test
    void ledgerThatFillsDuringPreparationCancelsBeforeSpiritCommit() {
        RitualCompletionSavedData completions = new RitualCompletionSavedData();
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 3));
        ArcanaServerRuntime runtime = completionCapacityRuntime(access, completions);
        var context = new RitualContext(CASTER, List.of(), new RitualAnchor("minecraft:overworld", 42L));
        assertEquals(RitualResult.Status.STARTED, runtime.rituals().start(
                BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION,
                RitualActivationId.parse("33333333-3333-3333-3333-333333333332"),
                context, 1_000L).status());
        fillCompletionLedger(completions);

        assertEquals(1, runtime.rituals().tick(1_100L, 8).cancelled());
        assertEquals(5, access.count(CASTER, "arcane"));
        assertEquals(3, access.count(CASTER, "wicked"));
        assertEquals(0, runtime.rituals().activeSessionCount());
    }

    private static ArcanaServerRuntime completionCapacityRuntime(
            FakeAccess access, RitualCompletionSavedData completions) {
        MalumRitualSpiritComponentProvider components = new MalumRitualSpiritComponentProvider(
                access,
                Map.of(BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
                        List.of(new MalumRitualSpiritRequirement("arcane", 4),
                                new MalumRitualSpiritRequirement("wicked", 2))));
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        BlackArcanaGrandRituals.install(runtime,
                (definition, context, nowTick) -> MalumServerIntegrationBootstrap.checkGrandRitualCompletionAdmission(
                        completions,
                        RitualCompletionKey.forCaster(definition.id(), context.casterId())),
                components,
                (definition, context, nowTick) -> {
                    RitualCompletionLedger.CompletionResult result = completions.complete(
                            RitualCompletionKey.forCaster(definition.id(), context.casterId()), nowTick);
                    return result == RitualCompletionLedger.CompletionResult.RECORDED
                            ? ArcanaDecision.allow()
                            : ArcanaDecision.deny("grand_ritual_completion_capacity", "completion unavailable");
                });
        return runtime;
    }

    private static void fillCompletionLedger(RitualCompletionSavedData data) {
        for (int i = 0; i < RitualCompletionSavedData.MAX_PERSISTED_COMPLETIONS; i++) {
            RitualCompletionKey key = RitualCompletionKey.forCaster(
                    BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID, new UUID(0L, i + 10L));
            assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, data.complete(key, i));
        }
    }

    private static final class FakeAccess implements MalumSpiritAccess {
        private final Map<String, Integer> counts = new HashMap<>();

        FakeAccess(Map<String, Integer> initial) {
            counts.putAll(initial);
        }

        @Override
        public int count(UUID playerId, String affinity) {
            return counts.getOrDefault(affinity, 0);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, String affinity, int delta) {
            int next = count(playerId, affinity) + delta;
            if (next < 0) return ArcanaDecision.deny("insufficient", "not enough spirits");
            counts.put(affinity, next);
            return ArcanaDecision.allow();
        }
    }
}
