package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
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
    @Test
    void malformedCompletionRowRequiresSanitizedSavedDataRewriteWithoutLosingValidReward() {
        RitualCompletionSavedData original = new RitualCompletionSavedData();
        RitualCompletionKey key = RitualCompletionKey.forCaster(
            ArcanaRitualId.parse("black_arcana:grand_attunement"),
            UUID.fromString("11111111-1111-1111-1111-111111111111"));
        assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, original.complete(key, 40L));

        CompoundTag root = original.save(new CompoundTag(), null);
        ListTag entries = root.getList("completions", Tag.TAG_COMPOUND);
        CompoundTag malformed = new CompoundTag();
        malformed.putString("ritual", "not a namespaced ritual");
        malformed.putString("scope", "CASTER");
        malformed.putString("subject", "broken");
        malformed.putLong("completed_at", 50L);
        entries.add(malformed);

        RitualCompletionSavedData restored = RitualCompletionSavedData.load(root, null);
        assertEquals(1, restored.size());
        assertTrue(restored.contains(key));
        assertTrue(restored.isDirty(), "dropping malformed persisted rewards must request a rewritten ledger");

        CompoundTag rewritten = restored.save(new CompoundTag(), null);
        assertEquals(1, rewritten.getList("completions", Tag.TAG_COMPOUND).size());
        RitualCompletionSavedData next = RitualCompletionSavedData.load(rewritten, null);
        assertTrue(next.contains(key));
        assertEquals(RitualCompletionLedger.CompletionResult.ALREADY_COMPLETED, next.complete(key, 90L),
                "a valid reward cannot be granted twice after sanitation and reload");
    }

    @Test
    void duplicateCompletionRowsRequireRewriteButPreserveFirstRecordedTimestamp() {
        RitualCompletionSavedData original = new RitualCompletionSavedData();
        RitualCompletionKey key = RitualCompletionKey.forCaster(
            ArcanaRitualId.parse("black_arcana:grand_attunement"),
            UUID.fromString("22222222-2222-2222-2222-222222222222"));
        assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, original.complete(key, 40L));
        CompoundTag root = original.save(new CompoundTag(), null);
        ListTag entries = root.getList("completions", Tag.TAG_COMPOUND);
        CompoundTag duplicate = entries.getCompound(0).copy();
        duplicate.putLong("completed_at", 80L);
        entries.add(duplicate);

        RitualCompletionSavedData restored = RitualCompletionSavedData.load(root, null);
        assertEquals(1, restored.size());
        assertTrue(restored.isDirty(), "deduplicated persisted completion must be normalized on next save");
        CompoundTag rewritten = restored.save(new CompoundTag(), null);
        ListTag normalized = rewritten.getList("completions", Tag.TAG_COMPOUND);
        assertEquals(1, normalized.size());
        assertEquals(40L, normalized.getCompound(0).getLong("completed_at"),
                "the first recorded completion must retain its original timestamp");
        assertEquals(RitualCompletionLedger.CompletionResult.ALREADY_COMPLETED, restored.complete(key, 90L));
    }

    @Test
    void cleanCompletionLedgerReloadDoesNotScheduleSpuriousRewrite() {
        RitualCompletionSavedData original = new RitualCompletionSavedData();
        RitualCompletionKey key = RitualCompletionKey.forCaster(
            ArcanaRitualId.parse("black_arcana:grand_attunement"),
            UUID.fromString("33333333-3333-3333-3333-333333333333"));
        assertEquals(RitualCompletionLedger.CompletionResult.RECORDED, original.complete(key, 40L));
        RitualCompletionSavedData clean = RitualCompletionSavedData.load(
            original.save(new CompoundTag(), null), null);

        assertTrue(clean.contains(key));
        assertTrue(!clean.isDirty(), "a valid ledger does not require a needless rewrite");
    }

}
