package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.BlackArcanaGrandRituals;
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
