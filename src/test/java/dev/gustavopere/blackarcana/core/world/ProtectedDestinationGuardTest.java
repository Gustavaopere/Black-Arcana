package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProtectedDestinationGuardTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");

    @Test
    void unloadedDestinationIsDeniedBeforeProtectionAdapters() {
        ProtectionAdapterRegistry adapters = new ProtectionAdapterRegistry(4);
        adapters.register("must-not-run", query -> {
            throw new AssertionError("protection adapter must not run for unloaded destination");
        });
        ProtectedDestinationGuard guard = new ProtectedDestinationGuard(
            new LoadedChunkGuard(4, chunk -> false),
            adapters);

        ArcanaDecision decision = guard.authorize(
            new ChunkRef("minecraft:overworld", 10, 10),
            query("minecraft:overworld", "block:test"));

        assertFalse(decision.allowed());
        assertEquals("world_chunk_unloaded", decision.code());
    }

    @Test
    void protectionAdapterDenialWinsAfterLoadedChunkCheck() {
        ProtectionAdapterRegistry adapters = new ProtectionAdapterRegistry(4);
        adapters.register("claims", query -> ArcanaDecision.deny("claim_protected", "protected"));
        ProtectedDestinationGuard guard = new ProtectedDestinationGuard(
            new LoadedChunkGuard(4, chunk -> true),
            adapters);

        ArcanaDecision decision = guard.authorize(
            new ChunkRef("minecraft:overworld", 0, 0),
            query("minecraft:overworld", "protected:test"));

        assertFalse(decision.allowed());
        assertEquals("claim_protected", decision.code());
    }

    @Test
    void loadedUnprotectedDestinationIsAllowed() {
        ProtectedDestinationGuard guard = new ProtectedDestinationGuard(
            new LoadedChunkGuard(4, chunk -> true),
            new ProtectionAdapterRegistry(4));

        assertTrue(guard.authorize(
            new ChunkRef("minecraft:overworld", 0, 0),
            query("minecraft:overworld", "block:test")).allowed());
    }

    @Test
    void dimensionMismatchFailsClosed() {
        ProtectedDestinationGuard guard = new ProtectedDestinationGuard(
            new LoadedChunkGuard(4, chunk -> true),
            new ProtectionAdapterRegistry(4));

        ArcanaDecision decision = guard.authorize(
            new ChunkRef("minecraft:the_nether", 0, 0),
            query("minecraft:overworld", "block:test"));

        assertFalse(decision.allowed());
        assertEquals("destination_dimension_mismatch", decision.code());
    }

    private static ProtectionQuery query(String dimension, String target) {
        return new ProtectionQuery(CASTER, dimension, target, EntityInteractionType.DISPLACEMENT);
    }
}
