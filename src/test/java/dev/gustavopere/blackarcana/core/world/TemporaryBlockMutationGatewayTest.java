package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TemporaryBlockMutationGatewayTest {
    private static final ArcanaSpellId ID = ArcanaSpellId.parse("black_arcana:temporary_probe");
    private static final TemporaryMutationKey KEY = new TemporaryMutationKey("minecraft:overworld", 42L);
    private static final ChunkRef CHUNK = new ChunkRef("minecraft:overworld", 0, 0);

    @Test
    void mutationRegistersRollbackBeforeApplyingAndRestoresAtExpiry() {
        var backend = new MapBackend();
        backend.states.put(KEY, "minecraft:stone");
        var tracker = new TemporaryMutationTracker(8);
        var gateway = gateway(tracker, backend);

        assertTrue(gateway.replace(request(), target(), CHUNK, KEY, "black_arcana:veil", 40L).allowed());
        assertEquals("black_arcana:veil", backend.states.get(KEY));
        assertEquals(1, tracker.size());

        var restoration = new TemporaryRestorationService(tracker, backend).tick(40L, 8);
        assertEquals(1, restoration.restored());
        assertEquals("minecraft:stone", backend.states.get(KEY));
        assertEquals(0, tracker.size());
    }

    @Test
    void failedCompareAndSetRollsBackTrackingRecord() {
        var backend = new MapBackend();
        backend.states.put(KEY, "minecraft:stone");
        backend.forceCompareFailure = true;
        var tracker = new TemporaryMutationTracker(8);

        var decision = gateway(tracker, backend).replace(
            request(), target(), CHUNK, KEY, "black_arcana:veil", 40L);

        assertFalse(decision.allowed());
        assertEquals("world_state_changed", decision.code());
        assertEquals(0, tracker.size());
        assertEquals("minecraft:stone", backend.states.get(KEY));
    }

    @Test
    void backendExceptionKeepsRestorationRecordFailSafe() {
        var backend = new MapBackend();
        backend.states.put(KEY, "minecraft:stone");
        backend.throwOnReplace = true;
        var tracker = new TemporaryMutationTracker(8);

        var decision = gateway(tracker, backend).replace(
            request(), target(), CHUNK, KEY, "black_arcana:veil", 40L);

        assertFalse(decision.allowed());
        assertEquals("world_backend_failed", decision.code());
        assertEquals(1, tracker.size());
    }

    @Test
    void lifetimeIsBoundedBeforeAdmission() {
        var backend = new MapBackend();
        backend.states.put(KEY, "minecraft:stone");
        var tracker = new TemporaryMutationTracker(8);

        var decision = gateway(tracker, backend).replace(
            request(), target(), CHUNK, KEY, "black_arcana:veil", 20L + 201L);

        assertEquals("temporary_lifetime", decision.code());
        assertEquals(0, tracker.size());
    }

    private static TemporaryBlockMutationGateway gateway(
        TemporaryMutationTracker tracker,
        TemporaryBlockBackend backend
    ) {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.TEMPORARY_BLOCK,
            WorldMutationClass.TEMPORARY,
            8,
            false));
        var policy = new ConfigurableWorldEffectPolicy(profiles, WorldEffectPolicyConfig.safeDefaults());
        var admission = new WorldEffectAdmissionService(
            policy,
            new LoadedChunkGuard(4, chunk -> true),
            new WorldEffectBudgetLedger(8, 8, 100));
        return new TemporaryBlockMutationGateway(admission, tracker, backend, 200L);
    }

    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
            ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
            new ArcanaSpellDefinition(
                ID,
                "spell.black_arcana.temporary_probe",
                "black_arcana:textures/spell/temporary_probe.png",
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

    private static final class MapBackend implements TemporaryBlockBackend {
        final Map<TemporaryMutationKey, String> states = new HashMap<>();
        boolean forceCompareFailure;
        boolean throwOnReplace;

        @Override
        public Optional<String> readLoadedState(TemporaryMutationKey key) {
            return Optional.ofNullable(states.get(key));
        }

        @Override
        public boolean replaceIfCurrent(TemporaryMutationKey key, String expectedState, String replacementState) {
            if (throwOnReplace) throw new IllegalStateException("simulated backend failure");
            if (forceCompareFailure) return false;
            if (!expectedState.equals(states.get(key))) return false;
            states.put(key, replacementState);
            return true;
        }
    }
}
