package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackArcanaSavedDataLoadoutTest {
    @Test
    void fullCanonicalLoadoutSurvivesCaptureSaveLoadAndRestore() {
        UUID caster = UUID.fromString("33333333-3333-3333-3333-333333333333");
        List<ArcanaSpellId> fullLoadout = IntStream.range(0, ArcanaCastRequest.MAX_LOADOUT_SLOTS)
                .mapToObj(index -> ArcanaSpellId.parse("black_arcana:slot_" + index))
                .toList();
        LoadoutRegistry source = new LoadoutRegistry();
        source.setLoadout(caster, fullLoadout);
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.capture(cooldowns, charges, source, 0L);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        LoadoutRegistry restored = new LoadoutRegistry();

        loaded.restore(cooldowns, charges, restored, 0L);

        assertEquals(ArcanaCastRequest.MAX_LOADOUT_SLOTS, restored.getLoadout(caster).size());
        assertEquals(fullLoadout, restored.getLoadout(caster));
    }

    @Test
    void malformedDuplicatePersistedLoadoutIsDiscardedPerCaster() {
        UUID validCaster = UUID.fromString("11111111-1111-1111-1111-111111111111");
        UUID malformedCaster = UUID.fromString("22222222-2222-2222-2222-222222222222");
        ArcanaSpellId alpha = ArcanaSpellId.parse("black_arcana:alpha");
        ArcanaSpellId beta = ArcanaSpellId.parse("black_arcana:beta");
        ArcanaSpellId duplicate = ArcanaSpellId.parse("black_arcana:duplicate");

        CompoundTag root = new CompoundTag();
        root.putInt("schema", 1);
        ListTag persistedLoadouts = new ListTag();
        persistedLoadouts.add(loadout(validCaster, alpha.canonical(), beta.canonical()));
        persistedLoadouts.add(loadout(malformedCaster, duplicate.canonical(), duplicate.canonical()));
        root.put("loadouts", persistedLoadouts);

        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        LoadoutRegistry restored = new LoadoutRegistry();
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);

        assertDoesNotThrow(() -> loaded.restore(cooldowns, charges, restored, 0L));
        assertEquals(List.of(alpha, beta), restored.getLoadout(validCaster));
        assertEquals(List.of(), restored.getLoadout(malformedCaster));
    }

    private static CompoundTag loadout(UUID caster, String... spellIds) {
        CompoundTag tag = new CompoundTag();
        tag.putUUID("caster", caster);
        ListTag spells = new ListTag();
        for (String spellId : spellIds) spells.add(StringTag.valueOf(spellId));
        tag.put("spells", spells);
        return tag;
    }
}
