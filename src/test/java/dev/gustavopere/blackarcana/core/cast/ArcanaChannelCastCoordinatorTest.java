package dev.gustavopere.blackarcana.core.cast;

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
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaChannelCastCoordinatorTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:channel_probe"),
            "spell.black_arcana.channel_probe",
            "black_arcana:channel_probe",
            new ArcanaCost("black_arcana:test", 1.0),
            false);

    @Test
    void releaseExecutesCanonicalEngineExactlyOnceWithServerOwnedDuration() {
        ArcanaServerRuntime runtime = runtimeWithChannelProbe();
        ArcanaCastId castId = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");
        AtomicInteger effects = new AtomicInteger();
        AtomicLong observedChannelTicks = new AtomicLong(-1L);
        installProbeEngine(runtime, effects, observedChannelTicks);

        CastIntentPayload begin = new CastIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                SPELL.id().canonical(),
                0,
                "");

        assertTrue(runtime.beginChannel(context(100), begin, new ArcanaChannelSpec(10, 40)).allowed());

        ArcanaCastResult released = runtime.releaseChannel(context(112), castId, "");
        assertEquals(ArcanaCastResult.Status.SUCCESS, released.status());
        assertEquals(1, effects.get());
        assertEquals(12L, observedChannelTicks.get());

        ArcanaCastResult duplicateRelease = runtime.releaseChannel(context(113), castId, "");
        assertEquals(ArcanaCastResult.Status.DENIED_CHANNEL, duplicateRelease.status());
        assertEquals("channel_missing", duplicateRelease.code());
        assertEquals(1, effects.get());
    }

    @Test
    void releaseRevalidatesCurrentServerOwnedLoadout() {
        ArcanaServerRuntime runtime = runtimeWithChannelProbe();
        ArcanaCastId castId = ArcanaCastId.parse("22222222-2222-2222-2222-222222222222");
        AtomicInteger effects = new AtomicInteger();
        installProbeEngine(runtime, effects, new AtomicLong());

        CastIntentPayload begin = new CastIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                SPELL.id().canonical(),
                0,
                "");
        assertTrue(runtime.beginChannel(context(200), begin, new ArcanaChannelSpec(5, 40)).allowed());

        runtime.loadouts().setLoadout(CASTER, List.of(ArcanaSpellId.parse("black_arcana:replacement")));
        ArcanaCastResult released = runtime.releaseChannel(context(210), castId, "");

        assertEquals(ArcanaCastResult.Status.DENIED_IDENTITY, released.status());
        assertEquals("loadout_spell_mismatch", released.code());
        assertEquals(0, effects.get());
    }

    private static ArcanaServerRuntime runtimeWithChannelProbe() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(12, 32, 32);
        runtime.spells().replaceAll(List.of(SPELL));
        runtime.loadouts().setLoadout(CASTER, List.of(SPELL.id()));
        return runtime;
    }

    private static void installProbeEngine(
            ArcanaServerRuntime runtime,
            AtomicInteger effects,
            AtomicLong observedChannelTicks
    ) {
        ArcanaServices.CostProvider cost = new ArcanaServices.CostProvider() {
            @Override
            public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) {
                return ArcanaDecision.allow();
            }

            @Override
            public ArcanaServices.CostReservation reserve(dev.gustavopere.blackarcana.api.ArcanaCastRequest request) {
                return new ArcanaServices.CostReservation() {
                    @Override
                    public ArcanaDecision decision() {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public void commit() { }

                    @Override
                    public void refund() { }
                };
            }
        };

        ArcanaCastEngine engine = new ArcanaCastEngine(
                new CompositeCastRequestValidator(List.of(runtime.spells(), runtime.loadouts())),
                new BoundedReplayGuard(32, 100L),
                request -> ArcanaDecision.allow(),
                runtime.cooldowns(),
                request -> ArcanaServices.TargetResolution.resolved("self"),
                cost,
                (request, target) -> ArcanaDecision.allow(),
                (request, target) -> {
                    effects.incrementAndGet();
                    observedChannelTicks.set(request.channelTicks());
                    return ArcanaServices.EffectResult.ok();
                });
        runtime.installEngine(SPELL.id(), engine);
    }

    private static ArcanaCastContext context(long tick) {
        return new ArcanaCastContext(CASTER, tick, "minecraft:overworld");
    }
}
