package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.content.noetic.AstralProjectionEntity;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.ClientTickEvent;

import java.util.Objects;
import java.util.Optional;

/**
 * Physical-client presentation adapter for server-authorized Astral Severance.
 *
 * <p>The controller owns only camera presentation. A BEGIN may precede vanilla entity spawn, so the exact
 * desired projection identity is retained while the physical camera stays on the body until the matching
 * loaded representation appears or an authoritative END clears the session.</p>
 */
public final class AstralSeveranceClientController {
    private static final AstralViewClientState STATE = new AstralViewClientState();
    private static Entity ownedCameraEntity;

    private AstralSeveranceClientController() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(AstralSeveranceClientController::onClientTick);
    }

    public static void accept(Player player, AstralViewPayload payload) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(payload, "payload");

        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || player != minecraft.player) {
            return;
        }
        STATE.accept(payload);
    }

    static Optional<AstralViewClientState.Desired> desiredProjection() {
        return STATE.desired();
    }

    /**
     * Returns armed control only while this controller still owns the exact Astral camera representation.
     * A server MOVE_ARM received before vanilla entity spawn stays dormant instead of suppressing the body
     * while the player is still looking through another camera. Likewise, external camera ownership, removal
     * or identity replacement immediately makes input redirection fail closed until reconciliation succeeds.
     */
    static Optional<AstralViewClientState.Desired> movementControl() {
        AstralViewClientState.Desired control = STATE.movementControl().orElse(null);
        if (control == null) {
            return Optional.empty();
        }

        Minecraft minecraft = Minecraft.getInstance();
        if (ownedCameraEntity == null
                || minecraft.getCameraEntity() != ownedCameraEntity
                || ownedCameraEntity.isRemoved()
                || ownedCameraEntity.getId() != control.entityId()
                || !ownedCameraEntity.getUUID().equals(control.projectionId())) {
            return Optional.empty();
        }
        return Optional.of(control);
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.level == null) {
            STATE.clear();
            ownedCameraEntity = null;
            return;
        }

        AstralViewClientState.Desired desired = STATE.desired().orElse(null);
        if (desired == null) {
            restorePhysicalBody(minecraft);
            return;
        }

        Entity target = minecraft.level.getEntity(desired.entityId());
        if (!(target instanceof AstralProjectionEntity)
                || target.isRemoved()
                || !target.getUUID().equals(desired.projectionId())) {
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
