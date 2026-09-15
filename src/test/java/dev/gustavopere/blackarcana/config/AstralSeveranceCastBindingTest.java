package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
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
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
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
        assertTrue(runtime.spells().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertTrue(runtime.channelSpecs().resolve(AstralSeveranceCastBinding.SPELL_ID).isEmpty());
        assertFalse(runtime.hasInstalledEngine(AstralSeveranceCastBinding.SPELL_ID));
        assertFalse(runtime.cooldownPolicies().cooldownSnapshot().containsKey(AstralSeveranceCastBinding.SPELL_ID));
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
        ArcanaCastId castId = ArcanaCastId.random();
        long beginTick = 100L;
        ArcanaDecision begin = runtime.beginChannel(
                new ArcanaCastContext(casterId, beginTick, "minecraft:overworld"),
                new ChannelBeginIntentPayload(
                        ArcanaProtocol.VERSION,
                        castId.canonical(),
                        AstralSeveranceCastBinding.SPELL_ID.canonical(),
                        0));
        assertTrue(begin.allowed());

        long releaseTick = beginTick + invocation.channelSpec().minimumTicks();
        ArcanaCastResult result = runtime.releaseChannel(
                new ArcanaCastContext(casterId, releaseTick, "minecraft:overworld"),
                castId,
                "");

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
