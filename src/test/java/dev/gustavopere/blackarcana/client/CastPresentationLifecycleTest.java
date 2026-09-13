package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CastPresentationLifecycleTest {
    private static final ArcanaCastId CAST_A = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");
    private static final ArcanaCastId CAST_B = ArcanaCastId.parse("22222222-2222-2222-2222-222222222222");
    private static final ArcanaCastId CAST_C = ArcanaCastId.parse("33333333-3333-3333-3333-333333333333");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:test_spell");

    @Test
    void localIntentIsOnlyAnticipationAndNeverSelfPromotesToSuccess() {
        var lifecycle = new CastPresentationLifecycle(8, 40);

        var cue = lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);

        assertEquals(CastPresentationLifecycle.Authority.LOCAL_INTENT_PRESENTATION, cue.authority());
        assertEquals(CastPresentationLifecycle.State.ANTICIPATING, cue.state());
        assertEquals(SPELL, cue.spellId().orElseThrow());
        assertFalse(cue.authoritative());
        assertFalse(cue.settled());
    }

    @Test
    void matchingAuthoritativeSuccessSettlesTheSameCastCorrelation() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);

        var cue = lifecycle.acceptAuthoritativeResult(result(CAST_A, ArcanaCastResult.Status.SUCCESS), 12L);

        assertEquals(CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT, cue.authority());
        assertEquals(CastPresentationLifecycle.State.SUCCEEDED, cue.state());
        assertEquals(SPELL, cue.spellId().orElseThrow());
        assertTrue(cue.authoritative());
        assertTrue(cue.settled());
        assertEquals(12L, cue.updatedTick());
    }

    @Test
    void authoritativeDenialCancelsPendingAnticipation() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);

        var cue = lifecycle.acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.DENIED_COOLDOWN),
                11L);

        assertEquals(CastPresentationLifecycle.State.DENIED, cue.state());
        assertTrue(cue.authoritative());
        assertTrue(cue.settled());
    }

    @Test
    void effectFailureIsAuthoritativeButDistinctFromSuccessAndDenial() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);

        var cue = lifecycle.acceptAuthoritativeResult(
                result(CAST_A, ArcanaCastResult.Status.EFFECT_FAILED),
                11L);

        assertEquals(CastPresentationLifecycle.State.FAILED, cue.state());
        assertTrue(cue.authoritative());
        assertTrue(cue.settled());
    }

    @Test
    void unmatchedAuthoritativeResultRemainsGenericAndInventsNoSpellOrTarget() {
        var lifecycle = new CastPresentationLifecycle(8, 40);

        var cue = lifecycle.acceptAuthoritativeResult(result(CAST_A, ArcanaCastResult.Status.SUCCESS), 12L);

        assertEquals(CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT, cue.authority());
        assertEquals(CastPresentationLifecycle.State.SUCCEEDED, cue.state());
        assertTrue(cue.spellId().isEmpty());
        assertTrue(cue.authoritative());
        assertTrue(cue.settled());
    }

    @Test
    void duplicateAuthoritativeResultIsIdempotentAndDoesNotRefreshLifetime() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);
        var payload = result(CAST_A, ArcanaCastResult.Status.SUCCESS);

        var first = lifecycle.acceptAuthoritativeResult(payload, 12L);
        var duplicate = lifecycle.acceptAuthoritativeResult(payload, 20L);

        assertEquals(first, duplicate);
        assertEquals(12L, duplicate.updatedTick());
        assertEquals(1, lifecycle.size());
    }

    @Test
    void lifecycleEvictsStaleEntriesAndBoundsEntryCountDeterministically() {
        var lifecycle = new CastPresentationLifecycle(2, 20);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 1L);
        lifecycle.recordLocalIntent(CAST_B, SPELL, 2L);
        lifecycle.recordLocalIntent(CAST_C, SPELL, 3L);

        assertTrue(lifecycle.find(CAST_A).isEmpty());
        assertTrue(lifecycle.find(CAST_B).isPresent());
        assertTrue(lifecycle.find(CAST_C).isPresent());
        assertEquals(2, lifecycle.size());

        lifecycle.evictStale(24L);

        assertEquals(0, lifecycle.size());
    }

    @Test
    void clearTearsDownEveryEphemeralPresentationEntry() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        lifecycle.recordLocalIntent(CAST_A, SPELL, 10L);
        lifecycle.acceptAuthoritativeResult(result(CAST_B, ArcanaCastResult.Status.DENIED_TARGET), 11L);

        lifecycle.clear();

        assertEquals(0, lifecycle.size());
        assertTrue(lifecycle.find(CAST_A).isEmpty());
        assertTrue(lifecycle.find(CAST_B).isEmpty());
    }

    @Test
    void sensoryPolicyCanSuppressDecorationWithoutChangingLifecycleTruth() {
        var lifecycle = new CastPresentationLifecycle(8, 40);
        var cue = lifecycle.acceptAuthoritativeResult(result(CAST_A, ArcanaCastResult.Status.SUCCESS), 12L);
        var policy = new CastPresentationLifecycle.SensoryPolicy(0.0D, true, true);

        assertFalse(policy.decorativeParticlesEnabled());
        assertFalse(policy.nonessentialMotionAllowed());
        assertFalse(policy.flashHeavyEffectsAllowed());
        assertEquals(CastPresentationLifecycle.State.SUCCEEDED, cue.state());
        assertTrue(cue.authoritative());
    }

    @Test
    void sensoryPolicyRejectsParticleDensityOutsideClientConfigBounds() {
        assertThrows(
                IllegalArgumentException.class,
                () -> new CastPresentationLifecycle.SensoryPolicy(-0.01D, false, false));
        assertThrows(
                IllegalArgumentException.class,
                () -> new CastPresentationLifecycle.SensoryPolicy(1.01D, false, false));
    }

    @Test
    void authorityVocabularyMatchesThePlanningContract() {
        assertEquals(
                java.util.List.of(
                        "LOCAL_INTENT_PRESENTATION",
                        "SERVER_AUTHORED_FORECAST",
                        "AUTHORITATIVE_CAST_RESULT",
                        "SERVER_OWNED_RUNTIME_EVENT",
                        "CLIENT_DECORATIVE_EFFECT",
                        "PROVIDER_OWNED_PRESENTATION",
                        "UNKNOWN_OR_UNAVAILABLE"),
                java.util.Arrays.stream(CastPresentationLifecycle.Authority.values()).map(Enum::name).toList());
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
