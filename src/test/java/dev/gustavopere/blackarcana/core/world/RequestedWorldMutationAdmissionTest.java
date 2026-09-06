package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RequestedWorldMutationAdmissionTest {
    private static final ArcanaSpellId ID = ArcanaSpellId.parse("black_arcana:adaptive_world_probe");
    private static final ChunkRef CHUNK = new ChunkRef("minecraft:overworld", 0, 0);

    @Test
    void permanentWorstCaseCanRequestTemporaryUnderTemporaryModeWithoutChangingLegacyPolicy() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.PERMANENT,
            8,
            false));
        var policy = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 8, true, Map.of()));

        assertEquals("world_effect_mode", policy.authorize(request(), target()).code(),
            "legacy authorization must continue evaluating the declared worst case");
        assertTrue(policy.authorize(request(), target(), WorldMutationClass.TEMPORARY).allowed(),
            "operation-specific TEMPORARY work must be allowed below a PERMANENT worst case");
    }

    @Test
    void requestedClassCannotExceedRegisteredWorstCase() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.TEMPORARY,
            8,
            false));
        var policy = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(WorldEffectMode.FULL, 8, true, Map.of()));

        var decision = policy.authorize(request(), target(), WorldMutationClass.LIMITED);
        assertFalse(decision.allowed());
        assertEquals("world_effect_class_exceeds_profile", decision.code());
    }

    @Test
    void requestedClassAdmissionSupportsNonConsumingPreflightThenSingleCanonicalBudgetConsume() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.PERMANENT,
            8,
            false));
        var ledger = new WorldEffectBudgetLedger(8, 8, 100);
        var service = new WorldEffectAdmissionService(
            new ConfigurableWorldEffectPolicy(
                profiles,
                new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 8, true, Map.of())),
            new LoadedChunkGuard(4, chunk -> true),
            ledger);
        var request = request();

        assertTrue(service.preflight(
            request, target(), List.of(CHUNK), 1, WorldMutationClass.TEMPORARY).allowed());
        assertEquals(0, ledger.usedUnits(request.castId()), "preflight must not consume world budget");
        assertTrue(service.consumeBudget(request, 1).allowed());
        assertEquals(1, ledger.usedUnits(request.castId()));
    }

    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
            ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
            new ArcanaSpellDefinition(
                ID,
                "spell.black_arcana.adaptive_world_probe",
                "black_arcana:textures/spell/adaptive_world_probe.png",
                new ArcanaCost("black_arcana:test", 1),
                true),
            new ArcanaCastContext(
                UUID.fromString("22222222-2222-2222-2222-222222222222"),
                20L,
                "minecraft:overworld"));
    }

    private static ArcanaServices.TargetResolution target() {
        return ArcanaServices.TargetResolution.resolved("block:0,64,0");
    }
}
