package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import java.util.Objects;
import java.util.UUID;

/**
 * Inventory-backed Malum spirit bridge. It deliberately uses vanilla item IDs
 * rather than Malum implementation classes, keeping the binary dependency optional.
 */
public final class NeoForgeMalumSpiritInventoryAccess implements MalumSpiritAccess {
    private final MinecraftServer server;

    private NeoForgeMalumSpiritInventoryAccess(MinecraftServer server) {
        this.server = Objects.requireNonNull(server, "server");
    }

    public static NeoForgeMalumSpiritInventoryAccess probe(MinecraftServer server) throws ReflectiveOperationException {
        Objects.requireNonNull(server, "server");
        // These are canonical 1.21.1 shard ids. Probe several families so a
        // registry rename fails closed instead of silently consuming another item.
        requireSpiritItem("arcane");
        requireSpiritItem("wicked");
        requireSpiritItem("eldritch");
        return new NeoForgeMalumSpiritInventoryAccess(server);
    }

    @Override
    public int count(UUID playerId, String affinity) {
        ServerPlayer player = requirePlayer(playerId);
        Item item = requireSpiritItem(affinity);
        int total = 0;
        var inventory = player.getInventory();
        for (int slot = 0; slot < inventory.getContainerSize(); slot++) {
            ItemStack stack = inventory.getItem(slot);
            if (stack.is(item)) total = Math.addExact(total, stack.getCount());
        }
        return total;
    }

    @Override
    public ArcanaDecision adjust(UUID playerId, String affinity, int delta) {
        if (delta == 0) return ArcanaDecision.allow();
        if (Math.abs((long) delta) > MalumSpiritCostProvider.ABSOLUTE_MAX_SPIRIT_COST) {
            return ArcanaDecision.deny("malum_spirit_delta_too_large", "spirit adjustment exceeds bounded shard limit");
        }

        ServerPlayer player;
        Item item;
        try {
            player = requirePlayer(playerId);
            item = requireSpiritItem(affinity);
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("malum_spirit_unavailable", failure.getMessage());
        }

        if (delta < 0) return remove(player, item, -delta);
        return add(player, item, delta);
    }

    private static ArcanaDecision remove(ServerPlayer player, Item item, int amount) {
        var inventory = player.getInventory();
        int available = 0;
        for (int slot = 0; slot < inventory.getContainerSize(); slot++) {
            ItemStack stack = inventory.getItem(slot);
            if (stack.is(item)) available += stack.getCount();
        }
        if (available < amount) {
            return ArcanaDecision.deny("insufficient_malum_spirits", "spirit inventory changed before reservation");
        }

        int remaining = amount;
        for (int slot = 0; slot < inventory.getContainerSize() && remaining > 0; slot++) {
            ItemStack stack = inventory.getItem(slot);
            if (!stack.is(item)) continue;
            int taken = Math.min(remaining, stack.getCount());
            stack.shrink(taken);
            remaining -= taken;
        }
        inventory.setChanged();
        return remaining == 0
            ? ArcanaDecision.allow()
            : ArcanaDecision.deny("malum_spirit_remove_incomplete", "spirit removal did not complete atomically");
    }

    private static ArcanaDecision add(ServerPlayer player, Item item, int amount) {
        ItemStack refund = new ItemStack(item, amount);
        player.getInventory().add(refund);
        if (!refund.isEmpty()) {
            player.drop(refund, false);
        }
        player.getInventory().setChanged();
        return ArcanaDecision.allow();
    }

    private ServerPlayer requirePlayer(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        if (player == null) throw new IllegalStateException("player is not online on this server");
        return player;
    }

    private static Item requireSpiritItem(String affinity) {
        Objects.requireNonNull(affinity, "affinity");
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(MalumIntegrationIds.MOD_ID, affinity + "_spirit");
        return BuiltInRegistries.ITEM.getOptional(id)
            .orElseThrow(() -> new IllegalStateException("Malum spirit item is missing: " + id));
    }
}
