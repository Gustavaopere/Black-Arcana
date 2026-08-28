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
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WorldEffectAdmissionServiceTest {
    private static final ArcanaSpellId ID = ArcanaSpellId.parse("black_arcana:temporary_probe");
    private static final ChunkRef CHUNK = new ChunkRef("minecraft:overworld", 0, 0);

    @Test
    void undeclaredMutationFailsClosedBeforeChunkOrBudgetWork() {
        var profiles = new WorldEffectProfileRegistry();
        var service = service(profiles, chunk -> true);

        assertEquals("world_mutation_not_declared",
            service.authorize(request(false), target(), List.of(CHUNK), 1).code());
    }

    @Test
    void requestedWorkCannotExceedDeclaredSpellBound() {
        var profiles = profiles(2);
        var service = service(profiles, chunk -> true);

        assertEquals("world_effect_declared_budget",
            service.authorize(request(true), target(), List.of(CHUNK), 3).code());
    }

    @Test
    void unloadedChunkAndCumulativeBudgetFailClosed() {
        var profiles = profiles(4);
        var unloaded = service(profiles, chunk -> false);
        assertEquals("world_chunk_unloaded",
            unloaded.authorize(request(true), target(), List.of(CHUNK), 1).code());

        var ledger = new WorldEffectBudgetLedger(4, 2, 100);
        var policy = new ConfigurableWorldEffectPolicy(profiles, WorldEffectPolicyConfig.safeDefaults());
        var loaded = new WorldEffectAdmissionService(policy, new LoadedChunkGuard(4, chunk -> true), ledger);
        ArcanaCastRequest request = request(true);
        assertTrue(loaded.authorize(request, target(), List.of(CHUNK), 1).allowed());
        assertTrue(loaded.authorize(request, target(), List.of(CHUNK), 1).allowed());
        assertFalse(loaded.authorize(request, target(), List.of(CHUNK), 1).allowed());
    }

    private static WorldEffectAdmissionService service(
        WorldEffectProfileRegistry profiles,
        LoadedChunkGuard.LoadedChunkProbe probe
    ) {
        return new WorldEffectAdmissionService(
            new ConfigurableWorldEffectPolicy(profiles, WorldEffectPolicyConfig.safeDefaults()),
            new LoadedChunkGuard(4, probe),
            new WorldEffectBudgetLedger(8, 8, 100));
    }

    private static WorldEffectProfileRegistry profiles(int units) {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.TEMPORARY_BLOCK,
            WorldMutationClass.TEMPORARY,
            units,
            false));
        return profiles;
    }

    private static ArcanaCastRequest request(boolean mutation) {
        return new ArcanaCastRequest(
            new ArcanaCastId(UUID.fromString("11111111-1111-1111-1111-111111111111")),
            new ArcanaSpellDefinition(
                ID,
                "spell.black_arcana.temporary_probe",
                "black_arcana:textures/spell/temporary_probe.png",
                new ArcanaCost("black_arcana:test", 1),
                mutation),
            new ArcanaCastContext(
                UUID.fromString("22222222-2222-2222-2222-222222222222"),
                20L,
                "minecraft:overworld"));
    }

    private static ArcanaServices.TargetResolution target() {
        return ArcanaServices.TargetResolution.resolved("block:0,64,0");
    }
}
