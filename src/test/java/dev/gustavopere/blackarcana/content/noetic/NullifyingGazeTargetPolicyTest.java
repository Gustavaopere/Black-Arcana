package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NullifyingGazeTargetPolicyTest {
    @Test
    void bossTargetsFailClosed() {
        ArcanaDecision decision = evaluateOrDefaultAllow(
            new EntityProtectionFacts(false, false, true, false, true));

        assertFalse(decision.allowed(), "boss targets must resist Nullifying Gaze by default");
    }

    @Test
    void ordinaryTargetsRemainEligibleForNormalAdmission() {
        ArcanaDecision decision = evaluateOrDefaultAllow(
            new EntityProtectionFacts(false, false, false, false, true));

        assertTrue(decision.allowed(), "ordinary targets must continue to normal effect/admission checks");
    }

    private static ArcanaDecision evaluateOrDefaultAllow(EntityProtectionFacts facts) {
        try {
            Class<?> policy = Class.forName(
                "dev.gustavopere.blackarcana.content.noetic.NullifyingGazeTargetPolicy");
            Method evaluate = policy.getMethod("evaluate", EntityProtectionFacts.class);
            return (ArcanaDecision) evaluate.invoke(null, facts);
        } catch (ReflectiveOperationException missingPolicy) {
            return ArcanaDecision.allow();
        }
    }
}
