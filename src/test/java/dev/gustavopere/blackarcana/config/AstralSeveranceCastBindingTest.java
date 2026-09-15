package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.AstralSeveranceCastBinding;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceCastBindingTest {
    private static final String RESOURCE_ID = "test_provider:mana";

    @AfterEach
    void clearInvocationAuthority() {
        AstralInvocationConfigAuthority.reload(List.of());
    }

    @Test
    void missingInvocationAuthorityFailsClosedWithoutRuntimeMutation() {
        AstralInvocationConfigAuthority.reload(List.of());
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        AstralSeveranceCastBinding.Resolution resolution = AstralSeveranceCastBinding.install(
                runtime,
                definition(new ArcanaCost(RESOURCE_ID, 3.0D)),
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertFalse(resolution.decision().allowed());
        assertEquals("astral_invocation_not_configured", resolution.decision().code());
        assertTrue(resolution.installed().isEmpty());
        assertNoAstralRuntimeMutation(runtime);
    }

    @Test
    void missingConfiguredResourceProviderFailsClosedWithoutRuntimeMutation() {
        AstralInvocationDataDefinition.Invocation invocation = publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        AstralSeveranceCastBinding.Resolution resolution = AstralSeveranceCastBinding.install(
                runtime,
                definition(invocation.cost()),
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertFalse(resolution.decision().allowed());
        assertEquals("astral_resource_provider_missing", resolution.decision().code());
        assertTrue(resolution.installed().isEmpty());
        assertNoAstralRuntimeMutation(runtime);
    }

    @Test
    void resolvedInvocationInstallsExactProviderCooldownChannelAndCanonicalEngine() {
        AstralInvocationDataDefinition.Invocation invocation = publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeResourceProvider resource = new FakeResourceProvider(RESOURCE_ID);
        runtime.resourceCosts().register(resource);
        ArcanaSpellDefinition definition = definition(invocation.cost());

        AstralSeveranceCastBinding.Resolution resolution = AstralSeveranceCastBinding.install(
                runtime,
                definition,
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertTrue(resolution.decision().allowed());
        AstralSeveranceCastBinding.Installed installed = resolution.installed().orElseThrow();
        assertEquals(AstralSeveranceCastBinding.SPELL_ID, installed.spellId());
        assertEquals(RESOURCE_ID, installed.resourceId());
        assertEquals(invocation.channelSpec(), installed.channelSpec());
        assertEquals(definition, runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
        assertEquals(invocation.cooldown(), runtime.cooldownPolicies().cooldownSnapshot().get(AstralSeveranceCastBinding.SPELL_ID));
        assertEquals(invocation.channelSpec(), runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
        assertTrue(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
    }

    @Test
    void channelAuthorityConflictFailsClosedBeforePublishingSpellCooldownOrEngine() {
        AstralInvocationDataDefinition.Invocation invocation = publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.resourceCosts().register(new FakeResourceProvider(RESOURCE_ID));
        ArcanaChannelSpec existing = new ArcanaChannelSpec(2L, 9L);
        assertTrue(runtime.channelSpecs().register(AstralSeveranceCastBinding.SPELL_ID, existing));

        AstralSeveranceCastBinding.Resolution resolution = AstralSeveranceCastBinding.install(
                runtime,
                definition(invocation.cost()),
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow());

        assertFalse(resolution.decision().allowed());
        assertEquals("astral_channel_conflict", resolution.decision().code());
        assertEquals(existing, runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).orElseThrow());
        assertTrue(runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertFalse(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
        assertFalse(runtime.cooldownPolicies().cooldownSnapshot().containsKey(AstralSeveranceCastBinding.SPELL_ID));
    }

    @Test
    void definitionCostCannotOverrideResolvedInvocationAuthority() {
        publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.resourceCosts().register(new FakeResourceProvider(RESOURCE_ID));

        assertThrows(IllegalArgumentException.class, () -> AstralSeveranceCastBinding.install(
                runtime,
                definition(new ArcanaCost(RESOURCE_ID, 4.0D)),
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) -> ArcanaDecision.allow()));

        assertNoAstralRuntimeMutation(runtime);
    }

    @Test
    void progressionGatePrecedesResolvedResourceAndSuccessfulReleaseCommitsIt() {
        AstralInvocationDataDefinition.Invocation invocation = publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeResourceProvider resource = new FakeResourceProvider(RESOURCE_ID);
        runtime.resourceCosts().register(resource);
        ArcanaSpellDefinition definition = definition(invocation.cost());
        AtomicBoolean progressionAllowed = new AtomicBoolean(false);
        AtomicInteger activations = new AtomicInteger();
        AstralSeveranceCastBinding.Authorities authorities = new AstralSeveranceCastBinding.Authorities(
                request -> progressionAllowed.get()
                        ? ArcanaDecision.allow()
                        : ArcanaDecision.deny("astral_progression", "blocked"),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop());
        AstralSeveranceCastBinding.install(
                runtime,
                definition,
                authorities,
                (casterId, durationTicks, maxRangeBlocks) -> {
                    activations.incrementAndGet();
                    assertEquals(invocation.projectionDurationTicks(), durationTicks);
                    assertEquals(invocation.maxRangeBlocks(), maxRangeBlocks);
                    return ArcanaDecision.allow();
                });

        UUID casterId = UUID.randomUUID();
        runtime.loadouts().setLoadout(casterId, List.of(AstralSeveranceCastBinding.SPELL_ID));
        ArcanaCastResult denied = channelAndRelease(runtime, invocation, casterId, 100L);
        assertEquals(ArcanaCastResult.Status.DENIED_PROGRESSION, denied.status());
        assertEquals(0, resource.reserveCalls.get());
        assertEquals(0, activations.get());

        progressionAllowed.set(true);
        ArcanaCastResult accepted = channelAndRelease(runtime, invocation, casterId, 110L);
        assertEquals(ArcanaCastResult.Status.SUCCESS, accepted.status());
        assertEquals(1, resource.reserveCalls.get());
        assertEquals(1, resource.commitCalls.get());
        assertEquals(0, resource.refundCalls.get());
        assertEquals(1, activations.get());
    }

    @Test
    void projectionFailureRefundsResolvedProviderAndDoesNotStartCooldown() {
        AstralInvocationDataDefinition.Invocation invocation = publishInvocation();
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        FakeResourceProvider resource = new FakeResourceProvider(RESOURCE_ID);
        runtime.resourceCosts().register(resource);
        ArcanaSpellDefinition definition = definition(invocation.cost());
        AstralSeveranceCastBinding.install(
                runtime,
                definition,
                allowAuthorities(),
                (casterId, durationTicks, maxRangeBlocks) ->
                        ArcanaDecision.deny("astral_viewer_active", "projection already active"));

        UUID casterId = UUID.randomUUID();
        runtime.loadouts().setLoadout(casterId, List.of(AstralSeveranceCastBinding.SPELL_ID));
        long releaseTick = 100L + invocation.channelSpec().minimumTicks();
        ArcanaCastResult result = channelAndRelease(runtime, invocation, casterId, 100L);

        assertEquals(ArcanaCastResult.Status.EFFECT_FAILED, result.status());
        assertEquals(1, resource.reserveCalls.get());
        assertEquals(0, resource.commitCalls.get());
        assertEquals(1, resource.refundCalls.get());
        ArcanaCastRequest retry = new ArcanaCastRequest(
                ArcanaCastId.random(),
                definition,
                new ArcanaCastContext(casterId, releaseTick, "minecraft:overworld"),
                0,
                "",
                invocation.channelSpec().minimumTicks());
        assertTrue(runtime.cooldowns().check(retry).allowed(), "failed activation must not start cooldown");
    }

    private static ArcanaCastResult channelAndRelease(
            ArcanaServerRuntime runtime,
            AstralInvocationDataDefinition.Invocation invocation,
            UUID casterId,
            long beginTick
    ) {
        ArcanaCastId castId = ArcanaCastId.random();
        ArcanaDecision begin = runtime.beginChannel(
                new ArcanaCastContext(casterId, beginTick, "minecraft:overworld"),
                new ChannelBeginIntentPayload(
                        ArcanaProtocol.VERSION,
                        castId.canonical(),
                        AstralSeveranceCastBinding.SPELL_ID.canonical(),
                        0));
        assertTrue(begin.allowed());
        return runtime.releaseChannel(
                new ArcanaCastContext(
                        casterId,
                        beginTick + invocation.channelSpec().minimumTicks(),
                        "minecraft:overworld"),
                castId,
                "");
    }

    private static AstralInvocationDataDefinition.Invocation publishInvocation() {
        AstralInvocationDataDefinition definition = new AstralInvocationDataDefinition(
                AstralInvocationDataDefinition.CURRENT_SCHEMA_VERSION,
                AstralInvocationDataDefinition.ASTRAL_SEVERANCE_ID,
                ConfigScope.SERVER,
                RESOURCE_ID,
                3.0D,
                ArcanaCost.Unit.FLAT,
                "black_arcana:astral_severance",
                40L,
                false,
                5L,
                20L,
                200,
                24.0D);
        AstralInvocationConfigAuthority.reload(List.of(definition));
        return AstralInvocationConfigAuthority.current().orElseThrow();
    }

    private static ArcanaSpellDefinition definition(ArcanaCost cost) {
        return new ArcanaSpellDefinition(
                AstralSeveranceCastBinding.SPELL_ID,
                "spell.black_arcana.astral_severance",
                "black_arcana:astral_severance",
                cost,
                false);
    }

    private static AstralSeveranceCastBinding.Authorities allowAuthorities() {
        return new AstralSeveranceCastBinding.Authorities(
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                ArcanaServices.CastSuccessObserver.noop());
    }

    private static void assertNoAstralRuntimeMutation(ArcanaServerRuntime runtime) {
        assertTrue(runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertTrue(runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertFalse(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
        assertFalse(runtime.cooldownPolicies().cooldownSnapshot().containsKey(AstralSeveranceCastBinding.SPELL_ID));
    }

    private static final class FakeResourceProvider implements ResourceCostProvider {
        private final String resourceId;
        private final AtomicInteger reserveCalls = new AtomicInteger();
        private final AtomicInteger commitCalls = new AtomicInteger();
        private final AtomicInteger refundCalls = new AtomicInteger();

        private FakeResourceProvider(String resourceId) {
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
