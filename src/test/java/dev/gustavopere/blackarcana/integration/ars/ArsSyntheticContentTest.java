package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArsSyntheticContentTest {
    private static final UUID CASTER = UUID.fromString("99999999-9999-9999-9999-999999999999");

    @Test
    void syntheticArsBackedSpellConsumesManaOnceAndUsesCoreCooldown() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeMana mana = new FakeMana(100.0D, 100.0D);
        ArsSyntheticContent.install(runtime, mana, Optional.empty());

        assertTrue(runtime.spells().resolve(ArsIntegrationIds.PROBE_ARCANA_ID).isPresent());
        assertEquals(1, runtime.installedEngineCount());
        assertEquals(
            ArsSyntheticContent.COOLDOWN_TICKS,
            runtime.cooldownPolicies().cooldownSnapshot().get(ArsIntegrationIds.PROBE_ARCANA_ID).durationTicks());

        var first = runtime.handle(
            new ArcanaCastContext(CASTER, 200L, "minecraft:overworld"),
            intent("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"));
        assertEquals(ArcanaCastResult.Status.SUCCESS.name(), first.status());
        assertEquals(75.0D, mana.current);
        assertEquals(1, mana.adjustments);

        var second = runtime.handle(
            new ArcanaCastContext(CASTER, 201L, "minecraft:overworld"),
            intent("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"));
        assertEquals(ArcanaCastResult.Status.DENIED_COOLDOWN.name(), second.status());
        assertEquals(75.0D, mana.current);
        assertEquals(1, mana.adjustments);
    }

    private static CastIntentPayload intent(String castId) {
        return new CastIntentPayload(
            ArcanaProtocol.VERSION,
            castId,
            ArsIntegrationIds.PROBE_ARCANA_ID.canonical(),
            0,
            "");
    }

    private static final class FakeMana implements ArsManaAccess {
        private double current;
        private final double maximum;
        private int adjustments;

        private FakeMana(double current, double maximum) {
            this.current = current;
            this.maximum = maximum;
        }

        @Override
        public ArsManaSnapshot snapshot(UUID playerId) {
            assertEquals(CASTER, playerId);
            return new ArsManaSnapshot(current, maximum);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, double delta) {
            assertEquals(CASTER, playerId);
            double next = current + delta;
            if (next < 0.0D || next > maximum) {
                return ArcanaDecision.deny("fake_mana_bounds", "out of bounds");
            }
            current = next;
            adjustments++;
            return ArcanaDecision.allow();
        }
    }
}
