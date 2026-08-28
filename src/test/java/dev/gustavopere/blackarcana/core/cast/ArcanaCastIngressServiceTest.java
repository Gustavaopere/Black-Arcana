package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaCastIngressServiceTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:ingress_test");

    private static ArcanaSpellDefinition spell() {
        return new ArcanaSpellDefinition(
                SPELL_ID,
                "spell.black_arcana.ingress_test",
                "black_arcana:ingress_test",
                ArcanaCost.none(),
                false);
    }

    private static CastIntentPayload intent(String spellId) {
        return new CastIntentPayload(
                ArcanaProtocol.VERSION,
                "00000000-0000-0000-0000-000000000001",
                spellId,
                0,
                "advisory-only");
    }

    private static ArcanaCastContext context(long tick) {
        return new ArcanaCastContext(CASTER, tick, "minecraft:overworld");
    }

    @Test
    void unknownSpellIsRejectedBeforeEngineResolution() {
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        ArcanaCastIngressService ingress = new ArcanaCastIngressService(
                registry,
                new IngressRateLimiter(4, 20L, 32),
                id -> { throw new AssertionError("engine resolution must not run"); });

        var result = ingress.handle(context(10L), intent("black_arcana:missing"));
        assertEquals("DENIED_IDENTITY", result.status());
        assertEquals("unknown_spell", result.code());
    }

    @Test
    void canonicalServerDefinitionIsUsedForExecution() {
        ArcanaSpellDefinition definition = spell();
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        registry.replaceAll(List.of(definition));
        AtomicReference<ArcanaSpellDefinition> observed = new AtomicReference<>();

        ArcanaCastEngine engine = new ArcanaCastEngine(
                req -> ArcanaDecision.allow(),
                req -> ArcanaDecision.allow(),
                req -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public void start(dev.gustavopere.blackarcana.api.ArcanaCastRequest req) { }
                },
                req -> {
                    observed.set(req.spell());
                    return ArcanaServices.TargetResolution.resolved("server-target");
                },
                new ArcanaServices.CostProvider() {
                    public ArcanaDecision check(dev.gustavopere.blackarcana.api.ArcanaCastRequest req) { return ArcanaDecision.allow(); }
                    public ArcanaServices.CostReservation reserve(dev.gustavopere.blackarcana.api.ArcanaCastRequest req) {
                        return new ArcanaServices.CostReservation() {
                            public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                            public void commit() { }
                            public void refund() { }
                        };
                    }
                },
                (req, target) -> ArcanaDecision.allow(),
                (req, target) -> ArcanaServices.EffectResult.ok());

        ArcanaCastIngressService ingress = new ArcanaCastIngressService(
                registry,
                new IngressRateLimiter(4, 20L, 32),
                id -> id.equals(SPELL_ID) ? engine : null);

        var result = ingress.handle(context(10L), intent(SPELL_ID.canonical()));
        assertEquals("SUCCESS", result.status());
        assertNotNull(observed.get());
        assertEquals(definition, observed.get());
    }

    @Test
    void rateLimitFailsBeforeSpellExecution() {
        ArcanaSpellRegistry registry = new ArcanaSpellRegistry();
        registry.replaceAll(List.of(spell()));
        AtomicInteger engineResolutions = new AtomicInteger();
        ArcanaCastIngressService ingress = new ArcanaCastIngressService(
                registry,
                new IngressRateLimiter(1, 20L, 32),
                id -> {
                    engineResolutions.incrementAndGet();
                    return null;
                });

        // First request consumes the ingress bucket and reaches runtime resolution once.
        var first = ingress.handle(context(10L), intent(SPELL_ID.canonical()));
        assertEquals("DENIED_IDENTITY", first.status());
        assertEquals("spell_runtime_unavailable", first.code());
        assertEquals(1, engineResolutions.get());

        var second = ingress.handle(context(11L), new CastIntentPayload(
                ArcanaProtocol.VERSION,
                "00000000-0000-0000-0000-000000000002",
                SPELL_ID.canonical(), 0, ""));
        assertEquals("DENIED_INGRESS", second.status());
        assertEquals("rate_limited", second.code());
        assertEquals(1, engineResolutions.get(), "rate-limited request must fail before engine resolution");
    }
}
