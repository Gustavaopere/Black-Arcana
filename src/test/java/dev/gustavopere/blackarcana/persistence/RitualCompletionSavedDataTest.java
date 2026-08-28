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
