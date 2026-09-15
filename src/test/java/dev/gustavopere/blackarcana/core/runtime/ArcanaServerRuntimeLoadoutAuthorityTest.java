package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcanaServerRuntimeLoadoutAuthorityTest {
    private static final UUID CASTER = UUID.fromString("0de576d5-6b02-4c5f-bc2e-44e9663b9caf");
    private static final ArcanaSpellId EQUIPPED = ArcanaSpellId.parse("black_arcana:equipped_spell");
    private static final ArcanaSpellId FORGED = ArcanaSpellId.parse("black_arcana:forged_spell");

    @Test
    void immediateCastCannotBypassServerOwnedLoadoutSlot() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(4, 32);
        runtime.spells().replaceAll(List.of(spell(EQUIPPED), spell(FORGED)));
        runtime.loadouts().setLoadout(CASTER, List.of(EQUIPPED));

        AtomicInteger effects = new AtomicInteger();
        runtime.installEngine(FORGED, permissiveEngine(runtime, effects));

        var result = runtime.handle(
                new ArcanaCastContext(CASTER, 10L, "minecraft:overworld"),
                new CastIntentPayload(
                        ArcanaProtocol.VERSION,
                        "00000000-0000-0000-0000-000000000051",
                        FORGED.canonical(),
                        0,
                        ""));

        assertEquals("DENIED_IDENTITY", result.status());
        assertEquals("loadout_spell_mismatch", result.code());
        assertEquals(0, effects.get(), "loadout denial must happen before spell execution");
    }

    private static ArcanaSpellDefinition spell(ArcanaSpellId id) {
        return new ArcanaSpellDefinition(
                id,
                "spell." + id.namespace() + "." + id.path(),
                id.canonical(),
                ArcanaCost.none(),
                false);
    }

    private static ArcanaCastEngine permissiveEngine(ArcanaServerRuntime runtime, AtomicInteger effects) {
        return new ArcanaCastEngine(
                runtime.spells(),
                request -> ArcanaDecision.allow(),
                request -> ArcanaDecision.allow(),
                new ArcanaServices.CooldownService() {
                    @Override
                    public ArcanaDecision check(ArcanaCastRequest request) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public void start(ArcanaCastRequest request) { }
                },
                request -> ArcanaServices.TargetResolution.resolved("server-target"),
                new ArcanaServices.CostProvider() {
                    @Override
                    public ArcanaDecision check(ArcanaCastRequest request) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
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
                },
                (request, target) -> ArcanaDecision.allow(),
                (request, target) -> {
                    effects.incrementAndGet();
                    return ArcanaServices.EffectResult.ok();
                });
    }
}
