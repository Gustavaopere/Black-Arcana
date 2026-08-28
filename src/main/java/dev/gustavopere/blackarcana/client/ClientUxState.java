package dev.gustavopere.blackarcana.client;

import net.minecraft.client.Minecraft;

/** Ephemeral physical-client presentation timing only. */
public final class ClientUxState {
    private static long selectionChangedTick = Long.MIN_VALUE;

    private ClientUxState() { }

    public static void markSelectionChanged() {
        var player = Minecraft.getInstance().player;
        if (player != null) selectionChangedTick = player.tickCount;
    }

    public static long selectionChangedTick() {
        return selectionChangedTick;
    }

    public static void clear() {
        selectionChangedTick = Long.MIN_VALUE;
    }
}
