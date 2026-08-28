package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationTracker;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackArcanaSavedDataTemporaryMutationTest {
    @Test
    void temporaryRestorationSurvivesSaveAndReload() {
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var source = new TemporaryMutationTracker(8);
        UUID owner = UUID.fromString("11111111-1111-1111-1111-111111111111");
        ArcanaCastId castId = ArcanaCastId.parse("22222222-2222-2222-2222-222222222222");
        source.register(
            new TemporaryMutationKey("minecraft:overworld", 123L),
            owner,
            castId,
            "minecraft:stone",
            "black_arcana:temporary_veil",
            500L);

        var saved = new BlackArcanaSavedData();
        saved.capture(cooldowns, charges, loadouts, source, 100L);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        var restored = new TemporaryMutationTracker(8);
        loaded.restore(cooldowns, charges, loadouts, restored, 100L);

        assertEquals(1, restored.size());
        var mutation = restored.snapshot().getFirst();
        assertEquals("minecraft:overworld", mutation.key().dimensionId());
        assertEquals(123L, mutation.key().packedBlockPos());
        assertEquals(owner, mutation.ownerId());
        assertEquals(castId, mutation.castId());
        assertEquals("minecraft:stone", mutation.originalState());
        assertEquals("black_arcana:temporary_veil", mutation.replacementState());
        assertEquals(500L, mutation.expiresAtTick());
    }
}
