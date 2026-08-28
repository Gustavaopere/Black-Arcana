package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TemporaryMutationTrackerTest {
    private static final TemporaryMutationKey KEY = new TemporaryMutationKey("minecraft:overworld", 42L);

    @Test
    void overlappingArcanaMutationPreservesOriginalStateAndExtendsExpiry() {
        var tracker = new TemporaryMutationTracker(4);
        var owner = UUID.randomUUID();

        var first = tracker.register(KEY, owner, ArcanaCastId.random(), "minecraft:stone", "black_arcana:veil", 20);
        var second = tracker.register(KEY, owner, ArcanaCastId.random(), "black_arcana:veil", "black_arcana:black_flame", 40);

        assertTrue(first.decision().allowed());
        assertTrue(second.decision().allowed());
        assertEquals("minecraft:stone", second.mutation().originalState());
        assertEquals(40, second.mutation().expiresAtTick());
        assertEquals(1, tracker.size());
    }

    @Test
    void playerEditIsNeverOverwrittenByExpiry() {
        var tracker = new TemporaryMutationTracker(4);
        var owner = UUID.randomUUID();
        tracker.register(KEY, owner, ArcanaCastId.random(), "minecraft:stone", "black_arcana:veil", 20);

        List<TemporaryMutationTracker.ExpiryAction> actions = tracker.inspectExpired(
            20, 4, ignored -> Optional.of("minecraft:diamond_block"));

        assertEquals(1, actions.size());
        assertEquals(TemporaryMutationTracker.ExpiryAction.Kind.DROP_CHANGED, actions.getFirst().kind());
        assertEquals(0, tracker.size());
    }

    @Test
    void unloadedChunkStaysPendingWithoutForceLoad() {
        var tracker = new TemporaryMutationTracker(4);
        var owner = UUID.randomUUID();
        tracker.register(KEY, owner, ArcanaCastId.random(), "minecraft:stone", "black_arcana:veil", 20);

        var actions = tracker.inspectExpired(20, 4, ignored -> Optional.empty());

        assertEquals(TemporaryMutationTracker.ExpiryAction.Kind.UNAVAILABLE, actions.getFirst().kind());
        assertEquals(1, tracker.size());
    }

    @Test
    void restorationRequiresConfirmationBeforeRecordIsRemoved() {
        var tracker = new TemporaryMutationTracker(4);
        var owner = UUID.randomUUID();
        tracker.register(KEY, owner, ArcanaCastId.random(), "minecraft:stone", "black_arcana:veil", 20);

        var actions = tracker.inspectExpired(20, 4, ignored -> Optional.of("black_arcana:veil"));
        assertEquals(TemporaryMutationTracker.ExpiryAction.Kind.RESTORE, actions.getFirst().kind());
        assertEquals(1, tracker.size());
        assertFalse(tracker.confirmRestored(KEY, "black_arcana:veil"));
        assertTrue(tracker.confirmRestored(KEY, "minecraft:stone"));
        assertEquals(0, tracker.size());
    }

    @Test
    void snapshotRestoreIsBounded() {
        var tracker = new TemporaryMutationTracker(2);
        var owner = UUID.randomUUID();
        var snapshot = List.of(
            new TemporaryWorldMutation(new TemporaryMutationKey("minecraft:overworld", 1), owner, ArcanaCastId.random(), "a", "b", 10),
            new TemporaryWorldMutation(new TemporaryMutationKey("minecraft:overworld", 2), owner, ArcanaCastId.random(), "a", "b", 10),
            new TemporaryWorldMutation(new TemporaryMutationKey("minecraft:overworld", 3), owner, ArcanaCastId.random(), "a", "b", 10));

        assertEquals(2, tracker.restoreSnapshot(snapshot));
        assertEquals(2, tracker.size());
    }
}
