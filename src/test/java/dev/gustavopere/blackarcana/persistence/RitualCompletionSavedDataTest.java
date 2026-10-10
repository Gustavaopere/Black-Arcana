package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RitualCompletionSavedDataTest {
    @Test
    void fullPersistedLedgerAdvertisesNoSpaceWithoutRecordingAnExtraReward() {
        RitualCompletionSavedData data = new RitualCompletionSavedData();
        ArcanaRitualId ritual = ArcanaRitualId.parse("black_arcana:grand_attunement");
        assertTrue(data.canAcceptNewCompletion());
        for (int i = 0; i < RitualCompletionSavedData.MAX_PERSISTED_COMPLETIONS; i++) {
            RitualCompletionKey key = RitualCompletionKey.forCaster(ritual, new UUID(0L, i + 1L));
            assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, data.complete(key, i));
        }
        assertEquals(RitualCompletionSavedData.MAX_PERSISTED_COMPLETIONS, data.size());
        assertTrue(!data.canAcceptNewCompletion());
        RitualCompletionKey additional = RitualCompletionKey.forCaster(ritual, new UUID(1L, 1L));
        assertEquals(RitualCompletionLedger.CompletionResult.CAPACITY_EXCEEDED, data.complete(additional, 20000L));
        assertEquals(RitualCompletionSavedData.MAX_PERSISTED_COMPLETIONS, data.size());
    }

    @Test
    void completionRoundTripsAndRemainsIdempotent() {
        RitualCompletionSavedData original = new RitualCompletionSavedData();
        RitualCompletionKey key = RitualCompletionKey.forCaster(
            ArcanaRitualId.parse("black_arcana:grand_attunement"),
            UUID.fromString("11111111-1111-1111-1111-111111111111"));

        assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, original.complete(key, 40L));
        CompoundTag tag = original.save(new CompoundTag(), null);
        RitualCompletionSavedData restored = RitualCompletionSavedData.load(tag, null);

        assertTrue(restored.contains(key));
        assertEquals(1, restored.size());
        assertEquals(RitualCompletionLedger.CompletionResult.ALREADY_COMPLETED, restored.complete(key, 80L));
    }
}
