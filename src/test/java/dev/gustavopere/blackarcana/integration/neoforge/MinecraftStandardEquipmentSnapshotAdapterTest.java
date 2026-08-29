package dev.gustavopere.blackarcana.integration.neoforge;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftStandardEquipmentSnapshotAdapterTest {
    @Test
    void nonDamageableStackUsesUnboundedDurabilitySentinel() {
        var snapshot = MinecraftStandardEquipmentSnapshotAdapter.normalize("mainhand", new ItemStack(Items.DIAMOND));
        assertTrue(snapshot.isPresent());
        assertEquals("mainhand", snapshot.orElseThrow().slotId());
        assertEquals("minecraft:diamond", snapshot.orElseThrow().itemId());
        assertEquals(Integer.MAX_VALUE, snapshot.orElseThrow().durabilityRemaining());
    }

    @Test
    void damageableStackFreezesRemainingDurability() {
        ItemStack stack = new ItemStack(Items.DIAMOND_HELMET);
        stack.setDamageValue(7);

        var snapshot = MinecraftStandardEquipmentSnapshotAdapter.normalize("head", stack);

        assertTrue(snapshot.isPresent());
        assertEquals(stack.getMaxDamage() - 7, snapshot.orElseThrow().durabilityRemaining());
    }

    @Test
    void emptyStackIsNotPublished() {
        assertTrue(MinecraftStandardEquipmentSnapshotAdapter.normalize("offhand", ItemStack.EMPTY).isEmpty());
    }
}
