package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.BoundedReplayGuard;
import dev.gustavopere.blackarcana.core.cast.CompositeCastRequestValidator;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeChannelAuthorityTest {
    private static final UUID CASTER = UUID.fromString("7ea535b1-a2af-4f80-83ab-d7ed3aa8169a");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:channel_authority_probe"),
            "spell.black_arcana.channel_authority_probe",
            "black_arcana:channel_authority_probe",
            new ArcanaCost("black_arcana:test", 1.0),
            false);

    @Test
    void beginIntentResolvesOnlyExplicitServerOwnedChannelSpec() {
        ArcanaServerRuntime runtime = runtime();
        ArcanaCastId first = ArcanaCastId.random();
        ChannelBeginIntentPayload begin = new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                first.canonical(),
                SPELL.id().canonical(),
                0);

        ArcanaDecision missing = runtime.beginChannel(context(100L), begin);
        assertEquals("channel_not_configured", missing.code());
        assertEquals(0, runtime.channels().activeSessions());

        assertTrue(runtime.channelSpecs().register(SPELL.id(), new ArcanaChannelSpec(5L, 40L)));
        ArcanaDecision accepted = runtime.beginChannel(context(101L), begin);
        assertTrue(accepted.allowed());
        assertEquals(1, runtime.channels().activeSessions());
    }

    @Test
    void physicalReleaseIsTerminalEvenWhenMinimumChannelWasNotReached() {
        ArcanaServerRuntime runtime = runtime();
        assertTrue(runtime.channelSpecs().register(SPELL.id(), new ArcanaChannelSpec(5L, 40L)));
        ArcanaCastId first = ArcanaCastId.random();
        assertTrue(runtime.beginChannel(context(100L), new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                first.canonical(),
                SPELL.id().canonical(),
                0)).allowed());

        ArcanaCastResult tooShort = runtime.releaseChannel(context(102L), new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                first.canonical(),
                ""));
        assertEquals(ArcanaCastResult.Status.DENIED_CHANNEL, tooShort.status());
        assertEquals("channel_too_short", tooShort.code());
        assertEquals(0, runtime.channels().activeSessions(),
                "physical key release must not leave a denied channel blocking the caster until timeout");

        ArcanaCastId second = ArcanaCastId.random();
        assertTrue(runtime.beginChannel(context(103L), new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                second.canonical(),
                SPELL.id().canonical(),
                0)).allowed());
        assertTrue(runtime.cancelChannel(context(104L), new ChannelCancelIntentPayload(
                ArcanaProtocol.VERSION,
                second.canonical())));
        assertEquals(0, runtime.channels().activeSessions());
    }

    private static ArcanaServerRuntime runtime() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(12, 32, 32);
        runtime.spells().replaceAll(List.of(SPELL));
        runtime.loadouts().setLoadout(CASTER, List.of(SPELL.id()));
        ArcanaServices.CostProvider cost = new ArcanaServices.CostProvider() {
            @Override
            public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) {
                return ArcanaDecision.allow();
            }

            @Override
            public ArcanaServices.CostReservation reserve(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) {
                return new ArcanaServices.CostReservation() {
                    @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    @Override public void commit() { }
                    @Override public void refund() { }
                };
            }
        };
        runtime.installEngine(SPELL.id(), new ArcanaCastEngine(
                new CompositeCastRequestValidator(List.of(runtime.spells(), runtime.loadouts())),
                new BoundedReplayGuard(32, 100L),
                request -> ArcanaDecision.allow(),
                runtime.cooldowns(),
                request -> ArcanaServices.TargetResolution.resolved("self"),
                cost,
                (request, target) -> ArcanaDecision.allow(),
                (request, target) -> ArcanaServices.EffectResult.ok()));
        return runtime;
    }

    private static ArcanaCastContext context(long tick) {
        return new ArcanaCastContext(CASTER, tick, "minecraft:overworld");
    }
}
