package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.ClientTickEvent;

import java.util.Objects;

/**
 * Physical-client presentation adapter for server-authorized Borrowed Sight.
 *
 * <p>This controller never admits observations, chooses targets, extends durations or sends gameplay
 * intent. It only follows the latest clientbound entity id while that entity remains loaded locally,
 * then restores the camera to the player's physical body.</p>
 */
public final class BorrowedSightClientController {
    private static volatile int targetEntityId = -1;
    private static Entity ownedCameraEntity;

    private BorrowedSightClientController() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(BorrowedSightClientController::onClientTick);
    }

    public static void accept(Player player, NoeticViewPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");

        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || player != minecraft.player) {
            return;
        }

        if (payload.action() == NoeticViewPayload.Action.BEGIN) {
            targetEntityId = payload.targetEntityId();
            return;
        }

        if (targetEntityId == payload.targetEntityId()) {
            targetEntityId = -1;
        }
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.level == null) {
            targetEntityId = -1;
            ownedCameraEntity = null;
            return;
        }

        int desiredTarget = targetEntityId;
        if (desiredTarget < 0) {
            restorePhysicalBody(minecraft);
            return;
        }

        Entity target = minecraft.level.getEntity(desiredTarget);
        if (target == null || target.isRemoved()) {
            BorrowedSightClientController.targetEntityId = -1;
            restorePhysicalBody(minecraft);
            return;
        }

        if (minecraft.getCameraEntity() != target) {
            minecraft.setCameraEntity(target);
        }
        ownedCameraEntity = target;
    }

    private static void restorePhysicalBody(Minecraft minecraft) {
        if (ownedCameraEntity == null || minecraft.player == null) {
            return;
        }
        if (minecraft.getCameraEntity() == ownedCameraEntity) {
            minecraft.setCameraEntity(minecraft.player);
        }
        ownedCameraEntity = null;
    }
}
