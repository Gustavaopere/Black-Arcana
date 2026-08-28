package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MalumSyntheticContentTest {
    private static final UUID CASTER = UUID.fromString("14141414-1414-1414-1414-141414141414");

    @Test
    void syntheticMalumBackedSpellConsumesSpiritsOnceAndUsesCoreCooldown() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeSpirits spirits = new FakeSpirits(Map.of(MalumIntegrationIds.PROBE_AFFINITY, 5));
        MalumSyntheticContent.install(runtime, spirits, Optional.empty());

        assertTrue(runtime.spells().resolve(MalumIntegrationIds.PROBE_ARCANA_ID).isPresent());
        assertEquals(1, runtime.installedEngineCount());
        assertEquals(
            MalumSyntheticContent.COOLDOWN_TICKS,
            runtime.cooldownPolicies().cooldownSnapshot().get(MalumIntegrationIds.PROBE_ARCANA_ID).durationTicks());

        var first = runtime.handle(
            new ArcanaCastContext(CASTER, 300L, "minecraft:overworld"),
            intent("15151515-1515-1515-1515-151515151515"));
        assertEquals(ArcanaCastResult.Status.SUCCESS.name(), first.status());
        assertEquals(3, spirits.count(CASTER, MalumIntegrationIds.PROBE_AFFINITY));
        assertEquals(1, spirits.adjustments);

        var second = runtime.handle(
            new ArcanaCastContext(CASTER, 301L, "minecraft:overworld"),
            intent("16161616-1616-1616-1616-161616161616"));
        assertEquals(ArcanaCastResult.Status.DENIED_COOLDOWN.name(), second.status());
        assertEquals(3, spirits.count(CASTER, MalumIntegrationIds.PROBE_AFFINITY));
        assertEquals(1, spirits.adjustments);
    }

    private static CastIntentPayload intent(String castId) {
        return new CastIntentPayload(
            ArcanaProtocol.VERSION,
            castId,
            MalumIntegrationIds.PROBE_ARCANA_ID.canonical(),
            0,
            "");
    }

    private static final class FakeSpirits implements MalumSpiritAccess {
        private final Map<String, Integer> counts = new HashMap<>();
        private int adjustments;

        private FakeSpirits(Map<String, Integer> initial) {
            counts.putAll(initial);
        }

        @Override
        public int count(UUID playerId, String affinity) {
            assertEquals(CASTER, playerId);
            return counts.getOrDefault(affinity, 0);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, String affinity, int delta) {
            assertEquals(CASTER, playerId);
            int next = counts.getOrDefault(affinity, 0) + delta;
            if (next < 0) return ArcanaDecision.deny("fake_spirit_bounds", "negative count");
            counts.put(affinity, next);
            adjustments++;
            return ArcanaDecision.allow();
        }
    }
}
