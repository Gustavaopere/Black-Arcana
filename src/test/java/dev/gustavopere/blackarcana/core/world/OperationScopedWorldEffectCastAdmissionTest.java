package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class OperationScopedWorldEffectCastAdmissionTest {
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:operation_scoped_probe");

    @Test
    void operationScopedProfilePreservesLegacyDenialButAllowsCastToReachRuntimeFallback() {
        WorldEffectProfileRegistry profiles = new WorldEffectProfileRegistry();
        profiles.register(SPELL_ID, new WorldEffectProfile(
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.PERMANENT,
            8,
            true,
            true));
        ConfigurableWorldEffectPolicy policy = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(WorldEffectMode.OFF, 8, true, Map.of()));
        ArcanaCastRequest request = request();
        ArcanaServices.TargetResolution target = ArcanaServices.TargetResolution.resolved("target");

        ArcanaDecision legacy = policy.authorize(request, target);
        assertFalse(legacy.allowed(), "legacy predecessor admission must retain worst-case mode gating");
        assertEquals("world_effect_mode", legacy.code());

        ArcanaCastEngine engine = new ArcanaCastEngine(
            ignored -> ArcanaDecision.allow(),
            ignored -> ArcanaDecision.allow(),
            ignored -> ArcanaDecision.allow(),
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest ignored) { return ArcanaDecision.allow(); }
                @Override public void start(ArcanaCastRequest ignored) { }
            },
            ignored -> target,
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest ignored) { return ArcanaDecision.allow(); }
                @Override public ArcanaServices.CostReservation reserve(ArcanaCastRequest ignored) {
                    return new ArcanaServices.CostReservation() {
                        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                        @Override public void commit() { }
                        @Override public void refund() { }
                    };
                }
            },
            policy,
            (ignored, ignoredTarget) -> ArcanaServices.EffectResult.ok());

        assertEquals(dev.gustavopere.blackarcana.api.ArcanaCastResult.Status.SUCCESS, engine.execute(request).status(),
            "operation-scoped terrain policy must not cancel entity/visual fallback before the runtime chooses a mutation class");
    }

    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
            ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
            new ArcanaSpellDefinition(
                SPELL_ID,
                "spell.black_arcana.operation_scoped_probe",
                "black_arcana:operation_scoped_probe",
                new ArcanaCost("black_arcana:test", 1.0D),
                true),
            new ArcanaCastContext(
                UUID.fromString("22222222-2222-2222-2222-222222222222"),
                20L,
                "minecraft:overworld"));
    }
}
