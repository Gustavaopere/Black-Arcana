package dev.gustavopere.blackarcana.integration.curios;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CuriosEquipmentSnapshotAdapterTest {
    @Test
    void missingAndBinaryIncompatibleCuriosAreDistinguished() {
        assertEquals(
            CuriosEquipmentSnapshotAdapter.Availability.MISSING_MOD,
            CuriosEquipmentSnapshotAdapter.probe(false, getClass().getClassLoader()).availability());
        assertEquals(
            CuriosEquipmentSnapshotAdapter.Availability.API_INCOMPATIBLE,
            CuriosEquipmentSnapshotAdapter.probe(true, ClassLoader.getPlatformClassLoader()).availability());
    }

    @Test
    void duplicateTraversalOfSameStackIdentityCannotDoubleCount() {
        ItemStack shared = new ItemStack(Items.DIAMOND);
        var normalized = CuriosEquipmentSnapshotAdapter.normalizeStacks(List.of(shared, shared));
        assertEquals(1, normalized.size());
        assertEquals("minecraft:diamond", normalized.getFirst().itemId());
    }

    @Test
    void distinctStacksOfSameItemRemainDistinctEquippedItems() {
        var normalized = CuriosEquipmentSnapshotAdapter.normalizeStacks(List.of(
            new ItemStack(Items.DIAMOND), new ItemStack(Items.DIAMOND)));
        assertEquals(2, normalized.size());
    }
}
