package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RpgMasteryAwardObserverMeaningfulUseTest {
    private static final UUID CASTER = UUID.fromString("22222222-2222-2222-2222-222222222222");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
        ArcanaSpellId.parse("black_arcana:mastery_probe"),
        "spell.black_arcana.mastery_probe",
        "black_arcana:mastery_probe",
        ArcanaCost.none(),
        false);
    private static final RpgMasteryAwardSpec AWARD = new RpgMasteryAwardSpec(
        "black_arcana:casting", 5, "black_arcana:mastery_probe");

    @Test
    void committedRepeatedCastAgainstSameTargetAwardsOncePerWindow() {
        FakeBridge bridge = new FakeBridge();
        RpgMasteryAwardObserver observer = new RpgMasteryAwardObserver(
            bridge,
            request -> Optional.of(AWARD),
            ignored -> { },
            new MeaningfulMasteryAwardThrottle(40L, 32));
        TargetResolution target = TargetResolution.resolved("entity:target-a");

        observer.onSuccess(request(100L), target, EffectResult.ok());
        observer.onSuccess(request(101L), target, EffectResult.ok());
        observer.onSuccess(request(140L), target, EffectResult.ok());

        assertEquals(2, bridge.awards);
    }

    @Test
    void failedEffectNeverAwardsEvenIfObserverIsCalledDefensively() {
        FakeBridge bridge = new FakeBridge();
        RpgMasteryAwardObserver observer = new RpgMasteryAwardObserver(
            bridge,
            request -> Optional.of(AWARD),
            ignored -> { },
            new MeaningfulMasteryAwardThrottle(40L, 32));

        observer.onSuccess(request(100L), TargetResolution.resolved("entity:target-a"), EffectResult.failed("failed"));

        assertEquals(0, bridge.awards);
    }

    private static ArcanaCastRequest request(long tick) {
        return new ArcanaCastRequest(SPELL, new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    private static final class FakeBridge implements RpgSkillTreeBridge {
        int awards;

        @Override
        public String integrationId() {
            return "rpgskilltree";
        }

        @Override
        public boolean available() {
            return true;
        }

        @Override
        public String implementationVersion() {
            return "test";
        }

        @Override
        public RpgProgressionQuery query(UUID playerId) {
            return RpgProgressionQuery.denied("unused", "unused in mastery award test");
        }

        @Override
        public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
            awards++;
            return ArcanaDecision.allow();
        }
    }
}
