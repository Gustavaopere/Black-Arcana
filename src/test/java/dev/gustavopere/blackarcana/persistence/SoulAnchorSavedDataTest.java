package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.content.souls.SoulAnchorLedger;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SoulAnchorSavedDataTest {
    @Test
    void snapshotsRoundTripWithDeathIdempotencyJournal() {
        UUID owner = UUID.fromString("11111111-1111-1111-1111-111111111111");
        UUID creditedA = UUID.fromString("22222222-2222-2222-2222-222222222222");
        UUID creditedB = UUID.fromString("33333333-3333-3333-3333-333333333333");
        UUID prevented = UUID.fromString("44444444-4444-4444-4444-444444444444");
        SoulAnchorLedger.Snapshot snapshot = new SoulAnchorLedger.Snapshot(
            owner,
            17.5D,
            2,
            900L,
            List.of(creditedA, creditedB),
            prevented);

        SoulAnchorSavedData original = new SoulAnchorSavedData();
        original.replaceSnapshots(List.of(snapshot));
        CompoundTag encoded = original.save(new CompoundTag(), null);
        SoulAnchorSavedData restored = SoulAnchorSavedData.load(encoded, null);

        assertEquals(List.of(snapshot), restored.snapshots());
    }
}
