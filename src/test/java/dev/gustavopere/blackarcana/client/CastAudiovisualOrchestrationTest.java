package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CastAudiovisualOrchestrationTest {
    private static final ArcanaCastId CAST_A = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");
    private static final ArcanaCastId CAST_B = ArcanaCastId.parse("22222222-2222-2222-2222-222222222222");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:test_spell");

    @Test
    void localIntentEmitsRestrainedNonAuthoritativeAnticipation() {
        List<CastAudiovisualOrchestration.Directive> emitted = new ArrayList<>();
        var controller = controller(fullPolicy(), emitted);

        var directive = controller.recordLocalIntent(CAST_A, SPELL, 10L).orElseThrow();

        assertEquals(CastAudiovisualOrchestration.Kind.ANTICIPATION, directive.kind());
        assertEquals(CastPresentationLifecycle.Authority.LOCAL_INTENT_PRESENTATION, directive.authority());
        assertEquals(CAST_A, directive.castId());
        assertEquals(SPELL, directive.spellId().orElseThrow());
        assertFalse(directive.authoritative());
        assertEquals(List.of(directive), emitted);
    }

    @Test
    void matchedSuccessEmitsAuthoritativeResultWithoutInventingImpactGeometry() {
        List<CastAudiovisualOrchestration.Directive> emitted = new ArrayList<>();
        var controller = controller(fullPolicy(), emitted);
        controller.recordLocalIntent(CAST_A, SPELL, 10L);

        var directive = controller.acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.SUCCESS), 12L).orElseThrow();

        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, directive.kind());
        assertEquals(CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT, directive.authority());
        assertEquals(SPELL, directive.spellId().orElseThrow());
        assertTrue(directive.authoritative());
        assertEquals(1.0D, directive.decorativeParticleDensity());
        assertTrue(directive.optionalMotionAllowed());
        assertTrue(directive.flashHeavyEffectsAllowed());
    }

    @Test
    void denialAndEffectFailureRemainDistinctAuthoritativeCueKinds() {
        var denied = controller(fullPolicy(), new ArrayList<>()).acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.DENIED_TARGET), 12L).orElseThrow();
        var failed = controller(fullPolicy(), new ArrayList<>()).acceptAuthoritativeResult(
                result(CAST_B, ArcanaCastResult.Status.EFFECT_FAILED), 12L).orElseThrow();

        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_DENIED, denied.kind());
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_FAILED, failed.kind());
        assertTrue(denied.authoritative());
        assertTrue(failed.authoritative());
    }

    @Test
    void unmatchedResultStaysGenericInsteadOfBorrowingCurrentSpellIdentity() {
        var controller = controller(fullPolicy(), new ArrayList<>());

        var directive = controller.acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.SUCCESS), 12L).orElseThrow();

        assertTrue(directive.spellId().isEmpty());
        assertEquals(CAST_A, directive.castId());
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, directive.kind());
    }

    @Test
    void duplicateIntentAndDuplicateSettlementDoNotEmitDuplicateDirectives() {
        List<CastAudiovisualOrchestration.Directive> emitted = new ArrayList<>();
        var controller = controller(fullPolicy(), emitted);
        var result = result(CAST_A, ArcanaCastResult.Status.SUCCESS);

        assertTrue(controller.recordLocalIntent(CAST_A, SPELL, 10L).isPresent());
        assertTrue(controller.recordLocalIntent(CAST_A, SPELL, 11L).isEmpty());
        assertTrue(controller.acceptAuthoritativeResult(result, 12L).isPresent());
        assertTrue(controller.acceptAuthoritativeResult(result, 20L).isEmpty());

        assertEquals(2, emitted.size());
        assertEquals(CastAudiovisualOrchestration.Kind.ANTICIPATION, emitted.get(0).kind());
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, emitted.get(1).kind());
    }

    @Test
    void accessibilityPolicyIsConsumedByDirectiveWithoutChangingOutcomeTruth() {
        var policy = new CastPresentationLifecycle.SensoryPolicy(0.0D, true, true);
        var controller = controller(policy, new ArrayList<>());
        controller.recordLocalIntent(CAST_A, SPELL, 10L);

        var directive = controller.acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.DENIED_COOLDOWN), 12L).orElseThrow();

        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_DENIED, directive.kind());
        assertTrue(directive.authoritative());
        assertEquals(0.0D, directive.decorativeParticleDensity());
        assertFalse(directive.optionalMotionAllowed());
        assertFalse(directive.flashHeavyEffectsAllowed());
    }

    @Test
    void staleEvictionAndClearKeepGenericLayerBounded() {
        var controller = new CastPresentationController(
                2,
                20L,
                CastAudiovisualOrchestrationTest::fullPolicy,
                directive -> { });
        controller.recordLocalIntent(CAST_A, SPELL, 1L);
        controller.acceptAuthoritativeResult(result(CAST_B, ArcanaCastResult.Status.SUCCESS), 2L);

        assertEquals(2, controller.size());
        controller.evictStale(23L);
        assertEquals(0, controller.size());

        controller.recordLocalIntent(CAST_A, SPELL, 30L);
        controller.clear();
        assertEquals(0, controller.size());
    }

    private static CastPresentationController controller(
            CastPresentationLifecycle.SensoryPolicy policy,
            List<CastAudiovisualOrchestration.Directive> emitted
    ) {
        return new CastPresentationController(8, 40L, () -> policy, emitted::add);
    }

    private static CastPresentationLifecycle.SensoryPolicy fullPolicy() {
        return new CastPresentationLifecycle.SensoryPolicy(1.0D, false, false);
    }

    private static CastResultPayload result(ArcanaCastId castId, ArcanaCastResult.Status status) {
        return new CastResultPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                status.name(),
                "test_code",
                "test detail");
    }
}
