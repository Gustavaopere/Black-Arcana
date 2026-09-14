package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaTargetReference;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceCastBindingTest {
    @Test
    void profileRejectsWrongIdentityWorldMutationAndSafetyCeilingOverflow() {
        ArcanaCooldownSpec cooldown = new ArcanaCooldownSpec("black_arcana:astral_severance", 40L, false);
        ArcanaChannelSpec channel = new ArcanaChannelSpec(1L, 20L);

        assertThrows(IllegalArgumentException.class, () -> new AstralSeveranceCastBinding.Profile(
            definition(ArcanaSpellId.parse("black_arcana:not_astral"), false), cooldown, channel, 20, 16.0D));
        assertThrows(IllegalArgumentException.class, () -> new AstralSeveranceCastBinding.Profile(
            definition(AstralSeveranceCastBinding.SPELL_ID, true), cooldown, channel, 20, 16.0D));
        assertThrows(IllegalArgumentException.class, () -> new AstralSeveranceCastBinding.Profile(
            definition(AstralSeveranceCastBinding.SPELL_ID, false), cooldown, channel,
            NoeticSafetyCeilings.MAX_DURATION_TICKS + 1, 16.0D));
        assertThrows(IllegalArgumentException.class, () -> new AstralSeveranceCastBinding.Profile(
            definition(AstralSeveranceCastBinding.SPELL_ID, false), cooldown, channel,
            20, NoeticSafetyCeilings.MAX_RANGE_BLOCKS + 0.001D));
    }

    @Test
    void resourceAuthorityMismatchFailsBeforeRuntimeMutation() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralSeveranceCastBinding.Profile profile = profile();
        FakeResourceAuthority wrongResource = new FakeResourceAuthority("irons_spellbooks:mana");

        assertThrows(IllegalArgumentException.class, () -> AstralSeveranceCastBinding.install(
            runtime,
            profile,
            new AstralSeveranceCastBinding.Authorities(
                wrongResource,
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop()),
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow()));

        assertTrue(runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertFalse(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
        assertTrue(runtime.cooldownPolicies().cooldownSnapshot().get(AstralSeveranceCastBinding.SPELL_ID) == null);
    }

    @Test
    void installRegistersOnlyExplicitProfileAndExposesChannelContract() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralSeveranceCastBinding.Profile profile = profile();
        FakeResourceAuthority resource = new FakeResourceAuthority(profile.definition().cost().resourceId());

        AstralSeveranceCastBinding.Installed installed = AstralSeveranceCastBinding.install(
            runtime,
            profile,
            new AstralSeveranceCastBinding.Authorities(
                resource,
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop()),
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertEquals(AstralSeveranceCastBinding.SPELL_ID, installed.spellId());
        assertEquals(profile.channelSpec(), installed.channelSpec());
        assertEquals(profile.definition(), runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
        assertEquals(profile.cooldown(), runtime.cooldownPolicies().cooldownSnapshot().get(AstralSeveranceCastBinding.SPELL_ID));
        assertTrue(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
    }

    @Test
    void immediateIngressCannotBypassConfiguredChannelMinimum() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralSeveranceCastBinding.Profile profile = profile();
        runtime.spells().replaceAll(java.util.List.of(profile.definition()));
        runtime.cooldownPolicies().replaceAll(
            java.util.Map.of(AstralSeveranceCastBinding.SPELL_ID, profile.cooldown()),
            java.util.Map.of());

        FakeResourceAuthority resource = new FakeResourceAuthority(profile.definition().cost().resourceId());
        AtomicInteger activations = new AtomicInteger();
        ArcanaCastEngine engine = AstralSeveranceCastBinding.buildEngine(
            runtime,
            profile,
            new AstralSeveranceCastBinding.Authorities(
                resource,
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop()),
            (casterId, durationTicks, maxRangeBlocks) -> {
                activations.incrementAndGet();
                return ArcanaDecision.allow();
            });

        ArcanaCastResult result = engine.execute(request(profile, UUID.randomUUID(), 90L, 0L));

        assertEquals(ArcanaCastResult.Status.DENIED_CHANNEL, result.status());
        assertEquals("channel_too_short", result.code());
        assertEquals(0, activations.get());
        assertEquals(0, resource.reserveCalls.get());
    }

    @Test
    void engineRunsProjectionOnlyAfterCanonicalGatesAndCommitsResourceOnSuccess() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralSeveranceCastBinding.Profile profile = profile();
        runtime.spells().replaceAll(java.util.List.of(profile.definition()));
        runtime.cooldownPolicies().replaceAll(
            java.util.Map.of(AstralSeveranceCastBinding.SPELL_ID, profile.cooldown()),
            java.util.Map.of());

        FakeResourceAuthority resource = new FakeResourceAuthority(profile.definition().cost().resourceId());
        AtomicBoolean progressionAllowed = new AtomicBoolean(false);
        AtomicInteger activations = new AtomicInteger();
        AtomicReference<String> observedTarget = new AtomicReference<>();
        AstralSeveranceCastBinding.Authorities authorities = new AstralSeveranceCastBinding.Authorities(
            resource,
            request -> progressionAllowed.get()
                ? ArcanaDecision.allow()
                : ArcanaDecision.deny("progression", "blocked"),
            request -> ArcanaDecision.allow(),
            (request, target, effectResult) -> observedTarget.set(target.targetId()));
        ArcanaCastEngine engine = AstralSeveranceCastBinding.buildEngine(
            runtime,
            profile,
            authorities,
            (casterId, durationTicks, maxRangeBlocks) -> {
                activations.incrementAndGet();
                assertEquals(profile.projectionDurationTicks(), durationTicks);
                assertEquals(profile.maxRangeBlocks(), maxRangeBlocks);
                return ArcanaDecision.allow();
            });

        UUID casterId = UUID.randomUUID();
        ArcanaCastResult deniedResult = engine.execute(request(
            profile, casterId, 100L, profile.channelSpec().minimumTicks()));
        assertEquals(ArcanaCastResult.Status.DENIED_PROGRESSION, deniedResult.status());
        assertEquals(0, activations.get());
        assertEquals(0, resource.reserveCalls.get());

        progressionAllowed.set(true);
        ArcanaCastResult acceptedResult = engine.execute(request(
            profile, casterId, 101L, profile.channelSpec().minimumTicks()));
        assertEquals(ArcanaCastResult.Status.SUCCESS, acceptedResult.status());
        assertEquals(1, activations.get());
        assertEquals(1, resource.reserveCalls.get());
        assertEquals(1, resource.commitCalls.get());
        assertEquals(0, resource.refundCalls.get());
        assertEquals(new ArcanaTargetReference.EntityRef(casterId).canonical(), observedTarget.get());
    }

    @Test
    void failedProjectionActivationRefundsResourceAndDoesNotStartCooldown() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        AstralSeveranceCastBinding.Profile profile = profile();
        runtime.spells().replaceAll(java.util.List.of(profile.definition()));
        runtime.cooldownPolicies().replaceAll(
            java.util.Map.of(AstralSeveranceCastBinding.SPELL_ID, profile.cooldown()),
            java.util.Map.of());
        FakeResourceAuthority resource = new FakeResourceAuthority(profile.definition().cost().resourceId());
        AstralSeveranceCastBinding.Authorities authorities = new AstralSeveranceCastBinding.Authorities(
            resource,
            request -> ArcanaDecision.allow(),
            request -> ArcanaDecision.allow(),
            ArcanaServices.CastSuccessObserver.noop());
        ArcanaCastEngine engine = AstralSeveranceCastBinding.buildEngine(
            runtime,
            profile,
            authorities,
            (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.deny("astral_viewer_active", "active"));

        UUID casterId = UUID.randomUUID();
        ArcanaCastRequest request = request(profile, casterId, 200L, profile.channelSpec().minimumTicks());
        ArcanaCastResult result = engine.execute(request);

        assertEquals(ArcanaCastResult.Status.EFFECT_FAILED, result.status());
        assertEquals(0, resource.commitCalls.get());
        assertEquals(1, resource.refundCalls.get());
        ArcanaCastRequest retry = request(profile, casterId, 200L, profile.channelSpec().minimumTicks());
        assertTrue(runtime.cooldowns().check(retry).allowed(), "failed activation must not start cooldown");
    }

    private static ArcanaCastRequest request(
        AstralSeveranceCastBinding.Profile profile,
        UUID casterId,
        long serverTick,
        long channelTicks
    ) {
        return new ArcanaCastRequest(
            ArcanaCastId.random(),
            profile.definition(),
            new ArcanaCastContext(casterId, serverTick, "minecraft:overworld"),
            0,
            "",
            channelTicks);
    }

    private static AstralSeveranceCastBinding.Profile profile() {
        return new AstralSeveranceCastBinding.Profile(
            definition(AstralSeveranceCastBinding.SPELL_ID, false),
            new ArcanaCooldownSpec("black_arcana:astral_severance", 40L, false),
            new ArcanaChannelSpec(1L, 20L),
            200,
            24.0D);
    }

    private static ArcanaSpellDefinition definition(ArcanaSpellId id, boolean worldMutation) {
        return new ArcanaSpellDefinition(
            id,
            "spell.black_arcana.astral_severance",
            "black_arcana:textures/gui/spell_icons/astral_severance.png",
            new ArcanaCost("black_arcana:test_resource", 3.0D),
            worldMutation);
    }

    private static final class FakeResourceAuthority implements AstralSeveranceCastBinding.ResourceAuthority {
        private final String resourceId;
        private final AtomicInteger reserveCalls = new AtomicInteger();
        private final AtomicInteger commitCalls = new AtomicInteger();
        private final AtomicInteger refundCalls = new AtomicInteger();

        private FakeResourceAuthority(String resourceId) {
            this.resourceId = resourceId;
        }

        @Override
        public String resourceId() {
            return resourceId;
        }

        @Override
        public ArcanaDecision check(ArcanaCastRequest request) {
            return ArcanaDecision.allow();
        }

        @Override
        public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
            reserveCalls.incrementAndGet();
            return new ArcanaServices.CostReservation() {
                @Override
                public ArcanaDecision decision() {
                    return ArcanaDecision.allow();
                }

                @Override
                public void commit() {
                    commitCalls.incrementAndGet();
                }

                @Override
                public void refund() {
                    refundCalls.incrementAndGet();
                }
            };
        }
    }
}
