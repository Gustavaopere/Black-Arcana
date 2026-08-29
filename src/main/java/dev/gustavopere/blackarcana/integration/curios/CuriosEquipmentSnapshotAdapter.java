package dev.gustavopere.blackarcana.integration.curios;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentProfileRegistry;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

/** Installed-first Curios 9.5.1+1.21.1 snapshot bridge with no binary Curios signature. */
public final class CuriosEquipmentSnapshotAdapter {
    public enum Availability { AVAILABLE, MISSING_MOD, API_INCOMPATIBLE }

    private final Availability availability;
    private final Method getCuriosInventory;
    private final Method getEquippedCurios;
    private final Method getSlots;
    private final Method getStackInSlot;

    private CuriosEquipmentSnapshotAdapter(
        Availability availability,
        Method getCuriosInventory,
        Method getEquippedCurios,
        Method getSlots,
        Method getStackInSlot
    ) {
        this.availability = availability;
        this.getCuriosInventory = getCuriosInventory;
        this.getEquippedCurios = getEquippedCurios;
        this.getSlots = getSlots;
        this.getStackInSlot = getStackInSlot;
    }

    public static CuriosEquipmentSnapshotAdapter probe(boolean modLoaded, ClassLoader loader) {
        Objects.requireNonNull(loader, "loader");
        if (!modLoaded) return unavailable(Availability.MISSING_MOD);
        try {
            Class<?> api = Class.forName("top.theillusivec4.curios.api.CuriosApi", false, loader);
            Class<?> handler = Class.forName("top.theillusivec4.curios.api.type.capability.ICuriosItemHandler", false, loader);
            Class<?> itemHandler = Class.forName("net.neoforged.neoforge.items.IItemHandler", false, loader);
            return new CuriosEquipmentSnapshotAdapter(
                Availability.AVAILABLE,
                api.getMethod("getCuriosInventory", LivingEntity.class),
                handler.getMethod("getEquippedCurios"),
                itemHandler.getMethod("getSlots"),
                itemHandler.getMethod("getStackInSlot", int.class));
        } catch (ReflectiveOperationException | LinkageError incompatible) {
            return unavailable(Availability.API_INCOMPATIBLE);
        }
    }

    public Availability availability() { return availability; }

    public ArcaneEquipmentSnapshotService.Snapshot snapshot(ServerPlayer player, ArcaneEquipmentProfileRegistry profiles) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(profiles, "profiles");
        if (availability != Availability.AVAILABLE) return new ArcaneEquipmentSnapshotService(profiles).capture(List.of());
        try {
            Object optionalObject = getCuriosInventory.invoke(null, player);
            if (!(optionalObject instanceof Optional<?> optional) || optional.isEmpty()) {
                return new ArcaneEquipmentSnapshotService(profiles).capture(List.of());
            }
            Object combined = getEquippedCurios.invoke(optional.get());
            int slots = Math.min((int) getSlots.invoke(combined), ArcaneEquipmentSnapshotService.MAX_EQUIPPED_SLOTS);
            List<ItemStack> stacks = new ArrayList<>(slots);
            for (int index = 0; index < slots; index++) {
                Object raw = getStackInSlot.invoke(combined, index);
                if (raw instanceof ItemStack stack) stacks.add(stack);
            }
            return new ArcaneEquipmentSnapshotService(profiles).capture(normalizeStacks(stacks));
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            return new ArcaneEquipmentSnapshotService(profiles).capture(List.of());
        }
    }

    static List<ArcaneEquipmentSlotSnapshot> normalizeStacks(List<ItemStack> stacks) {
        Objects.requireNonNull(stacks, "stacks");
        List<ArcaneEquipmentSlotSnapshot> result = new ArrayList<>();
        Set<ItemStack> seenStacks = Collections.newSetFromMap(new IdentityHashMap<>());
        int bounded = Math.min(stacks.size(), ArcaneEquipmentSnapshotService.MAX_EQUIPPED_SLOTS);
        for (int index = 0; index < bounded; index++) {
            ItemStack stack = stacks.get(index);
            if (stack == null || stack.isEmpty() || !seenStacks.add(stack)) continue;
            String itemId = BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
            int durability = stack.isDamageableItem()
                ? Math.max(0, stack.getMaxDamage() - stack.getDamageValue())
                : Integer.MAX_VALUE;
            result.add(new ArcaneEquipmentSlotSnapshot("curio_" + index, itemId, durability));
        }
        return List.copyOf(result);
    }

    private static CuriosEquipmentSnapshotAdapter unavailable(Availability availability) {
        return new CuriosEquipmentSnapshotAdapter(availability, null, null, null, null);
    }
}
