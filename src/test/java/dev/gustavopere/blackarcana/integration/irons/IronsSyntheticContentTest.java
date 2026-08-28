package dev.gustavopere.blackarcana.integration.irons;

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

class IronsSyntheticContentTest {
    private static final UUID CASTER = UUID.fromString("66666666-6666-6666-6666-666666666666");

    @Test
    void syntheticHostedSpellConsumesManaOnceAndUsesCoreCooldown() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeMana mana = new FakeMana(100.0F, 100.0F);
        IronsSyntheticContent.install(runtime, mana, Optional.empty());

        assertTrue(runtime.spells().resolve(IronsIntegrationIds.PROBE_ARCANA_ID).isPresent());
        assertEquals(1, runtime.installedEngineCount());
        assertEquals(
            IronsSyntheticContent.COOLDOWN_TICKS,
            runtime.cooldownPolicies().cooldownSnapshot().get(IronsIntegrationIds.PROBE_ARCANA_ID).durationTicks());

        var first = runtime.handle(
            new ArcanaCastContext(CASTER, 100L, "minecraft:overworld"),
            intent("77777777-7777-7777-7777-777777777777"));
        assertEquals(ArcanaCastResult.Status.SUCCESS.name(), first.status());
        assertEquals(80.0F, mana.current);
        assertEquals(1, mana.adjustments);

        var second = runtime.handle(
            new ArcanaCastContext(CASTER, 101L, "minecraft:overworld"),
            intent("88888888-8888-8888-8888-888888888888"));
        assertEquals(ArcanaCastResult.Status.DENIED_COOLDOWN.name(), second.status());
        assertEquals(80.0F, mana.current);
        assertEquals(1, mana.adjustments);
    }

    private static CastIntentPayload intent(String castId) {
        return new CastIntentPayload(
            ArcanaProtocol.VERSION,
            castId,
            IronsIntegrationIds.PROBE_ARCANA_ID.canonical(),
            0,
            "");
    }

    private static final class FakeMana implements IronsManaAccess {
        private float current;
        private final float maximum;
        private int adjustments;

        private FakeMana(float current, float maximum) {
            this.current = current;
            this.maximum = maximum;
        }

        @Override
        public IronsManaSnapshot snapshot(UUID playerId) {
            assertEquals(CASTER, playerId);
            return new IronsManaSnapshot(current, maximum);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, float delta) {
            assertEquals(CASTER, playerId);
            float next = current + delta;
            if (next < 0.0F || next > maximum) {
                return ArcanaDecision.deny("fake_mana_bounds", "out of bounds");
            }
            current = next;
            adjustments++;
            return ArcanaDecision.allow();
        }
    }
}
