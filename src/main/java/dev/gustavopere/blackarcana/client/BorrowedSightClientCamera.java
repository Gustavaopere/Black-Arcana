package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.BorrowedSightCameraPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;

import java.util.Objects;

/** Physical-client-only presentation handler for Borrowed Sight. */
public final class BorrowedSightClientCamera {
    private BorrowedSightClientCamera() { }

    public static void accept(Player logicalPlayer, BorrowedSightCameraPayload payload) {
        Objects.requireNonNull(payload, "payload");
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.level == null) return;
        if (logicalPlayer != null && !minecraft.player.getUUID().equals(logicalPlayer.getUUID())) return;

        if (!payload.active()) {
            minecraft.setCameraEntity(minecraft.player);
            return;
        }

        Entity target = minecraft.level.getEntity(payload.entityId());
        if (target == null || !target.isAlive() || !payload.targetId().equals(target.getUUID())) {
            minecraft.setCameraEntity(minecraft.player);
            return;
        }
        minecraft.setCameraEntity(target);
    }
}
