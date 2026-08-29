package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentProfileRegistry;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSetBonusRegistry;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Snapshots the six standard player equipment slots without converting vanilla armor stats. */
public final class MinecraftStandardEquipmentSnapshotAdapter {
    private static final List<SlotBinding> STANDARD_SLOTS = List.of(
        new SlotBinding("mainhand", EquipmentSlot.MAINHAND),
        new SlotBinding("offhand", EquipmentSlot.OFFHAND),
        new SlotBinding("head", EquipmentSlot.HEAD),
        new SlotBinding("chest", EquipmentSlot.CHEST),
        new SlotBinding("legs", EquipmentSlot.LEGS),
        new SlotBinding("feet", EquipmentSlot.FEET));

    private final ArcaneEquipmentSnapshotService snapshots;

    public MinecraftStandardEquipmentSnapshotAdapter(ArcaneEquipmentProfileRegistry profiles) {
        this(profiles, new ArcaneEquipmentSetBonusRegistry());
    }

    public MinecraftStandardEquipmentSnapshotAdapter(
        ArcaneEquipmentProfileRegistry profiles,
        ArcaneEquipmentSetBonusRegistry setBonuses
    ) {
        this.snapshots = new ArcaneEquipmentSnapshotService(
            Objects.requireNonNull(profiles, "profiles"),
            Objects.requireNonNull(setBonuses, "setBonuses"));
    }

    public ArcaneEquipmentSnapshotService.Snapshot snapshot(ServerPlayer player) {
        Objects.requireNonNull(player, "player");
        List<ArcaneEquipmentSlotSnapshot> equipped = new ArrayList<>(STANDARD_SLOTS.size());
        for (SlotBinding binding : STANDARD_SLOTS) {
            normalize(binding.id(), player.getItemBySlot(binding.slot())).ifPresent(equipped::add);
        }
        return snapshots.capture(equipped);
    }

    static Optional<ArcaneEquipmentSlotSnapshot> normalize(String slotId, ItemStack stack) {
        Objects.requireNonNull(slotId, "slotId");
        Objects.requireNonNull(stack, "stack");
        if (stack.isEmpty()) return Optional.empty();
        String itemId = BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
        int durability = stack.isDamageableItem()
            ? Math.max(0, stack.getMaxDamage() - stack.getDamageValue())
            : Integer.MAX_VALUE;
        return Optional.of(new ArcaneEquipmentSlotSnapshot(slotId, itemId, durability));
    }

    private record SlotBinding(String id, EquipmentSlot slot) { }
}
