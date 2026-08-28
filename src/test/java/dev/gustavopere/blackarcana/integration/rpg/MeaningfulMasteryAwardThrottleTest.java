package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MeaningfulMasteryAwardThrottleTest {
    private static final UUID CASTER = UUID.fromString("22222222-2222-2222-2222-222222222222");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
        ArcanaSpellId.parse("black_arcana:mastery_probe"),
        "spell.black_arcana.mastery_probe",
        "black_arcana:mastery_probe",
        ArcanaCost.none(),
        false);

    @Test
    void sameSpellAndTargetInsideWindowDoesNotAwardAgain() {
        var throttle = new MeaningfulMasteryAwardThrottle(40L, 16);
        var target = TargetResolution.resolved("entity:target-a");

        assertTrue(throttle.allow(request(100L), target));
        assertFalse(throttle.allow(request(101L), target));
        assertFalse(throttle.allow(request(139L), target));
        assertTrue(throttle.allow(request(140L), target));
    }

    @Test
    void differentMeaningfulTargetsCanProgressIndependently() {
        var throttle = new MeaningfulMasteryAwardThrottle(40L, 16);

        assertTrue(throttle.allow(request(100L), TargetResolution.resolved("entity:target-a")));
        assertTrue(throttle.allow(request(101L), TargetResolution.resolved("entity:target-b")));
    }

    @Test
    void targetSetOrderingDoesNotCreateASecondRewardIdentity() {
        var throttle = new MeaningfulMasteryAwardThrottle(40L, 16);

        assertTrue(throttle.allow(request(100L), TargetResolution.resolved(List.of("entity:b", "entity:a"))));
        assertFalse(throttle.allow(request(101L), TargetResolution.resolved(List.of("entity:a", "entity:b"))));
    }

    @Test
    void saturationFailsClosedForMasteryWithoutEvictingActiveIdentity() {
        var throttle = new MeaningfulMasteryAwardThrottle(100L, 1);

        assertTrue(throttle.allow(request(10L), TargetResolution.resolved("entity:first")));
        assertFalse(throttle.allow(request(11L), TargetResolution.resolved("entity:second")));
        assertFalse(throttle.allow(request(12L), TargetResolution.resolved("entity:first")));
        assertTrue(throttle.allow(request(110L), TargetResolution.resolved("entity:second")));
    }

    @Test
    void deniedTargetResolutionNeverAwardsMastery() {
        var throttle = new MeaningfulMasteryAwardThrottle(40L, 16);
        assertFalse(throttle.allow(request(100L), TargetResolution.denied("no valid target")));
    }

    private static ArcanaCastRequest request(long tick) {
        return new ArcanaCastRequest(
            SPELL,
            new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }
}
