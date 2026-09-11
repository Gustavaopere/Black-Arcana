package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.ArrayDeque;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralSeveranceRuntimeTest {
    private static final AstralProjectionPose ORIGIN =
            new AstralProjectionPose(4.0D, 72.0D, -3.0D, 15.0F, -5.0F);

    @Test
    void serverGeneratedIdentityIsBoundToCanonicalPhysicalBodyAndOneProjectionPerCaster() {
        UUID projectionA = UUID.randomUUID();
        UUID projectionB = UUID.randomUUID();
        ArrayDeque<UUID> ids = new ArrayDeque<>(List.of(projectionA, projectionB));
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, ids::removeFirst);
        UUID caster = UUID.randomUUID();

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(caster, 100L, 20, 12.0D, ORIGIN));
        var active = runtime.projection(caster).orElseThrow();
        assertEquals(projectionA, active.projectionId());
        assertEquals(caster, active.casterId());
        assertEquals(caster, active.physicalBodyId());
        assertEquals(12.0D, active.maxRangeBlocks());
        assertEquals(ORIGIN, active.originPose());
        assertEquals(ORIGIN, active.currentPose());

        assertEquals(AstralSeveranceRuntime.StartResult.CASTER_ALREADY_PROJECTED,
                runtime.start(caster, 101L, 20, 12.0D, ORIGIN));
        assertEquals(1, runtime.activeCount());
    }

    @Test
    void hardDurationRangeAndGlobalBoundsFailClosedWithoutInventingBalanceDefaults() {
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(1);
        UUID casterA = UUID.randomUUID();
        UUID casterB = UUID.randomUUID();

        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_DURATION,
                runtime.start(casterA, 1L, 0, 8.0D, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_DURATION,
                runtime.start(casterA, 1L, NoeticSafetyCeilings.MAX_DURATION_TICKS + 1, 8.0D, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_RANGE,
                runtime.start(casterA, 1L, 20, 0.0D, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_RANGE,
                runtime.start(casterA, 1L, 20, Double.NaN, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_RANGE,
                runtime.start(casterA, 1L, 20, Double.POSITIVE_INFINITY, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.INVALID_RANGE,
                runtime.start(casterA, 1L, 20, NoeticSafetyCeilings.MAX_RANGE_BLOCKS + 0.01D, ORIGIN));
        assertThrows(IllegalArgumentException.class,
                () -> runtime.start(casterA, -1L, 20, 8.0D, ORIGIN));

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterA, 1L, 20, NoeticSafetyCeilings.MAX_RANGE_BLOCKS, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.GLOBAL_LIMIT,
                runtime.start(casterB, 1L, 20, 8.0D, ORIGIN));
    }

    @Test
    void staleForeignOrReplayedReturnHandlesCannotCloseAProjection() {
        UUID projectionId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, () -> projectionId);
        UUID caster = UUID.randomUUID();

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(caster, 5L, 20, 8.0D, ORIGIN));
        assertFalse(runtime.requestReturn(caster, UUID.randomUUID()));
        assertFalse(runtime.requestReturn(UUID.randomUUID(), projectionId));
        assertEquals(1, runtime.activeCount());

        assertTrue(runtime.requestReturn(caster, projectionId));
        assertFalse(runtime.requestReturn(caster, projectionId));
        assertEquals(0, runtime.activeCount());
    }

    @Test
    void expiryAndServerStopCleanupAreExactAndBounded() {
        UUID casterA = UUID.randomUUID();
        UUID casterB = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2);

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterA, 10L, 5, 8.0D, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(casterB, 10L, 20, 8.0D, ORIGIN));

        assertEquals(0, runtime.expire(14L));
        assertEquals(1, runtime.expire(15L));
        assertTrue(runtime.projection(casterA).isEmpty());
        assertTrue(runtime.projection(casterB).isPresent());

        assertEquals(1, runtime.clearForServerStop());
        assertEquals(0, runtime.clearForServerStop());
        assertEquals(0, runtime.activeCount());
    }

    @Test
    void duplicateGeneratedProjectionIdentityFailsClosed() {
        UUID duplicateId = UUID.randomUUID();
        AstralSeveranceRuntime runtime = new AstralSeveranceRuntime(2, () -> duplicateId);

        assertEquals(AstralSeveranceRuntime.StartResult.STARTED,
                runtime.start(UUID.randomUUID(), 1L, 20, 8.0D, ORIGIN));
        assertEquals(AstralSeveranceRuntime.StartResult.IDENTITY_COLLISION,
                runtime.start(UUID.randomUUID(), 1L, 20, 8.0D, ORIGIN));
        assertEquals(1, runtime.activeCount());
    }
}
